import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
import logging
from streamlit_autorefresh import st_autorefresh
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    nltk.download('punkt')
except Exception as e:
    logging.error(f"Failed to download 'punkt' from NLTK: {e}")
    st.error("Failed to download 'punkt' from NLTK. Please check the console for more details.")

st.set_page_config(page_title='News Summarizer: A Summarised News📰 Portal', page_icon='./Meta/newspaper.ico')

if 'previous_news' not in st.session_state:
    st.session_state['previous_news'] = {}

def fetch_category_news(topic):
    base_url = 'https://news.google.com/rss/search?q={category}+when:1d&hl=en-US&gl=US&ceid=US:en'
    site = base_url.format(category=topic.replace(' ', '+'))

    try:
        op = urlopen(site)
        rd = op.read()
        op.close()
        sp_page = soup(rd, 'xml')
        news_list = sp_page.find_all('item')
        return news_list
    except Exception as e:
        logging.error(f"Failed to fetch news for {topic}: {e}")
        st.error(f"Failed to fetch news for {topic}. Please check the console for more details.")
        return None

def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        st.image(image, use_column_width=True)
    except Exception as e:
        logging.warning(f"Failed to load image: {e}")
        st.warning(f"Failed to load image. Please check the console for more details.")
        st.image('./Meta/no_image.jpg', use_column_width=True)

def summarize_text(text, sentence_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join([str(sentence) for sentence in summary])

def display_news(list_of_news, news_quantity):
    c = 0
    successful_news = []
    for news in list_of_news:
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
            successful_news.append((news, news_data))
        except Exception as e:
            logging.error(f"Failed to extract information from {news.link.text}: {e}")
            continue
        if len(successful_news) >= news_quantity:
            break

    for i, (news, news_data) in enumerate(successful_news):
        c += 1
        st.write('**({}) {}**'.format(c, news.title.text))
        fetch_news_poster(news_data.top_image)
        with st.expander(news.title.text):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}</h6>'''.format(news_data.summary),
                unsafe_allow_html=True)
            st.markdown("[Read more at {}]({})".format(news.source.text, news.link.text))

            # Display important abstracts
            try:
                important_abstracts = summarize_text(news_data.text, sentence_count=5)
                st.markdown(f"**Important Points:**")
                st.markdown(important_abstracts)
            except ValueError as e:
                logging.warning(f"Failed to summarize text: {e}")
                st.markdown("Summarization not possible for this article.")

        st.success("Published Date: " + news.pubDate.text)

def fetch_research_papers():
    url = "https://huggingface.co/papers"
    try:
        response = requests.get(url)
        page = soup(response.content, 'html.parser')
        papers = page.find_all('article')
        paper_info_list = []

        for paper in papers:
            paper_details = {}
            paper_link = paper.find('a', href=True)['href']
            paper_url = f"https://huggingface.co{paper_link}"
            paper_details['url'] = paper_url
            paper_response = requests.get(paper_url)
            paper_page = soup(paper_response.content, 'html.parser')

            try:
                title_elem = paper_page.find('h1', class_='mb-2 text-2xl font-semibold sm:text-3xl lg:pr-6 lg:text-3xl xl:pr-10 2xl:text-4xl')
                if title_elem:
                    paper_details['title'] = title_elem.text.strip()

                image_elem = paper_page.find('img', class_='h-full w-full object-cover object-top')
                if image_elem:
                    paper_details['image_url'] = image_elem['src']

                abstract_div = paper_page.find('div', class_='pb-8 pr-4 md:pr-16')
                if abstract_div:
                    paper_details['abstract'] = abstract_div.find('p').text.strip()

                authors_div = paper_page.find('div', class_='order-first ml-3')
                if authors_div:
                    paper_details['authors'] = authors_div.text.strip()

                published_date_tag = paper_page.find('time')
                if published_date_tag:
                    paper_details['published_date'] = published_date_tag['datetime']

                paper_info_list.append(paper_details)
            except AttributeError as e:
                logging.warning(f"Missing information in paper at {paper_url}: {e}")
            except Exception as e:
                logging.error(f"Error processing paper at {paper_url}: {e}")

        return paper_info_list
    except Exception as e:
        logging.error(f"Failed to fetch research papers: {e}")
        st.error("Failed to fetch research papers. Trying to fetch from Google...")
        return fetch_research_papers_google()


def fetch_research_papers_google():
    # This function will search Google and return summarized AI research papers
    google_search_url = "https://www.google.com/search?q=AI+research+papers&tbm=nws"
    try:
        response = requests.get(google_search_url)
        page = soup(response.content, 'html.parser')
        news_articles = page.find_all('div', class_='BVG0Nb')
        paper_info_list = []

        for article in news_articles:
            paper_details = {}
            title_tag = article.find('a')
            if title_tag:
                paper_details['title'] = title_tag.text
                paper_details['url'] = title_tag['href']
                summary_tag = article.find('div', class_='Y3v8qd')
                if summary_tag:
                    paper_details['abstract'] = summary_tag.text

                time_tag = article.find('span', class_='WG9SHc')
                if time_tag:
                    paper_details['published_date'] = time_tag.find('time')['datetime']

                paper_info_list.append(paper_details)

        return paper_info_list
    except Exception as e:
        logging.error(f"Failed to fetch research papers from Google: {e}")
        st.error("Failed to fetch research papers from Google.")
        return []

def display_research_papers(papers, paper_quantity):
    for i, paper in enumerate(papers[:paper_quantity]):
        st.write('**({}) {}**'.format(i + 1, paper['title']))
        st.markdown(f"[Read full paper here]({paper['url']})")

        with st.expander(paper['title']):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}</h6>'''.format(paper['abstract']),
                unsafe_allow_html=True)
            st.markdown(f"**Authors:** {paper.get('authors', 'N/A')}")
            st.markdown(f"**Published Date:** {paper.get('published_date', 'N/A')}")
            st.markdown(f"[View arXiv page](https://arxiv.org/abs/{paper['url'].split('/')[-1]})")

def run():
    st.title("News Summarizer: A Summarised News📰 Portal")

    # Category selection
    categories = ['Technology', 'Science', 'Artificial Intelligence', 'Research Papers']
    chosen_category = st.selectbox("Select News Category:", categories)

    no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)

    # Auto-refresh functionality with Streamlit's built-in method
    count = st_autorefresh(interval=20 * 60 * 1000, key="refresh_counter")

    if chosen_category == 'Research Papers':
        research_papers = fetch_research_papers()
        if research_papers:
            st.subheader(f"✅ Here are some research papers on AI for you")
            display_research_papers(research_papers, no_of_news)
        else:
            st.error("No research papers found.")
    else:
        news_list = fetch_category_news(chosen_category)
        new_news_available = False  # New flag to track if news is updated
        if news_list:
            if chosen_category not in st.session_state['previous_news'] or len(news_list) != len(st.session_state['previous_news'][chosen_category]):
                st.session_state['previous_news'][chosen_category] = news_list
                new_news_available = True  # Set flag to True if news is updated

            if count:
                st.success("News has been updated!")
            st.subheader(f"✅ Here are some {chosen_category} news for you")
            display_news(news_list, no_of_news)

            if new_news_available:  # Show toast only if news is updated
                st.toast("New news updates are available!")
        else:
            st.error(f"No news found for {chosen_category}")

try:
    run()
except Exception as e:
    logging.error(f"An error occurred: {e}")
    st.error("An unexpected error occurred. Please check the console for more details.")
