# Scrapista
Scrapista helps with scraping datasets from some of the most popular websites such as Wikipedia, Amazon, etc.


## Installation
---
<!-- Github Markdown -->
```
$ python -m pip install scrapista
```

## Getting started with the Amazon scraper: 
```python 
from scrapista.amazon import AmazonScraper

# sample headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
# default url
base_url = "https://www.amazon.com"
# you don't have to pass them in since they are already default
scraper = AmazonScraper(base_url,headers)
data_list = scraper.scrape_keywords(["pencil","couch"])

print(len(data_list)) # 120
```
<style>
    .center {
        text-align:center;
    }
</style>
<hr>
<h2 class="center">Aligned Center</h2>
