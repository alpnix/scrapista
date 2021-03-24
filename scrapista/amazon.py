from bs4 import BeautifulSoup
from time import perf_counter
import concurrent.futures
import threading as th
import requests
import re



class AmazonScraper:
    """
        This class has some methods that scrape the amazon website 
        and return you some data. 
    """
    def __init__(self,headers,base_url="https://www.amazon.de"):
        self.base_url = base_url
        self.headers = headers
        self.tracked = []

    
    def scrape_keyword(self,keyword,data_list=[]):

        """
            Scrape all the instances of a single element
        """

        url_keyword_addition = f"/s?k={keyword}&language=en_GB&currency=USD&ref=nb_sb_noss_2"
        r = requests.get(self.base_url+url_keyword_addition,headers=self.headers)
        soup = BeautifulSoup(r.content, "html.parser")
        groups = soup.select(".a-section.a-spacing-medium")

        for group in groups: 

            name_tag = group.select_one(".a-link-normal.a-text-normal")
            image = group.select_one(".s-image")
            stars = group.select_one(".a-icon-alt")
            price = group.select_one(".a-price-whole")

            try: 
                price_amount = price.get_text(strip=True).replace(",",".")
                price_amount = float(price_amount)
            except: 
                price_amount = None

            try: 
                source = image["src"]
            except: 
                source = None

            try: 
                star_amount = stars.get_text(strip=True)[:3].replace(",",".")
                star_amount = float(star_amount)
            except: 
                star_amount = None

            try:
                product_name = name_tag.get_text("|",strip=True)
            except: 
                product_name = None

            try: 
                product_url = self.base_url + name_tag["href"]
            except: 
                product_url = None

            laptop_object = {
                "img_source": source,
                "stars": star_amount,
                "price": price_amount,
                "name": product_name,
                "url": product_url
            }
            
            data_list.append(laptop_object)

        
        data_list = list(filter(lambda x: any(x.values()), data_list)) 

        return data_list


    def scrape_keywords(self,keywords,data_list=[]): 

        """
            Expects a list of items and it will scrape the data
            for each element in that list and return it in json form
        """

        if type(keywords) != list: 
            raise BaseException("A list type is expected for 'keywords' argument")


        for keyword in keywords: 
            self.scrape_keyword(keyword,data_list)
        
        return data_list[:-1]


    def async_scrape_keywords(self,keywords,data_list=[]): 

        """
            This function is the exact same of the scrape_keyword function
            but this one runs with multiprocessing therefore it's much faster
        """

        if type(keywords) != list: 
            raise BaseException("A list type is expected for 'keywords' argument")

        threads = [th.Thread(target=self.scrape_keyword,args=(keyword,data_list)) for keyword in keywords]

        for t in threads: 
            t.start()
        
        for t in threads: 
            t.join()

        return data_list[:-1]

    
    def track_item(self, url): 

        """
            You will pass a list of urls and an interval, it returns the current price and state of all those items
        """

        url_list = url.split(self.base_url)
        item_code = url_list[-1]
        url = self.base_url + item_code + "?language=en_GB&currency=USD"
        r = requests.get(url,headers=self.headers)

        if r.status_code not in [200,304,301]:
            raise BaseException("request not successful")

        soup = BeautifulSoup(r.content, "html.parser")

        title_tag = soup.select_one("#productTitle")
        stars_tag = soup.select_one(".a-icon.a-icon-star.a-star-4-5")
        price_tag = soup.find(id="priceblock_ourprice")
        if not price_tag: 
            price_tag = soup.find(id="priceblock_dealprice")
        note_tag = soup.find(id="vatMessage")


        try: 
            title = title_tag.get_text("|",strip=True)
        except Exception as e: 
            title = None

        try: 
            stars = stars_tag.get_text("|",strip=True)[:3].replace(",",".")
            stars = float(stars)
        except Exception as e: 
            stars = None
        
        try: 
            price = price_tag.get_text("|",strip=True).replace(".","")
            price = price.replace(",",".")
            price_list = price.split(".")
            price = price_list[0] + "." + price_list[1][:2]
            price = float(price)            
        except Exception as e: 
            price = None


        item_object = {
            "title": title,
            "stars": stars,
            "price": price,
        }

        if note_tag: 
            item_object["note"] = note_tag.get_text(" ",strip=True)

        if url not in self.tracked: 
            self.tracked.append(url)


        return item_object


    def track_items(self,urls,data_list=[]):
        """
            Track all the items that are passed into the function as 
            list type. 
        """

        if type(urls) != list: 
            raise BaseException("A list type is expected for 'urls' argument")

        for url in urls: 

            data = self.track_item(url)
            data_list.append(data)

        data_list = list(filter(lambda x: any(x.values()), data_list)) 

        return data_list


    def async_track_items(self,urls,data_list=[]):
        """
            This function is the asynchronous version of the 
            AmazonScraper.track_items function 
        """

        if type(urls) != list: 
            raise BaseException("A list type is expected for 'urls' argument")



        with concurrent.futures.ThreadPoolExecutor() as executor:
            for url in urls: 
                future = executor.submit(self.track_item,url)
                data = future.result()
                data_list.append(data)


        data_list = list(filter(lambda x: any(x.values()), data_list)) 

        return data_list



headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}

items = [
    "pencil","cardboard","racket","paddle","book","headphone","water bottle","usb charger","book shelf","paper","markers","pencilcase","notebook","calculator"
]

start = perf_counter()
scraper = AmazonScraper(headers)

"Sync Single keyword"

# data = scraper.scrape_keyword("airpod")

# print(data)

"Scraping multiple keywords"
"Sync scraping keywords"

# data_list = scraper.scrape_keywords(items)
# print(len(data_list))

"Async scraping keywords"

data_list = scraper.async_scrape_keywords(items)
print(len(data_list))

"Tracking item"

# airpod = scraper.track_item("https://www.amazon.de/-/en/Lenovo-IdeaPad-Chromebook-WideView-Tablet/dp/B08CZXFKDP/?_encoding=UTF8&pd_rd_w=wofLG&pf_rd_p=07208ea4-5452-4c67-8f65-44901c0f68eb&pf_rd_r=0JJ8ZD05AEXFSZAQB3TS&pd_rd_r=8c4d6402-ff5e-4ee0-b158-13f872c81f7d&pd_rd_wg=BfT3H&ref_=pd_gw_ci_mcx_mr_hp_d")

# print(airpod)

"Tracking multiple items"

urls = [
    "https://www.amazon.de/-/en/Lenovo-IdeaPad-Chromebook-WideView-Tablet/dp/B08CZXFKDP/?_encoding=UTF8&pd_rd_w=wofLG&pf_rd_p=07208ea4-5452-4c67-8f65-44901c0f68eb&pf_rd_r=0JJ8ZD05AEXFSZAQB3TS&pd_rd_r=8c4d6402-ff5e-4ee0-b158-13f872c81f7d&pd_rd_wg=BfT3H&ref_=pd_gw_ci_mcx_mr_hp_d","https://www.amazon.de/Window-Battery-Charger-Supply-Karcher/dp/B07WCWHXRG/ref=sr_1_4_sspa?dchild=1&keywords=tuch&qid=1616610242&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQUpJVk5aM0dLVExVJmVuY3J5cHRlZElkPUEwNzU0MTk3SThHNlk4M0xJQTNaJmVuY3J5cHRlZEFkSWQ9QTAyNzgxNzkyWkJBNlg4S0pPVkU0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==","https://www.amazon.de/-/en/Heinz-Drache/dp/B014STN07I/ref=sr_1_12?dchild=1&keywords=tuch&qid=1616610258&sr=8-12","https://www.amazon.de/-/en/Lenovo-IdeaPad-Chromebook-WideView-Tablet/dp/B08CZXFKDP/?_encoding=UTF8&pd_rd_w=wofLG&pf_rd_p=07208ea4-5452-4c67-8f65-44901c0f68eb&pf_rd_r=0JJ8ZD05AEXFSZAQB3TS&pd_rd_r=8c4d6402-ff5e-4ee0-b158-13f872c81f7d&pd_rd_wg=BfT3H&ref_=pd_gw_ci_mcx_mr_hp_d","https://www.amazon.de/Window-Battery-Charger-Supply-Karcher/dp/B07WCWHXRG/ref=sr_1_4_sspa?dchild=1&keywords=tuch&qid=1616610242&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQUpJVk5aM0dLVExVJmVuY3J5cHRlZElkPUEwNzU0MTk3SThHNlk4M0xJQTNaJmVuY3J5cHRlZEFkSWQ9QTAyNzgxNzkyWkJBNlg4S0pPVkU0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==","https://www.amazon.de/-/en/Heinz-Drache/dp/B014STN07I/ref=sr_1_12?dchild=1&keywords=tuch&qid=1616610258&sr=8-12","https://www.amazon.de/-/en/Lenovo-IdeaPad-Chromebook-WideView-Tablet/dp/B08CZXFKDP/?_encoding=UTF8&pd_rd_w=wofLG&pf_rd_p=07208ea4-5452-4c67-8f65-44901c0f68eb&pf_rd_r=0JJ8ZD05AEXFSZAQB3TS&pd_rd_r=8c4d6402-ff5e-4ee0-b158-13f872c81f7d&pd_rd_wg=BfT3H&ref_=pd_gw_ci_mcx_mr_hp_d","https://www.amazon.de/Window-Battery-Charger-Supply-Karcher/dp/B07WCWHXRG/ref=sr_1_4_sspa?dchild=1&keywords=tuch&qid=1616610242&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQUpJVk5aM0dLVExVJmVuY3J5cHRlZElkPUEwNzU0MTk3SThHNlk4M0xJQTNaJmVuY3J5cHRlZEFkSWQ9QTAyNzgxNzkyWkJBNlg4S0pPVkU0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==","https://www.amazon.de/-/en/Heinz-Drache/dp/B014STN07I/ref=sr_1_12?dchild=1&keywords=tuch&qid=1616610258&sr=8-12","https://www.amazon.de/-/en/Lenovo-IdeaPad-Chromebook-WideView-Tablet/dp/B08CZXFKDP/?_encoding=UTF8&pd_rd_w=wofLG&pf_rd_p=07208ea4-5452-4c67-8f65-44901c0f68eb&pf_rd_r=0JJ8ZD05AEXFSZAQB3TS&pd_rd_r=8c4d6402-ff5e-4ee0-b158-13f872c81f7d&pd_rd_wg=BfT3H&ref_=pd_gw_ci_mcx_mr_hp_d","https://www.amazon.de/Window-Battery-Charger-Supply-Karcher/dp/B07WCWHXRG/ref=sr_1_4_sspa?dchild=1&keywords=tuch&qid=1616610242&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQUpJVk5aM0dLVExVJmVuY3J5cHRlZElkPUEwNzU0MTk3SThHNlk4M0xJQTNaJmVuY3J5cHRlZEFkSWQ9QTAyNzgxNzkyWkJBNlg4S0pPVkU0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==","https://www.amazon.de/-/en/Heinz-Drache/dp/B014STN07I/ref=sr_1_12?dchild=1&keywords=tuch&qid=1616610258&sr=8-12"
]

"Synchronously tracking multiple items"
# data_list = scraper.track_items(urls)
# print(data_list)

"Asynchronously tracking multiple items"
# data_list = scraper.async_track_items(urls)
# print(data_list)


end = perf_counter()
print(f"In total it took {round(end-start,2)} seconds")
