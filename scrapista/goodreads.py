from helpers.helpers import get_count
from bs4 import BeautifulSoup
from time import perf_counter
import concurrent.futures
import threading as th
import requests
import re
import datetime as dt


class GoodReadsScraper:
    
    def __init__(self,base_url="https://www.goodreads.com/genres/mystery"):
        self.base_url = base_url
        pass


    @property
    def popular_quotes(self):
        """
            This property scrapes the most popular quotes on goodreads from 
            the first page of all the quotes
        """

        url = "https://www.goodreads.com/quotes?page=1"
        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")
        quotes = soup.select(".quote")

        quotes_list = []
        
        for quote in quotes: 
            try: 
                like_tag = quote.select_one(".right .smallText")
                likes = int(get_count(like_tag.get_text("",strip=True)))
            except Exception as e:
                likes = "N/A"
                print("likes|", e)
                pass

            try:
                quote_tag = quote.select_one(".quoteText")
                for idx, quoteText in enumerate(quote_tag.stripped_strings): 
                    if idx == 0:
                        quote_text = quoteText

            except Exception as e:
                print("quote|", e)
                continue

            try: 
                by_tag = quote.select_one(".authorOrTitle")
                by = by_tag.get_text("",strip=True)
            except Exception as e:
                print("by|", e)
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
        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")

        book_data_list = []

        wrappers = soup.select(".coverWrapper")

        links = []  
        for wrapper in wrappers: 
            try:
                link = wrapper.find("a")
            except: 
                raise(BaseException("Genre is not a valid genre"))
            else: 
                links.append(link)

        images = []
        for link in links: 
            try: 
                images.append(link.find("img"))
            except Exception as e:
                print(e)
                pass
        
        # print("images:",images)
        # print("links:", links)
        for link, image in zip(links,images): 

            try: 
                book_url = self.base_url + link["href"]
            except Exception as e:
                print(e)
                book_url = "N/A"
                pass

            try: 
                book_title = image["alt"]
            except Exception as e: 
                print(e)
                if not book_url: 
                    continue
                book_title = "N/A"
                pass
                

            try:
                cover_url = image["src"]
            except Exception as e:
                cover_url = "N/A"
                print(e)
                pass

            book_object = {
                "title": book_title,
                "genre": genre,
                "book_url": book_url,
                "cover_url": cover_url,
            }

            book_data_list.append(book_object)

        return book_data_list


    def scrape_book(self,url):
        """
            This function helps you scrape the data of a book by passing the 
            goodreads url of that book into the function
        """

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")

        try: 
            title_tag = soup.select_one("#bookTitle")
            title = title_tag.get_text("",strip=True)
        except Exception as e: 
            title = None
            print(e)
            pass

        try: 
            book_cover_tag = soup.find(id="coverImage")
            book_cover = book_cover_tag["src"]
        except Exception as e:
            book_cover = None
            print(e)
            pass

        try:
            rating_tag = soup.find(itemprop="ratingValue")
            rating = float(rating_tag.get_text("",strip=True))
        except Exception as e:
            rating = None
            print(e)
            pass

        try:
            rating_count_tag = soup.find(itemprop="ratingCount")
            rating_count = get_count(rating_count_tag.get_text("",strip=True))
        except Exception as e:
            rating_count = None
            print(e)
            pass

        try:
           review_count_tag = soup.find(itemprop="reviewCount")
           review_count = get_count(review_count_tag.get_text("",strip=True))
        except Exception as e:
            review_count = None
            print(e)
            pass

            
        book_object = {
            "title": title,
            "rating(5)": rating,
            "rating_count": rating_count,
            "review_count": review_count,
            "cover_url": book_cover
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


start = perf_counter()

gr = GoodReadsScraper()



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

urls = [
    "https://www.goodreads.com/book/show/2429135.The_Girl_with_the_Dragon_Tattoo",
    "https://www.goodreads.com/book/show/52758545-the-black-coast",
    "https://www.goodreads.com/book/show/54304115-the-girl-from-shadow-springs",
    "https://www.goodreads.com/book/show/43263361-crown-of-bones"
]

# book_data_list = gr.async_scrape_books(urls)

# print(book_data_list)






end = perf_counter()

print(f"In total it took {end-start:.2f} second(s)")