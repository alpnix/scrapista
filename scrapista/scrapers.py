from bs4 import BeautifulSoup
import numpy as np
import requests

class AmazonScraper:
    def __init__(self,headers,base_url="https://www.amazon.de"):
        self.base_url = base_url
        self.headers = headers
        
    def scrape_keyword(self,keyword): 
        url_keyword_addition = f"/s?k={keyword}&ref=nb_sb_noss"
        r = requests.get(self.base_url+url_keyword_addition,headers=self.headers)
        soup = BeautifulSoup(r.content, "html.parser")
        groups = soup.select(".a-section.a-spacing-medium")
        data_list = []
        for group in groups: 

            name_tag = group.select_one(".a-link-normal.a-text-normal")
            image = group.select_one(".s-image")
            stars = group.select_one(".a-icon-alt")
            price = group.select_one(".a-price-whole")

            try: 
                price_amount = price.get_text(strip=True).replace(",",".")
                price_amount = float(price_amount)
            except: 
                price_amount = np.nan

            try: 
                source = image["src"]
            except: 
                source = np.nan

            try: 
                star_amount = stars.get_text(strip=True)[:3].replace(",",".")
                star_amount = float(star_amount)
            except: 
                star_amount = np.nan

            try:
                product_name = name_tag.get_text("|",strip=True)
            except: 
                product_name = np.nan

            try: 
                product_url = self.base_url + name_tag["href"]
            except: 
                product_url = np.nan

            laptop_object = {
                "img_source": source,
                "stars": star_amount,
                "price": price_amount,
                "name": product_name,
                "url": product_url
            }
            
            data_list.append(laptop_object)
    
        return data_list[:-1]
