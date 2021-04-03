from scrapista.helpers.helpers import get_count, get_word_info
from bs4 import BeautifulSoup
from time import perf_counter
import concurrent.futures
import threading as th
import requests
import re
import datetime as dt


class GoodReadsScraper:
    
    def __init__(self,base_url="https://www.goodreads.com",headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}):
        self.base_url = base_url
        pass


    @property
    def popular_quotes(self):
        """
            This property scrapes the most popular quotes on goodreads from 
            the first page of all the quotes
        """

        url = "https://www.goodreads.com/quotes?page=1"
        try:
            r = requests.get(url)
        except:
            return "Connection Error"

        soup = BeautifulSoup(r.content, "html.parser")
        quotes = soup.select(".quote")

        quotes_list = []
        
        for quote in quotes: 
            try: 
                like_tag = quote.select_one(".right .smallText")
                likes = int(get_count(like_tag.get_text("",strip=True)))
            except Exception as e:
                likes = "N/A"
                pass

            try:
                quote_tag = quote.select_one(".quoteText")
                for idx, quoteText in enumerate(quote_tag.stripped_strings): 
                    if idx == 0:
                        quote_text = quoteText

            except Exception as e:
                continue

            try: 
                by_tag = quote.select_one(".authorOrTitle")
                by = by_tag.get_text("",strip=True)
            except Exception as e:
                by = "Anonymous"
            

            quote_object = {
                "quote": quote_text,
                "by": by,
                "likes": likes
            }

            quotes_list.append(quote_object)
        
        return quotes_list


    def scrape_quotes_by_tag(self,tag,page=1):
        """
            This function expects a tag of a quote and a page number 
            and it will return a quote object in json form.
        """

        if page > 100: 
            raise(Exception("invalid page number: page number should be between 1-100"))

        url = f"https://www.goodreads.com/quotes/tag/{tag}?page={page}"
        try:
            r = requests.get(url)
        except Exception as e:
            return "Connection Error"

        soup = BeautifulSoup(r.content, "html.parser")
        quotes = soup.select(".quote")

        quotes_list = []
        
        for quote in quotes: 
            try: 
                like_tag = quote.select_one(".right .smallText")
                likes = int(get_count(like_tag.get_text("",strip=True)))
            except Exception as e:
                likes = "N/A"
                pass

            try:
                quote_tag = quote.select_one(".quoteText")
                for idx, quoteText in enumerate(quote_tag.stripped_strings): 
                    if idx == 0:
                        quote_text = quoteText

            except Exception as e:
                continue

            try: 
                by_tag = quote.select_one(".authorOrTitle")
                by = by_tag.get_text("",strip=True)
            except Exception as e:
                by = "Anonymous"
            

            quote_object = {
                "quote": quote_text,
                "by": by,
                "likes": likes
            }

            quotes_list.append(quote_object)
        
        return quotes_list


    def scrape_books_by_genre(self,genre): 
        
        url = "https://www.goodreads.com/genres/" + genre
        try:
            r = requests.get(url)
        except: 
            return "Connection Error"

        soup = BeautifulSoup(r.content, "html.parser")

        book_data_list = []

        wrappers = soup.select(".coverWrapper")

        links = []  
        for wrapper in wrappers: 
            try:
                link = wrapper.find("a")
            except: 
                raise(Exception("Genre is not a valid genre"))
            else: 
                links.append(link)

        images = []
        for link in links: 
            try: 
                images.append(link.find("img"))
            except Exception as e:
                pass
        
        for link, image in zip(links,images): 

            try: 
                book_url = self.base_url + link["href"]
            except Exception as e:
                book_url = "N/A"
                pass

            try: 
                book_title = image["alt"]
            except Exception as e: 
                if not book_url: 
                    continue
                book_title = "N/A"
                pass
                

            try:
                cover_url = image["src"]
            except Exception as e:
                cover_url = "N/A"
                pass

            book_object = {
                "title": book_title,
                "genre": genre,
                "url": book_url,
                "img_src": cover_url,
            }

            book_data_list.append(book_object)

        return book_data_list


    def scrape_book(self,url):
        """
            This function helps you scrape the data of a book by passing the 
            goodreads url of that book into the function
        """

        try:
            r = requests.get(url)
        except: 
            return "Connection Error"

        soup = BeautifulSoup(r.content, "html.parser")

        try: 
            title_tag = soup.select_one("#bookTitle")
            title = title_tag.get_text("",strip=True)
        except Exception as e: 
            title = None
            pass

        try: 
            book_cover_tag = soup.find(id="coverImage")
            book_cover = book_cover_tag["src"]
        except Exception as e:
            book_cover = None
            pass

        try:
            rating_tag = soup.find(itemprop="ratingValue")
            rating = float(rating_tag.get_text("",strip=True))
        except Exception as e:
            rating = None
            pass

        try:
            rating_count_tag = soup.find(itemprop="ratingCount")
            rating_count = get_count(rating_count_tag.get_text("",strip=True))
        except Exception as e:
            rating_count = None
            pass

        try:
           review_count_tag = soup.find(itemprop="reviewCount")
           review_count = get_count(review_count_tag.get_text("",strip=True))
        except Exception as e:
            review_count = None
            pass

            
        book_object = {
            "name": title,
            "rating(5)": rating,
            "rating_count": rating_count,
            "review_count": review_count,
            "img_src": book_cover
        }


        return book_object


    def async_scrape_books(self,urls):
        """
            This function runs the 'scrape_book' function asynchronously with 
            ThreadPoolExecutor.
        """

        book_list = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for url in urls: 
                future = executor.submit(self.scrape_book,url=url)
                book_data = future.result()
                book_list.append(book_data)

        return book_list



# start = perf_counter()

# gr = GoodReadsScraper()

"getting most popular quotes"

# quotes = gr.popular_quotes

# print(quotes)


"scraping books by their genre"

# book_list = gr.scrape_books_by_genre("mystery")

# print(book_list)
# print(len(book_list))


"scraping particular books by their url"

# book_data = gr.scrape_book("https://www.goodreads.com/book/show/2429135.The_Girl_with_the_Dragon_Tattoo")

# print(book_data)


"scraping multiple movies asynchronously"
"p.s. takes to much time at the moment"

# urls = [
#     "https://www.goodreads.com/book/show/2429135.The_Girl_with_the_Dragon_Tattoo",
#     "https://www.goodreads.com/book/show/52758545-the-black-coast",
#     "https://www.goodreads.com/book/show/54304115-the-girl-from-shadow-springs",
#     "https://www.goodreads.com/book/show/43263361-crown-of-bones"
# ]

# book_data_list = gr.async_scrape_books(urls)

# print(book_data_list)



"scrape a page of quotes of a tag"

# quote_list = gr.scrape_custom_quotes("life")

# print(quote_list)
# print(len(quote_list))


"scraping quotes by the custom values put into function"
"sync: 139.49s", "async: 271.80s"
# total_quotes = []
# for i in range(50):
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future = executor.submit(gr.scrape_custom_quotes,tag="love",page=i)
#         quote_list = future.result()
#         total_quotes.extend(quote_list)

#     print(i, "done")

# print(len(total_quotes))



# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
# }



# end = perf_counter()

# print(f"In total it took {end-start:.2f} second(s)")