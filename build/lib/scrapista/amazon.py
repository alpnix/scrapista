from bs4 import BeautifulSoup
from time import perf_counter
import concurrent.futures
import threading as th
import requests



class AmazonScraper:
    """
        This class has some methods that scrape the amazon website 
        and return you some data. 
    """
    def __init__(self,headers,base_url="https://www.amazon.com",params={"language": "en", "currency": "USD"}):
        self.base_url = base_url
        self.headers = headers
        self.params = params
        self.tracked = []
        
        r = requests.get(f"https://www.x-rates.com/calculator/?from=EUR&to={params['currency']}&amount=1")
        soup = BeautifulSoup(r.content, "html.parser")
        
        container = soup.select_one(".ccOutputRslt")
        for span in container.find_all("span"):
            span.decompose()

        self._currency_ratio = float(container.get_text("",strip=True))

    
    def scrape_keyword(self,keyword,data_list=[]):

        """
            Scrape all the instances of a single element
        """

        url_keyword_addition = f"/s?k={keyword}&ref=nb_sb_noss_2"
        url = self.base_url+url_keyword_addition
        url = url.replace("https://www.amazon.com","https://www.amazon.de")
        r = requests.get(url,headers=self.headers,params=self.params)


        if not r.ok:
            raise BaseException("unsuccessful request to: " + r.url)

        soup = BeautifulSoup(r.content, "html.parser")
        groups = soup.select(".s-result-item")

        print(r.url)

        for group in groups: 

            name_tag = group.select_one(".a-link-normal.a-text-normal")
            image = group.select_one(".s-image")
            stars = group.select_one(".a-icon-alt")
            price = group.select_one(".a-price-whole")

            try: 
                price_amount = price.get_text(strip=True).replace(",","")
                price_amount = round(float(price_amount) * self._currency_ratio,2)
            except: 
                continue

            try: 
                source = image["src"]
                source = source.replace("www.amazon.de","www.amazon.com")
            except: 
                source = "N/A"

            try: 
                star_amount = stars.get_text(strip=True)[:3].replace(",",".")
                star_amount = float(star_amount)
            except: 
                star_amount = "N/A"

            try:
                product_name = name_tag.get_text("|",strip=True)
            except: 
                product_name = "N/A"

            try: 
                product_url = self.base_url + name_tag["href"]
            except: 
                if product_name == "N/A":
                    continue
                product_url = "N/A"

            item_info = {
                "name": product_name,
                f"price({self.params['currency']})": price_amount,
                "stars(5)": star_amount,
                "url": product_url,
                "img_source": source,
            }
            
            data_list.append(item_info)

        
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
        

        data_list = list(filter(lambda x: any(x.values()), data_list)) 

        return data_list


    def async_scrape_keywords(self,keywords,data_list=[]): 

        """
            This function is the exact same of the scrape_keyword function
            but this one runs with multiprocessing therefore it's much faster
        """

        if type(keywords) != list: 
            raise BaseException("A list type is expected for 'keywords' argument")
        
        # alternative of ThreadExecutorPool
        """
        threads = [th.Thread(target=self.scrape_keyword,args=(keyword,data_list)) for keyword in keywords]

        for t in threads: 
            t.start()
        
        for t in threads: 
            t.join()
        """

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for keyword in keywords: 
                future = executor.submit(self.scrape_keyword,keyword,data_list)


        data_list = list(filter(lambda x: any(x.values()), data_list)) 

        return data_list

    
    def track_item(self, url): 

        """
            You will pass a list of urls and an interval, it returns the current price and state of all those items
        """

        url = url.replace("https://www.amazon.com","https://www.amazon.de")
        r = requests.get(url,headers=self.headers,params=self.params)

        if not r.ok:
            raise BaseException("unsuccessful request to: " + r.url)
            
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
            price = round(float(price) * self._currency_ratio,2)          
        except Exception as e: 
            price = None


        item_object = {
            "title": title,
            "stars(out of 5)": stars,
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




# params = {
#     "language": "en", 
#     "currency": "USD"
# }

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
# }


# start = perf_counter()
# scraper = AmazonScraper(headers,params=params)

"Sync Single keyword"

# data = scraper.scrape_keyword("airpod")

# print(data)

"Scraping multiple keywords"
# items = [
#     "pencil","cardboard","racket","paddle","book","headphone","water bottle","usb charger","book shelf","paper","markers","pencilcase","notebook","calculator"
# ]

"Sync scraping keywords"

# data_list = scraper.scrape_keywords(items)
# print(len(data_list))

"Async scraping keywords"

# data_list = scraper.async_scrape_keywords(items)
# print(len(data_list))



"Tracking single item"

# airpod = scraper.track_item("https://www.amazon.de/-/en/Lenovo-IdeaPad-Chromebook-WideView-Tablet/dp/B08CZXFKDP/?_encoding=UTF8&pd_rd_w=wofLG&pf_rd_p=07208ea4-5452-4c67-8f65-44901c0f68eb&pf_rd_r=0JJ8ZD05AEXFSZAQB3TS&pd_rd_r=8c4d6402-ff5e-4ee0-b158-13f872c81f7d&pd_rd_wg=BfT3H&ref_=pd_gw_ci_mcx_mr_hp_d")

# print(airpod)

"Tracking multiple items"

# urls = [
#     "https://www.amazon.de/-/en/Lenovo-IdeaPad-Chromebook-WideView-Tablet/dp/B08CZXFKDP/?_encoding=UTF8&pd_rd_w=wofLG&pf_rd_p=07208ea4-5452-4c67-8f65-44901c0f68eb&pf_rd_r=0JJ8ZD05AEXFSZAQB3TS&pd_rd_r=8c4d6402-ff5e-4ee0-b158-13f872c81f7d&pd_rd_wg=BfT3H&ref_=pd_gw_ci_mcx_mr_hp_d","https://www.amazon.de/Window-Battery-Charger-Supply-Karcher/dp/B07WCWHXRG/ref=sr_1_4_sspa?dchild=1&keywords=tuch&qid=1616610242&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQUpJVk5aM0dLVExVJmVuY3J5cHRlZElkPUEwNzU0MTk3SThHNlk4M0xJQTNaJmVuY3J5cHRlZEFkSWQ9QTAyNzgxNzkyWkJBNlg4S0pPVkU0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==","https://www.amazon.de/-/en/Heinz-Drache/dp/B014STN07I/ref=sr_1_12?dchild=1&keywords=tuch&qid=1616610258&sr=8-12","https://www.amazon.de/-/en/Lenovo-IdeaPad-Chromebook-WideView-Tablet/dp/B08CZXFKDP/?_encoding=UTF8&pd_rd_w=wofLG&pf_rd_p=07208ea4-5452-4c67-8f65-44901c0f68eb&pf_rd_r=0JJ8ZD05AEXFSZAQB3TS&pd_rd_r=8c4d6402-ff5e-4ee0-b158-13f872c81f7d&pd_rd_wg=BfT3H&ref_=pd_gw_ci_mcx_mr_hp_d","https://www.amazon.de/Window-Battery-Charger-Supply-Karcher/dp/B07WCWHXRG/ref=sr_1_4_sspa?dchild=1&keywords=tuch&qid=1616610242&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQUpJVk5aM0dLVExVJmVuY3J5cHRlZElkPUEwNzU0MTk3SThHNlk4M0xJQTNaJmVuY3J5cHRlZEFkSWQ9QTAyNzgxNzkyWkJBNlg4S0pPVkU0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==","https://www.amazon.de/-/en/Heinz-Drache/dp/B014STN07I/ref=sr_1_12?dchild=1&keywords=tuch&qid=1616610258&sr=8-12","https://www.amazon.de/-/en/Lenovo-IdeaPad-Chromebook-WideView-Tablet/dp/B08CZXFKDP/?_encoding=UTF8&pd_rd_w=wofLG&pf_rd_p=07208ea4-5452-4c67-8f65-44901c0f68eb&pf_rd_r=0JJ8ZD05AEXFSZAQB3TS&pd_rd_r=8c4d6402-ff5e-4ee0-b158-13f872c81f7d&pd_rd_wg=BfT3H&ref_=pd_gw_ci_mcx_mr_hp_d","https://www.amazon.de/Window-Battery-Charger-Supply-Karcher/dp/B07WCWHXRG/ref=sr_1_4_sspa?dchild=1&keywords=tuch&qid=1616610242&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQUpJVk5aM0dLVExVJmVuY3J5cHRlZElkPUEwNzU0MTk3SThHNlk4M0xJQTNaJmVuY3J5cHRlZEFkSWQ9QTAyNzgxNzkyWkJBNlg4S0pPVkU0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==","https://www.amazon.de/-/en/Heinz-Drache/dp/B014STN07I/ref=sr_1_12?dchild=1&keywords=tuch&qid=1616610258&sr=8-12","https://www.amazon.de/-/en/Lenovo-IdeaPad-Chromebook-WideView-Tablet/dp/B08CZXFKDP/?_encoding=UTF8&pd_rd_w=wofLG&pf_rd_p=07208ea4-5452-4c67-8f65-44901c0f68eb&pf_rd_r=0JJ8ZD05AEXFSZAQB3TS&pd_rd_r=8c4d6402-ff5e-4ee0-b158-13f872c81f7d&pd_rd_wg=BfT3H&ref_=pd_gw_ci_mcx_mr_hp_d","https://www.amazon.de/Window-Battery-Charger-Supply-Karcher/dp/B07WCWHXRG/ref=sr_1_4_sspa?dchild=1&keywords=tuch&qid=1616610242&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQUpJVk5aM0dLVExVJmVuY3J5cHRlZElkPUEwNzU0MTk3SThHNlk4M0xJQTNaJmVuY3J5cHRlZEFkSWQ9QTAyNzgxNzkyWkJBNlg4S0pPVkU0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==","https://www.amazon.de/-/en/Heinz-Drache/dp/B014STN07I/ref=sr_1_12?dchild=1&keywords=tuch&qid=1616610258&sr=8-12"
# ]

"Synchronously tracking multiple items"
# data_list = scraper.track_items(urls)
# print(data_list)

"Asynchronously tracking multiple items"
# data_list = scraper.async_track_items(urls)
# print(data_list)


"display tracked items"

# print(scraper.tracked)


# end = perf_counter()
# print(f"In total it took {end-start:.2f} seconds")
