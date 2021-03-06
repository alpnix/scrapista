from bs4 import BeautifulSoup
from time import perf_counter
import concurrent.futures
import threading as th
import requests

def clean_string(string):
    string = string.replace("\n","")
    string = string.replace("\t","")
    string = string.strip()
    return string


class AmazonScraper:
    """
        This class has some methods that scrape the amazon website 
        and return you some data. 
    """
    def __init__(self,base_url="https://www.amazon.com",headers={"upgrade-insecure-requests": "1", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"},params={"language": "en", "currency": "USD"}):
        self.base_url = base_url
        self.headers = headers
        self.params = params
        self.tracked = []
    
    
    def scrape_keyword(self,keyword,data_list=[]):
        """
            This method will return every product on amazon related to the 
            keyword you pass into the method
        """

        keyword_addition = keyword.replace(" ","+")
        url_keyword_addition = f"/s?k={keyword_addition}&ref=nb_sb_noss_2"
        url = self.base_url + url_keyword_addition

        try:
            r = requests.get(url,headers=self.headers,params=self.params)
        except:
            return "Connection Error"


        soup = BeautifulSoup(r.content, "html.parser")
        groups = soup.select(".s-result-item")

        for group in groups: 
            
            name_tag = group.select_one(".a-link-normal.a-text-normal")
            image = group.select_one(".s-image")
            stars = group.select_one(".a-icon-alt")
            price = group.select_one(".a-price-whole")
            price_symbol_tag = group.select_one(".a-price-symbol")

            try: 
                price_amount = price.get_text(strip=True).replace(",","")
                price_amount = float(price_amount)
            except: 
                continue

            try:
                price_symbol = price_symbol_tag.get_text("",strip=True)
                price_symbol = "(" + price_symbol + ")" 
            except:
                price_symbol = ""

            try: 
                source = image["src"]
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
                "price"+price_symbol: price_amount,
                "stars(5)": star_amount,
                "url": product_url,
                "img_src": source,
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
            raise Exception("A list type is expected for 'keywords' argument")


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
            raise Exception("A list type is expected for 'keywords' argument")
        
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

    
    def scrape_item(self, url): 
        """
            Scrape all the instances of a single element
        """

        try:
            r = requests.get(url,headers=self.headers,params=self.params)
        except:
            return "Connection Error"

            
        soup = BeautifulSoup(r.content, "html.parser")

        title_tag = soup.select_one("h1#title")
        stars_tag = soup.select_one(".a-icon.a-icon-star")
        price_tag = soup.find(id="price_inside_buybox")

        if not price_tag: 
            price_tag = soup.find(id="priceblock_dealprice")

        try: 
            title = title_tag.get_text("|",strip=True)
        except Exception as e: 
            title = None

        try: 
            stars = stars_tag.get_text("|",strip=True)[:3].replace(",",".")
            stars = float(stars)
        except Exception as e: 
            stars = "N/A"
        
        try: 
            price = price_tag.get_text("|",strip=True)
        except Exception as e: 
            price = "N/A"

        try:
            price_int = price.replace(",","")[1:]
            price_int = float(price_int)
        except:
            "N/A"
        else:
            price = price_int

        try:
            currency = self.params["currency"]
            currency_addition = "(" + currency + ")"
        except:
            currency_addition = ""
        
        
        item_object = {
            "title": title,
            "stars(out of 5)": stars,
            "price"+currency_addition: price,
        }

        rows = soup.select("table.a-normal tr")

        for row in rows:
            try: 
                key = clean_string(row.select("td")[0].get_text())
                value = clean_string(row.select("td")[1].get_text())

                if not bool(key) or not bool(value): 
                    continue
            except:
                pass
            else: 
                item_object[key] = value

        try:
            note_list = soup.select_one("ul.a-unordered-list.a-vertical.a-spacing-mini")
            note = note_list.get_text("").replace("\n","").strip().replace("\xa0","")
            note_items = note_list.select("li")
            notes = []
            for item in note_items:
                note = item.get_text("").replace("\n","").strip().replace("\xa0","")
                while "  " in note:
                    note = note.replace("  ", " ")
            
                notes.append(note)

            item_object["about"] = notes
        except:
            pass

        if url not in self.tracked: 
            self.tracked.append(url)


        return item_object


    def scrape_items(self,urls,data_list=[]):
        """
            Track all the items that are passed into the function as 
            list type. 
        """

        if type(urls) != list: 
            raise Exception("A list type is expected for 'urls' argument")

        for url in urls: 

            data = self.scrape_item(url)
            data_list.append(data)

        data_list = list(filter(lambda x: any(x.values()), data_list)) 

        return data_list


    def async_scrape_items(self,urls,data_list=[]):
        """
            This function is the asynchronous version of the 
            AmazonScraper.track_items function 
        """

        if type(urls) != list: 
            raise Exception("A list type is expected for 'urls' argument")


        with concurrent.futures.ThreadPoolExecutor() as executor:
            for url in urls: 
                future = executor.submit(self.scrape_item,url)
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

# scraper = AmazonScraper()
# print(scraper.track_item("https://www.amazon.de/-/en/23-8-inch-Full-all-one/dp/B089PJ5S5B/ref=sr_1_3?currency=USD&dchild=1&keywords=computer&qid=1617312928&sr=8-3"))


if __name__ == "__main__":
    pass