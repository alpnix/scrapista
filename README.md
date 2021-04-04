# Scrapista
Scrapista helps with scraping datasets from some of the most popular websites such as Wikipedia, Amazon, etc.


## Installation
---
<!-- Github Markdown -->
```
$ python -m pip install scrapista
```
## Scraping Wikipedia
---
Importing WikiScraper class
```python
from scrapista.wikipedia import WikiScraper

ws = WikiScraper()

# these are some properties of WikiScraper class
highest_grossings = ws.highest_grossing_movies
print(highest_grossings)
"""[{'name':'Avatar','url':'https://en.wikipedia.org/wiki/Avatar_(2009_film)'},{'name':'Avengers: Endgame','url':'https://en.wikipedia.org/wiki/Avengers:_Endgame'},...]"""

important_people = ws.most_important_people
print(important_people)
"""[{'name':'Barack Obama','url':'https://en.wikipedia.org/wiki/Barack_Obama'},{'name':'Xi Jinping','url':'https://en.wikipedia.org/wiki/Xi_Jinping'},...]"""
```
It is also possible to scrape data dynamically..
```python
ws = WikiScraper()
movie_url = "https://en.wikipedia.org/wiki/The_Shawshank_Redemption"

movie_data = ws.scrape_movie(movie_url)
print(movie_data)
"""{'title': 'The Shawshank Redemption', 'Directed by': 'Frank Darabont', 'Produced by': 'Niki Marvin', 'Screenplay by': 'Frank Darabont', 'Based on': 'Rita Hayworth and Shawshank Redemption by Stephen King', 'Starring': ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton', 'William Sadler', 'Clancy Brown', 
'Gil Bellows', 'James Whitmore'], 'Music by': 'Thomas Newman',...}"""
```
You may also want to scrape info of any person
```python
ws = WikiScraper()
person_url = "https://en.wikipedia.org/wiki/Stephen_King"

# you can pass in the url
person_data = ws.scrape_person(person_url)

# or alternatively,
# you can pass in the name of the person
person_data = ws.scrape_person(name="Stephen King")
print(person_data)
"""{'Name': 'Stephen King', 'Born': 'Portland, Maine, U.S.', 'Pen name': ['Richard Bachman', 'John Swithen', 'Beryl Evans'], 'Occupation': 'Author', 'Alma mater': 'University of Maine', 'Period': '1967–present', 'Genre': ['Horror','fantasy', 'supernatural fiction', 'drama', 'gothic', 'genre fiction','dark fantasy', 'post-apocalyptic fiction', 'crime fiction', 'suspense', 'thriller'], 'Spouse': 'Tabitha Spruce (1971-present)','Children':3,'Age':73,'Birth Date':datetime.datetime(1947, 9, 21, 0, 0)}"""
```
If none of those methods were helpful you could use the custom scraping method
```python
ws = WikiScraper()

# with this method you can scrape info about a company, a place, or an event
url = "https://en.wikipedia.org/wiki/Microsoft"

msft_data = ws.scrape_custom(url)
print(msft_data)
"""{'Name': 'Microsoft Corporation', 'Type': 'Public', 'Traded as': ['Nasdaq : MSFT', 'Nasdaq-100 component', 'DJIA component', 'S&P 100 component', 'S&P 500 component'], 'ISIN': 'US5949181045', 'Industry': ['Software development', 'Computer hardware',...]...}"""

# alternatively,
# you can pass in the name as well
br_data = ws.scrape_custom(name="Brazil")
print(br_data)
"""{'Name': 'Federative Republic of Brazil(Portuguese)', 'Capital': 'Brasília 15°47′S 47°52′W  /  15.783°S 47.867°W', 'Largest city': 'São Paulo 23°33′S 46°38′W  /  23.550°S 46.633°W', 'Official language and national language': 'Portuguese', 'Ethnic groups (2010)': ['47.73% White', '43.13% Mixed',...]...}"""
```
## Scraping Amazon: 
---
```python 
from scrapista.amazon import AmazonScraper

# you don't have to pass them in since they are already default
ams = AmazonScraper()
data_list = ams.scrape_keyword("pencil")

print(data_list)
"""
[{'name': 'Faber Castell - Sparkle Pencil', 'price(USD)': 7.64, 'stars(5)': 4.9, 'url': 'https://www.amazon.com/-/en/218485-Faber-Castell-Sparkle-Pencil/dp/B08LL7D76C/ref=sr_1_22?currency=USD&dchild=1&keywords=Bleistift&qid=1617311520&sr=8-22', 'img_source': 'https://m.media-amazon.com/images/I/712WnPZ6FpL._AC_UL320_.jpg'}, {'name': 'Faber-Castell 119065 – Pencil Castell 9000, Set of 12, Art Set, Contains 8B – 2H pencils, Basic assortment 8b - 2h', 'price(USD)': 16.41, 'stars(5)': 4.9, 'url': 'https://www.amazon.com/-/en/Faber-Castell-119065-Castell-Contains-assortment/dp/B000I5MNC0/ref=sr_1_23?currency=USD&dchild=1&keywords=Bleistift&qid=1617311520&sr=8-23', 'img_source': 'https://m.media-amazon.com/images/I/91-gnNu26JL._AC_UL320_.jpg'},...]
"""

print(len(data_list)) # 60
```
Or you can track a single item and get info about it..
```python
url = "https://www.amazon.de/-/en/23-8-inch-Full-all-one/dp/B089PJ5S5B/ref=sr_1_3?currency=USD&dchild=1&keywords=computer&qid=1617312928&sr=8-3"

item_info = ams.track_item(url)

print(item_info)
"""{'title': 'HP (23.8 inch / Full HD) all-in-one PC.', 'stars(out of 5)': 4.4, 'price': 702.44, 'note': 'Prices for items sold by Amazon include VAT. Depending on your delivery address, VAT may vary at Checkout. For other items, 
please see details.'}"""
```
