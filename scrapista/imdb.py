from scrapista.helpers.helpers import get_count
from bs4 import BeautifulSoup
from time import perf_counter
import concurrent.futures
import threading as th
import datetime as dt
import requests
import re


class ImdbScraper:

    def __init__(self,base_url="https://www.imdb.com",headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}):
        self.base_url = base_url
        pass

    @property
    def top_ranked_movies(self):
        
        r = requests.get("https://www.imdb.com/chart/top/")
        soup = BeautifulSoup(r.content, "html.parser")

        table = soup.select_one(".chart.full-width tbody")

        data_list = []

        for row in table.find_all("tr"):    

            image_tag = row.find_all("td")[0].find("a")
            img_src = self.base_url + image_tag["href"]

            title_tag = row.find_all("td")[1].find("a")
            title = title_tag.get_text(" ", strip=True)
            movie_src = self.base_url + title_tag["href"]

            rating_tag = row.find_all("td")[2].find("strong")
            rating = rating_tag.get_text(" ", strip=True)

            movie_object = {
                "name": title,
                "imdb_rating": float(rating),
                "url": movie_src,
                "img_src": img_src, 
            }

            data_list.append(movie_object)


        return data_list        


    @property
    def popular_movies(self):
        """
            This method returns the most popular movies by the current date. It returns 100 movies. 
        """
        url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        table_body = soup.select_one(".chart.full-width tbody")

        data_list = []

        for row in table_body.find_all("tr"):
            try: 
                a_tag = row.find_all("td")[1].find("a")
                link = self.base_url + a_tag["href"]
            except: 
                link = None
            else: 
                try:
                    name = a_tag.get_text("",strip=True)
                except: 
                    name = None

            data_list.append({"name": name, "url": link})

        return data_list    
        

    def scrape_movies_by_genre(self,genre):
        """
            With the help of this method you will get top 50 movies and tv shows by the genre passed into the function
        """

        url = f"https://www.imdb.com/search/title/?genres={genre}"

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        movie_data = []

        movie_cards = [movie_item for movie_item in soup.select(".lister-item.mode-advanced")]
        try:
            movie_urls = [card.find("h3").find("a")["href"] for card in movie_cards]

            movie_urls = list(map(lambda x: self.base_url + x, movie_urls))
        
            movie_names = [card.find("h3").find("a").get_text("",strip=True) for card in movie_cards]
        except:
            return []
        else: 
            for i in range(len(movie_names)):
                movie_object = {"name": movie_names[i],"url": movie_urls[i]}
                if movie_object not in movie_data:
                    movie_data.append(movie_object)

        return movie_data


    def scrape_movie(self,url):
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")


        title = soup.find("h1").get_text("",strip=True)
        
        try:
            rating_count = int(soup.find(itemprop="ratingCount").get_text("", strip=True).replace(",",""))
        except:
            rating_count = "N/A"

        try:
            rating_value = float(soup.find(itemprop="ratingValue").get_text("",strip=True).replace(",",""))
        except:
            rating_value = "N/A"

        try:
            running_time = soup.select_one(".title_wrapper .subtext time").get_text("",strip=True)
        except:
            running_time = "N/A"

        def get_running_minutes(str):
            minutes = 0
            hour_pattern = "\d+h"
            minute_pattern = "\d+min"
            try: 
                hours = re.findall(hour_pattern,str)[0]
                minutes += int(hours[0]) * 60
            except Exception as e: 
                pass
            finally:
                try:
                    minutes_min = re.findall(minute_pattern,str)[0]
                    minutes += int(re.findall("\d+",minutes_min)[0])
                    return minutes
                except Exception as e: 
                    return minutes

        running_time_int = get_running_minutes(running_time)

        try:
            *genre_tags, release_tag = soup.select(".title_wrapper .subtext a")

            genres = [genre.get_text("",strip=True) for genre in genre_tags]

            release = release_tag.get_text("",strip=True)
        except:
            genres = []
            release = "N/A"

        restriction = list(soup.select_one(".title_wrapper .subtext").stripped_strings)[0]
        if len(restriction) > 4: 
            restriction = "R?"
            
        try:
            trailer = self.base_url + soup.find("a", class_=["video-modal"])["href"]
        except:
            trailer = self.base_url + "/404.html"

        try:
            image_source = soup.select_one(".poster img")["src"]
        except:
            image_source = self.base_url + "/404.html"

        try:
            metascore = float(soup.select_one(".metacriticScore span").get_text("",strip=True))
        except: 
            metascore = "N/A"

        try:
            review_tag, critic_tag = soup.select(".titleReviewBarItem.titleReviewbarItemBorder .subText a")
            review_count = get_count(review_tag.get_text("",strip=True))
            critic_count = get_count(critic_tag.get_text("",strip=True))
        except: 
            review_count = "-"
            critic_count = "-"


        cast_table = soup.select_one("table.cast_list")

        cast_list = []
        for row in cast_table.find_all("tr"):
            try: 
                cast_list.append(row.find_all("td")[1].get_text("",strip=True))
            except Exception as e:
                pass
            
        
        summary = soup.select_one(".plot_summary")


        movie_object = {
            "name": title,
            "rating_count": rating_count,
            "rating_value": rating_value,
            "running_time(min)": running_time_int,
            "genres": genres,
            "release": release,
            "restriction": restriction,
            "trailer": trailer,
            "image_source": image_source,
            "metascore": metascore,
            "review_count": review_count,
            "critic_count": critic_count,
        }

        for row in summary.find_all("div"):
            try:
                header = row.find("h4").get_text("",strip=True)[:-1]
                if header in ["Writer","Writers"]:
                    header = "writer(s)"
                elif header in ["Director","Directors"]:
                    header = "director(s)"
                elif header in ["Stars","Star"]: 
                    header = "star(s)"
                a_tags = [a_tags for a_tags in row.find_all("a",href=re.compile("^/name"))]
                data = [a_tag.get_text("",strip=True) for a_tag in a_tags]
            except Exception as e:
                pass
            else:
                movie_object[header] = data

        movie_object["cast"] = cast_list


        return movie_object
    

    def async_scrape_movies(self,urls,checkpoints=False):
        """
            This function scrapes each movie asynchronously
            instead of scraping them one by one
        """

        if checkpoints == 0 or (type(checkpoints) == bool and checkpoints == True):
            raise(Exception("checkpoint should be a positive integer"))

        all_movie_list = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for idx,url in enumerate(urls): 
                if checkpoints and idx % checkpoints == 0:
                    print("Getting data... {}/{}".format(idx,len(urls)))
                future = executor.submit(self.scrape_movie, url)
                movie_info = future.result()
                all_movie_list.append(movie_info)

        return all_movie_list


    def scrape_actors_by_bdate(self,date=""):
        """
            This method returns the actors that were born today or optionally 
            you can pass a day as an argument and get the actors that were born
            in that day. P.s. date format is month-day eg '05-24'
        """

        if not date: 
            now = dt.datetime.now()
            date = f"{now.month}-{now.day}"

        url = "https://www.imdb.com/search/name/?birth_monthday=" + date

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")

        actor_cards = [card for card in soup.select(".lister-item.mode-detail")]
        actor_tags = [card.find("h3").find("a") for card in actor_cards]

        try:
            actor_names = [tag.get_text("",strip=True) for tag in actor_tags]

        except Exception as e:
            pass


        if actor_names == []:
            raise(Exception("date format is month-day eg. 05-24"))

        

        return actor_names




# scraper = ImdbScraper()
# start = perf_counter()


"getting top 250 movies"

# movie_list = scraper.top_ranked_movies_data

# print(movie_list)

"scrape a single movie"

# movie_index = 65
# queue: 138,193,205,216,232

# movie_info = scraper.scrape_movie("https://www.imdb.com/title/tt2737304/?ref_=fn_al_tt_1/")

# print(movie_info)

"async scraping multiple movies"
"this method is 2.5 times faster than running them synchronously"

# movie_urls = [movie["movie_url"] for movie in movie_list]

# all_movie_data = scraper.async_scrape_movies(movie_urls)

# print(all_movie_data)


"getting 50 movies urls by their genres"

# horror_urls = scraper.scrape_movies_by_genre("adventure")

# print(horror_urls)


"scraping the names and the links of most popular movies"

# popular_movies = scraper.most_popular_movies_data

# print(popular_movies)


"scraping actors that were born today"

# born_today = scraper.scrape_actors_by_birthdate()

# print(born_today)




# end = perf_counter()
# print(f"In total it took {round(end-start,2)} second(s)")