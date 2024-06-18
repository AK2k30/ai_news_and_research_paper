# InNews🇮🇳: News Summarizer App

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)   

## Overview

AINewsSummari is a web application built with Streamlit, aimed at providing users with curated news and research papers. The application fetches data from various sources such as Google News and Hugging Face Papers, summarizes news articles using natural language processing (NLP) techniques, and allows users to explore detailed information about research papers related to Artificial Intelligence.

## [Demo of App](https://share.streamlit.io/spidy20/innews/App.py)

## Purpose

The purpose of AINewsSummari is to provide users with a convenient way to:

- Stay updated with the latest news in categories like Technology, Science, and more.
- Explore and read detailed summaries of news articles.
- Discover and access research papers related to Artificial Intelligence.

## Source
- For summarizing the news I have used [Newspaper3k](https://newspaper.readthedocs.io/en/latest/)
- For scraping the news I have used Google News RSS API.

## Tool used

- Python: Programming language used for backend logic and data processing.
- Streamlit: Open-source framework for building interactive web applications.
- Beautiful Soup: Python library for scraping data from HTML and XML files.
- Newspaper3k: Python library for extracting and curating articles from websites.
- NLTK: Natural Language Toolkit used for text processing tasks like tokenization.
- Pillow: Python Imaging Library used for image processing.
- Requests: Python library for making HTTP requests.
- Sumy: Library for automatic text summarization.

## Main Feature

- Category Selection: Users can choose from categories like Technology, Science, and Artificial     Intelligence to view news articles.
- Automatic Summarization: News articles are summarized using LexRankSummarizer to highlight  important points.
- Image Display: Images associated with news articles are displayed using the PIL library.
Auto-refresh: The application automatically refreshes every 20 minutes to fetch updated news.

## Features
- Trending News
- Favorite Topics
- Search News
- Quantity control
- Summary of AI research paper

## Usage
- Clone my repository.
- Open CMD in working directory.
- Run following command.
  ```
  pip install -r requirements.txt
  ```
- `App.py` is the main Python file of Streamlit Web-Application. 
- To run app, write following command in CMD. or use any IDE.
  ```
  streamlit run App.py --server.port 80
  ```

## Just follow☝️ me and Star⭐ my repository 

## [Buy me a Coffee☕](https://www.buymeacoffee.com/spidy20)
