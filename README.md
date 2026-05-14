# Scraper Exercise

Author: Matteo Severi

Standard tools for collecting motorcycle data lack structure and
scalability. This project builds a Scrapy-based spider that crawls
motorcycle.com, extracting technical specifications across brands,
models, and categories from a multi-page listing into a structured
JSON/CSV output. The spider navigates paginated brand pages, follows
individual model links, and parses spec tables into flat records
ready for analysis.
