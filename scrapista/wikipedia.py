from bs4 import BeautifulSoup
from time import perf_counter
import concurrent.futures
import threading as th
import requests
import re
import datetime as dt


class WikiScraper:

    def __init__(self,base_url="https://en.wikipedia.org"):
        self.base_url = base_url
        

    @property
    def disney_movies_urls(self):
        """
            This property returns the disney movies' urls 
            from the wikipedia page
        """
        r = requests.get("https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")
        soup = BeautifulSoup(r.content, "html.parser")

        tables = soup.select(".wikitable.sortable tbody")

        data_points = []
        links = []
        for table in tables: 
            rows = table.find_all("tr")
            for row in rows: 
                try: 
                    data_points.append(row.find_all("td")[1])
                except Exception as e:  
                    pass
            
        for data in data_points: 
            try: 
                link = data.find("a")["href"]
            except Exception as e: 
                pass
            else: 
                if not(link[0] == "#"):
                    link = self.base_url + link 
                    links.append(link)

        return links

    @property
    def highest_grossing_movies_urls(self):
        """
            This function returns the urls of the highest grossing movies 
            in the world righ now.
        """

        r = requests.get("https://en.wikipedia.org/wiki/List_of_highest-grossing_films")
        soup = BeautifulSoup(r.content, "html.parser")

        table = soup.select_one(".wikitable.sortable").find("tbody")

        highest_grossing_urls = []

        for row in table.find_all("tr"):
            try:
                link_tag = row.find_all("th")[0].find("a")
                link = link_tag["href"]
            except Exception as e:
                print(e)
                pass
            else:
                highest_grossing_urls.append(self.base_url+link)
        
        return highest_grossing_urls

    
    def scrape_movie_info(self,url): 
        """
            You need to pass a wikipedia movie url into this function
            and it will return the info about that movie
        """

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        info_box = soup.select_one(".infobox.vevent")


        for sup in info_box.find_all("sup"): 
            sup.decompose()

        movie_info = {}

        for idx, row in enumerate(info_box.find_all("tr")):

            if idx == 0: 
                movie_info["title"] = row.get_text()
            
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
            print(e)
            pass
        else: 
            del movie_info["Running time"]
        

        # converting box office and budget into integer values
        def money_string_to_int(key):

            currency = movie_info[key][0]
            movie_info[key] = movie_info[key].replace(currency,"")
            movie_info[key] = movie_info[key].strip()

            money_pattern = "(\d+-\d+|\d+\.\d+|\d+)"
            money_result = re.findall(money_pattern,movie_info[key])
            if not money_result:
                money_result = re.findall("\d+", movie_info[key])

            scale_pattern = "\w+"
            scale_result = re.findall(scale_pattern, movie_info[key])[-1]

            if scale_result == "billion": 
                scale = 1_000_000_00
            elif scale_result == "million": 
                scale = 1_000_000

            movies_monies = money_result

            for idx, money in enumerate(movies_monies):
                money = float(money)
                movies_monies[idx] = money * scale

            if len(movies_monies) == 1: 
                movies_monies = movies_monies[0]

            return (currency, movies_monies)


        # getting the gross of the movie
        try: 
            currency, gross = money_string_to_int("Box office")
            movie_info[f"Gross({currency})"] = gross
        except Exception as e:
            print(e)
            pass
        else:
            del movie_info["Box office"]

        try: 
            currency, budget = money_string_to_int("Budget")
            movie_info[f"Budget({currency})"] = budget
        except Exception as e:
            print(e)
            pass
        else:
            del movie_info["Budget"]


        return movie_info


    def async_scrape_movies_info(self,urls):
        """
            This function utlizies the 'scrape_movie_info' method 
            in multiple threads 
        """

        movies_urls = []

        with concurrent.futures.ThreadPoolExecutor() as executor: 
            for url in urls:
                future = executor.submit(self.scrape_movie_info,url)
                data = future.result()
                movies_urls.append(data)

        return movies_urls
            

    def scrape_person_info(self,url="",name=""): 
        """
            This function is similar to the scraping movie info function
            but you pass in a person page's url into it and it scrapes info 
            about that person
            infobox biography vcard
        """
        if not url: 
            url_name = "_".join(name.split())
            url = self.base_url + "/wiki/" + url_name
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        info_box = soup.select_one(".infobox.vcard")

        if not info_box: 
            print(f"{url} table not found")
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
                    items = [li.get_text(" ",strip=True).replace("\xa0"," ").replace("\u200b","") for li in row.find("ul").find_all("li")]

                person_info[header] = items

            # if there isn't any list scrape get items single 
            else: 
                try: 
                    header = row.find("th").string.replace("\xa0"," ")
                    data = row.find("td").get_text(" ",strip=True).replace("\xa0"," ").replace("\u200b","").replace("   "," ").replace("  ", " ").replace(" ,",",")
                except Exception as e: 
                    pass
                else: 
                    person_info[header] = data

        # removing spaces in website url
        if "Website" in person_info.keys():
            person_info["Website"] = person_info["Website"].replace(" ","")

        # removing signature since it is not available
        try: 
            del person_info["Signature"]
        except Exception as e: 
            print(e)
            pass            

        # removing sports years team data
        try: 
            if person_info["Years"] == "Team":
                del person_info["Years"]
        except Exception as e:
            print(e)
            pass

        # removing awards if it is full list
        try: 
            if person_info["Awards"] == "Full list":
                del person_info["Awards"]
        except Exception as e:
            print(e)
            pass
                   

        # extracting the age from the 'born' key
        def get_age(key):
            age_pattern = "\(age \d+\)"
            results = re.findall(age_pattern,person_info[key])
            result = results[0]
            person_info[key] = person_info[key].replace(result,"")
            if re.findall("^| ",person_info[key]):
                person_info[key] = person_info[key].replace("| ","")
            age = int(re.findall("\d+",result)[0])
            return age

        try: 
            age = get_age("Born")
        except Exception as e: 
            print(e)
            try:
                age = get_age("Date of birth")
                person_info["Age"] = age
            except Exception as e: 
                print(e)
                pass
        else: 
            person_info["Age"] = age


        # creating a datetime object of the person's birth time
        def get_bdate(key):
            date_pattern = "\w+ \d+, \d+"
            result = re.findall(date_pattern,person_info[key])[0]
            person_info[key] = person_info[key].replace(result,"")
            bdate = dt.datetime.strptime(result,"%B %d, %Y")
            return bdate

        try: 
            bdate = get_bdate("Born")
        except Exception as e: 
            print("born2 |",e)
            try: 
                person_info["Date of birth"] = person_info["Date of birth"].strip()
                if not person_info["Date of birth"]:
                    del person_info["Date of birth"]

            except Exception as e:
                print("born2.2 |",e)
                pass
        else: 
            person_info["Birth Date"] = bdate
            person_info["Born"] = person_info["Born"].replace("   "," | ").replace(" ,",",").strip()

        
        # children number converted to an integer
        try: 
            person_info["Children"] = int(person_info["Children"])
        except Exception as e: 
            print("children |",e)
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
            print("spouses |",e)
            pass
        else: 
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
            print("spouse |",e)
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
            print("net worth |",e)
            pass
        else: 
            del person_info["Net worth"]
        
        
        return person_info


    def async_scrape_person_info(self,urls="",names=""):
        """
            This function scrapes each person's info by threading. 
            It is much more efficient than running 'scrape_movie_info'
            method synchronously
        """

        people_info = []

        if names: 
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for name in names:
                    future = executor.submit(self.scrape_person_info,name=name)
                    person_info = future.result()
                    people_info.append(person_info)
        else: 
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for url in urls:
                    future = executor.submit(self.scrape_person_info,url=url)
                    person_info = future.result()
                    people_info.append(person_info)

        return people_info


    def scrape_movie_cast(self,url):
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        cast_header = soup.find(id="Cast")

        cast_list = cast_header.find_next("ul")

        cast_items = [li.find("a") for li in cast_list.find_all("li")]
        cast_urls = [self.base_url+a["href"] for a in cast_items]
        
        return cast_urls


ws = WikiScraper()
start = perf_counter()

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

people = [
    "Elon Musk","Chris Evans","Gal Gadot","Jeff Bezos","Lionel Messi","Cristiano Ronaldo","Elon Musk","Chris Evans","Gal Gadot","Jeff Bezos","Lionel Messi","Cristiano Ronaldo","Elon Musk","Chris Evans","Gal Gadot","Jeff Bezos","Lionel Messi","Cristiano Ronaldo"
]


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



end = perf_counter()
print(f"In total it took {round(end-start,2)} second(s)")
