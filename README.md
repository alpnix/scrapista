# Scrapista
Scrapista helps with scraping datasets from some of the most popular websites such as Wikipedia, Amazon, etc.


## Installation
---
<!-- Github Markdown -->
```
$ python -m pip install scrapista
```

## Getting started to use the Amazon scraper: 
```python 
from scrapista import AmazonScraper

# sample headers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

base_url = "https://www.amazon.com"

scraper = AmazonScraper(headers,base_url)
data_list = scraper.scrape_keywords(["pencil","couch"])

print(len(data_list)) # 120
```

