from scrapista.helpers.helpers import put_year_limit,get_age,get_bdate,money_string_to_int
from bs4 import BeautifulSoup
from time import perf_counter
import concurrent.futures
import threading as th
import requests
import re
import datetime as dt



class WikiScraper:

    def __init__(self,base_url="https://en.wikipedia.org",headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"},):
        self.base_url = base_url


    @property
    def disney_movies(self):
        """
            This property returns the disney movies' urls 
            from the wikipedia page
        """
        r = requests.get("https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")
        soup = BeautifulSoup(r.content, "html.parser")

        tables = soup.select(".wikitable.sortable tbody")

        data_points = []
        data_list = []
        for table in tables: 
            rows = table.find_all("tr")
            for row in rows: 
                try: 
                    data_points.append(row.find_all("td")[1])
                except Exception as e:  
                    pass
            
        for data in data_points:
            disney_movie = {} 
            link_text = data.find("a")

            try:
                name = link_text.get_text("",strip=True)
            except Exception as e:
                pass
            else:
                disney_movie["name"] = name

            try: 
                link = link_text["href"]
            except Exception as e: 
                pass
            else: 
                if not(link[0] == "#"):
                    link = self.base_url + link 
                    disney_movie["url"] = link

            data_list.append(disney_movie)

        return data_list


    @property
    def highest_grossing_movies(self):
        """
            This function returns the urls of the highest grossing movies 
            in the world righ now.
        """

        r = requests.get("https://en.wikipedia.org/wiki/List_of_highest-grossing_films")
        soup = BeautifulSoup(r.content, "html.parser")

        table = soup.select_one(".wikitable.sortable").find("tbody")

        highest_grossing_movies = []

        for row in table.find_all("tr"):

            movie_object = {}
            link_tag = row.find_all("th")[0].find("a")

            try:
                movie_name = link_tag.get_text("",strip=True)
            except Exception as e:
                pass 
            else:
                movie_object["name"] = movie_name

            try:    
                link = link_tag["href"]
                link = self.base_url+link
            except Exception as e:
                pass
            else:
                movie_object["url"] = link

            if any(movie_object):
                highest_grossing_movies.append(movie_object)
        
        return highest_grossing_movies

    
    @property
    def most_important_people(self):
        """
            This function returns the most most important people of all
            times according to 'Times 100'.
        """

        url = "https://en.wikipedia.org/wiki/Time_100"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        gallery_boxes = soup.select(".gallerybox")
        gallery_texts = [gallery_box.select_one(".gallerytext") for gallery_box in gallery_boxes]

        people_list = []

        for text in gallery_texts:
            try:
                person_tag = text.find("a")
                name = person_tag.get_text("",strip=True)
                person_url = self.base_url + person_tag["href"]
            except Exception as e:
                pass
            else:
                person_object = {
                    "name": name,
                    "url": person_url,
                }

                people_list.append(person_object)


        return people_list


    def scrape_movie(self,url): 
        """
            You need to pass a wikipedia movie url into this function
            and it will return the info about that movie
        """

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        info_box = soup.select_one(".infobox.vevent")

        if not info_box: 
            return

        for sup in info_box.find_all("sup"): 
            sup.decompose()

        movie_info = {}

        for idx, row in enumerate(info_box.find_all("tr")):

            if idx == 0: 
                movie_info["Name"] = row.get_text()
            
            if idx == 1: 
                continue

            if row.find("ul"): 
                header = row.find("th").get_text(" ", strip=True)
                items = [li.get_text(" ",strip=True).replace("\xa0"," ") for li in row.find("ul").find_all("li")]

                movie_info[header] = items

            else: 
                try: 
                    header = row.find("th").get_text(" ", strip=True)
                    data = row.find("td").get_text(" ", strip=True)
                except Exception as e: 
                    pass
                else: 
                    movie_info[header] = data

            
        # converting running time to integers
        try: 
            minute_number_pattern = re.compile("\d+")
            minutes_unit_pattern = re.compile("\w+")

            minutes = int(re.findall(minute_number_pattern,movie_info["Running time"])[0])
            minute_unit = re.findall(minutes_unit_pattern,movie_info["Running time"])[-1]
            movie_info[f"Running time({minute_unit})"] = minutes
        except Exception as e:
            pass
        else: 
            del movie_info["Running time"]
        

        # getting the gross of the movie
        try: 
            currency, gross = money_string_to_int(movie_info,"Box office")
            movie_info[f"Gross({currency})"] = gross
        except Exception as e:
            pass
        else:
            del movie_info["Box office"]

        try: 
            currency, budget = money_string_to_int(movie_info,"Budget")
            movie_info[f"Budget({currency})"] = budget
        except Exception as e:
            pass
        else:
            del movie_info["Budget"]


        return movie_info


    def async_scrape_movies(self,urls):
        """
            This function utlizies the 'scrape_movie_info' method 
            in multiple threads 
        """

        movies_urls = []

        with concurrent.futures.ThreadPoolExecutor() as executor: 
            for url in urls:
                future = executor.submit(self.scrape_movie,url)
                data = future.result()
                movies_urls.append(data)

        return movies_urls
            
        
    def scrape_notable_movies_by_year(self,year):
        """
            This function expects a year and scrapes the notable movies that 
            were released in that year.
        """

        put_year_limit(year,1920)

        try:
            year = int(year)
        except:
            raise(Exception("Please enter a valid year"))

        url = f"https://en.wikipedia.org/wiki/{year}_in_film"
        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")

        lists = []

        for header in soup.find_all("h3"):
            ul = header.find_next("ul") 
            if ul:
                lists.append(ul)

        def scrape_movies_year_list(ul,movie_list):
            list_items = ul.find_all("li")

            for idx, item in enumerate(list_items):
                movie_object = {}
                try: 
                    movie_tag = item.find("i").find("a")
                    movie_title = movie_tag.get_text("",strip=True)
                    movie_url = movie_tag["href"]
                except Exception as e:
                    pass
                else:
                    movie_object["name"] = movie_title
                    movie_object["url"] = self.base_url + movie_url
                    if movie_object not in movie_list:
                        movie_list.append(movie_object)

        movie_list = []

        for ul in lists: 
            movie_data = scrape_movies_year_list(ul,movie_list)

        if year >= 2004: 

            table_body = soup.select_one(".wikitable.sortable tbody")

            for row in table_body.find_all("tr"):
                try: 
                    movie_tag = row.find("td").find("a")
                    movie_url = self.base_url + movie_tag["href"]
                    movie_title = movie_tag.get_text("",strip=True)
                except Exception as e:
                    pass
                else:
                    movie_object = {
                        "name": movie_title,
                        "url": movie_url
                    }
                    movie_list.append(movie_object)
                
            
        return movie_list


    def scrape_american_movies_by_year(self,year):
        """
            Scrapes the american movies by the year that was passed into
            the method.
        """

        put_year_limit(year,1920)

        url = f"https://en.wikipedia.org/wiki/List_of_American_films_of_" + str(year)
        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")
        tables = soup.select(".wikitable")
        title_index = 0

        movie_list = []

        for table in tables: 
            head = table.find("thead")
            try: 
                for idx, headers in enumerate(head.find_all("th")):
                    if headers.get_text("",strip=True):
                        title_index = idx
            except Exception as e: 
                pass

            body = table.find("tbody")

            for row in body.find_all("tr"):
                try: 
                    element = row.find_all("td")[title_index]
                    movie_tag = element.find("a")
                    movie_url = self.base_url + movie_tag["href"]
                    movie_title = movie_tag.get_text("",strip=True)
                except Exception as e: 
                    pass
                else: 
                    movie_object = {
                        "name": movie_title,
                        "url": movie_url
                    }
                    movie_list.append(movie_object)


        return movie_list


    def scrape_person(self,url="",name=""): 
        """
            This function is similar to the scraping movie info function
            but you pass in a person page's url into it and it scrapes info 
            about that person
            infobox biography vcard
        """

        if not name and not url:
            return None

        if not url: 
            url_name = "_".join(name.split())
            url = self.base_url + "/wiki/" + url_name
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        info_box = soup.select_one(".infobox.vcard")

        if not info_box: 
            print(f"{url} data not found")
            return

        # removing all the suffix and sup element from the DOM
        for sup in info_box.find_all("sup"): 
            sup.decompose()

        for br in info_box.find_all("br"):
            soup.i.string = " "
            br.replace_with(soup.i)

        for hidden in soup.find_all(style="display:none"): 
            hidden.decompose()

        try:
            info_box.find(class_="honorific-suffix").decompose()
        except Exception as e:
            pass


        person_info = {}

        if info_box.find("caption"): 
            person_info["Name"] = info_box.find("caption").get_text(" ",strip=True) 


        # scraping data
        for idx, row in enumerate(info_box.find_all("tr")):
            # getting the name of the person
            if idx == 0:
                if "Name" not in person_info.keys(): 
                    person_info["Name"] = row.get_text()

                        
            # if there is a list in the data get a list item
            if row.find("ul"): 
                try: 
                    header = row.find("th").get_text(" ", strip=True).replace("\xa0"," ")
                except Exception as e: 
                    header = "Miscellaneous"
                finally:
                    items = [li.get_text(" ",strip=True).replace("\xa0"," ").replace("\u200b","") for li in row.find("ul").find_all("li") if li.get_text(" ",strip=True)]
                if items:
                    person_info[header] = items

            # if there isn't any list scrape get items single 
            else: 
                try: 
                    header = row.find("th").string.replace("\xa0"," ")
                    data = row.find("td").get_text(" ",strip=True).replace("\xa0"," ").replace("\u200b","").replace("   "," ").replace("  ", " ").replace(" ,",",")
                except Exception as e: 
                    pass
                else: 
                    if data:
                        person_info[header] = data



        """Now let's get to convert and clean up the data a little"""


        # removing spaces in website url
        if "Website" in person_info.keys():
            person_info["Website"] = person_info["Website"].replace(" ","")

        # removing signature since it is not available
        try: 
            del person_info["Signature"]
        except Exception as e: 
            pass            

        # removing sports years team data
        try: 
            if person_info["Years"] == "Team":
                del person_info["Years"]
        except Exception as e:
            pass

        # removing awards if it is full list
        try: 
            if person_info["Awards"] == "Full list":
                del person_info["Awards"]
        except Exception as e:
            pass
                        

        try: 
            age = get_age(person_info,"Born")
        except Exception as e: 
            try:
                age = get_age("Date of birth")
                person_info["Age"] = age
            except Exception as e: 
                pass
        else: 
            person_info["Age"] = age


        try: 
            bdate = get_bdate(person_info,"Born")
        except Exception as e: 
            try: 
                person_info["Date of birth"] = person_info["Date of birth"].strip()
                if not person_info["Date of birth"]:
                    del person_info["Date of birth"]

            except Exception as e:
                pass
        else: 
            person_info["Birth Date"] = bdate
            person_info["Born"] = person_info["Born"].replace("   "," | ").replace(" ,",",").strip()

        
        # children number converted to an integer
        try: 
            children_count = re.findall("\d+",person_info["Children"])[0]
            person_info["Children"] = int(children_count)
        except Exception as e: 
            pass


        # converting spouses into a list object
        try: 
            bracket_pattern = "\(.*?\)"
            if type(person_info["Spouse(s)"]) == list:
                for idx,spouse in enumerate(person_info["Spouse(s)"]):
                    results = re.findall(bracket_pattern,spouse)
                    for result in results:
                        years_pattern = "\d+"
                        years = re.findall(years_pattern,result)
                        interval = "-".join(years)
                        present = ""
                        if len(results) == 1:
                            present = "-present"
                        person_info["Spouse(s)"][idx] = spouse.replace(result,"("+interval+present+")").replace("  ","").strip() 
                    
                spouse_list = person_info["Spouse(s)"]
            else:
                results = re.findall(bracket_pattern,person_info["Spouse(s)"])
                for idx,result in enumerate(results): 
                    years_pattern = "\d+"
                    years = re.findall(years_pattern,result)
                    interval = "-".join(years)
                    present = ""
                    if len(results) == 1:
                        present = "-present"
                    if idx==0:
                        person_info["Spouse(s)"] = person_info["Spouse(s)"].replace(result,"("+interval+")   ")
                    else:
                        person_info["Spouse(s)"] = person_info["Spouse(s)"].replace(result,"("+interval+present+")")
                
                person_info["Spouse(s)"] = person_info["Spouse(s)"].strip()
                spouse_list = person_info["Spouse(s)"].split("   ")
        except Exception as e: 
            pass
        else: 
            if spouse_list:
                person_info["Spouse(s)"] = spouse_list

        
        # cleaning the single data spouse
        try: 
            bracket_pattern = "\(.*\)"
            results = re.findall(bracket_pattern,person_info["Spouse"])
            for result in results: 
                years_pattern = "\d+"
                years = re.findall(years_pattern,result)
                interval = "-".join(years)
                present = ""
                if len(results) == 1:     
                    present = "-present"
                person_info["Spouse"] = person_info["Spouse"].replace(result,"("+interval+present+")")   
        except Exception as e: 
            pass
        else:
            person_info["Spouse"] = person_info["Spouse"].strip()


        # converting net worth integer with the currency
        try: 
            currency = person_info["Net worth"][:3]
            money_pattern = "\d+\.\d+"
            results = re.findall(money_pattern,person_info["Net worth"])
            if results: 
                if "billion" in person_info["Net worth"]: 
                    person_info["Net worth("+currency+")"] = 1_000_000_000 * float(results[0])
                elif "million" in person_info["Net worth"]: 
                    person_info["Net worth("+currency+")"] = 1_000_000 * float(results[0])
        except Exception as e:
            pass
        else: 
            del person_info["Net worth"]
        
        
        return person_info


    def async_scrape_people(self,urls="",names=""):
        """
            This function scrapes each person's info by threading. 
            It is much more efficient than running 'scrape_movie_info'
            method synchronously
        """ 

        people_info = []

        if names: 
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for name in names:
                    future = executor.submit(self.scrape_person,name=name)
                    person_info = future.result()
                    people_info.append(person_info)
        else: 
            if not urls:
                return None
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for url in urls:
                    future = executor.submit(self.scrape_person,url=url)
                    person_info = future.result()
                    people_info.append(person_info)

        return people_info


    def scrape_custom(self,url="",name=""):
        """
            This method is a vague one, you can pass in the url of an event, company, or even a place. This function will return the data on the info box if present, otherwise it will return None 
        """

        if not url and not name:
            return None

        if not url:
            url = "https://en.wikipedia.org/wiki/" + name
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        info_box = soup.select_one(".infobox")

        if not info_box: 
            return

        for sup in info_box.find_all("sup"):
            sup.decompose()

        for br in info_box.find_all("br"):
            soup.i.string = " "
            br.replace_with(soup.i)

        for hidden in soup.find_all(style="display:none"): 
            hidden.decompose()

        custom_info = {}

        caption = info_box.find("caption")
        if caption: 
            custom_info["Name"] = caption.get_text(" ",strip=True).replace("\xa0", " ")


        for idx, row in enumerate(info_box.find_all("tr")):

            if idx == 0 and "Name" not in custom_info.keys(): 
                custom_info["Name"] = row.get_text("",strip=True).replace("\xa0", " ")
            
            if row.find("td") and row.find("ul"):
                try: 
                    header = row.find("th").get_text(" ", strip=True).replace("\xa0"," ")
                    items = [li.get_text(" ",strip=True).replace("\xa0"," ") for li in row.find("ul").find_all("li")]
                except Exception as e:
                    pass
                else:
                    custom_info[header] = items

            else: 
                try: 
                    go_to_url = row.select_one(".url")
                    header = row.find("th").get_text(" ", strip=True).replace("\xa0"," ").replace("•","").strip()
                    data = row.find("td").get_text(" ", strip=True).replace("\xa0"," ").replace("\ufeff", "").replace("•","").strip()
                    if go_to_url:
                        data = go_to_url.find("a")["href"]
                        
                except Exception as e: 
                    pass
                else: 
                    custom_info[header] = data


        # converting running time to integers
        try: 
            minute_number_pattern = re.compile("\d+")
            minutes_unit_pattern = re.compile("\w+")

            minutes = int(re.findall(minute_number_pattern,custom_info["Running time"])[0])
            minute_unit = re.findall(minutes_unit_pattern,custom_info["Running time"])[-1]
            movie_info[f"Running time({minute_unit})"] = minutes
        except Exception as e:
            pass
        else: 
            del custom_info["Running time"]
        

        # getting the gross of the movie
        try: 
            currency, gross = money_string_to_int(custom_info,"Box office")
            movie_info[f"Gross({currency})"] = gross
        except Exception as e:
            pass
        else:
            del custom_info["Box office"]

        try: 
            currency, budget = money_string_to_int(custom_info,"Budget")
            movie_info[f"Budget({currency})"] = budget
        except Exception as e:
            pass
        else:
            del custom_info["Budget"]

        if len(custom_info) < 2:
            return

        return custom_info



# ws = WikiScraper()
# start = perf_counter()

"disney movies property"
# print(ws.disney_movies_urls)

"scraping a movie info"

# person_info = ws.scrape_movie_info("https://en.wikipedia.org/wiki/Finding_Dory")

# print(person_info)

"scraping a person's info"

# data = ws.scrape_person_info(name="Jeff Bezos")
# data = ws.scrape_person_info(url="https://www.wikipedia.com/wiki/Elon_Musk")

# print(data)

"scraping the cast of a movie"

# cast = ws.scrape_movie_cast("https://en.wikipedia.org/wiki/Avengers:_Endgame")

# print(cast)

"scraping info of multiple people"

# people = [
#     "Elon Musk","Chris Evans","Gal Gadot","Jeff Bezos","Lionel Messi","Cristiano Ronaldo","Elon Musk","Chris Evans","Gal Gadot","Jeff Bezos","Lionel Messi","Cristiano Ronaldo","Elon Musk","Chris Evans","Gal Gadot","Jeff Bezos","Lionel Messi","Cristiano Ronaldo"
# ]


"scraping people info synchronously"

# people_info = []
# for person in people: 
#     person_info = ws.scrape_person_info(name=person)
#     people_info.append(person_info)

# print(people_info)
# print(len(people_info))



"scraping people info asynchronously"

# people_info = ws.async_scrape_person_info(names=people)

# print(people_info)
# print(len(people_info))


"highest grossing movies urls property"

# highest_grossing_movies = ws.highest_grossing_movies_urls

# print(highest_grossing_movies)


"requesting multiple data synchronously"

# all_movie_data = []

# movies = ws.highest_grossing_movies_urls

# for movie in movies: 
#     all_movie_data.append(ws.scrape_movie_info(movie))

# print(all_movie_data)
# print(len(all_movie_data))



"async movie info requests"


# all_movie_data = ws.async_scrape_movies_info(ws.highest_grossing_movies_urls)

# print(all_movie_data)
# print(len(all_movie_data))


"scraping notable movies by year they were released"

# for year in range(1920,2021):
#     with concurrent.futures.ThreadPoolExecutor() as executor: 
#         future = executor.submit(ws.scrape_notable_movies_by_year,year)
#         movie_list = future.result()
#         # print(movie_list)
#         print(f"{year}: {len(movie_list)}")


"scraping american movies by year"

# movie_data_list = ws.scrape_american_movies_by_year(1920)

# print(movie_data_list)
# print(len(movie_data_list))


"getting most important people"

# people = ws.most_important_people

# print(people)
# print(len(people))



# end = perf_counter()
# print(f"In total it took {round(end-start,2)} second(s)")

