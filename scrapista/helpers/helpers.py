import requests
from bs4 import BeautifulSoup
import re
import datetime as dt

#  converting box office and budget into integer values that we got from wikipedia info box
def money_string_to_int(movie_info,key):
    
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


# this function raises exception when an invalid year is passed into a function as an argument
def put_year_limit(year,start,end=dt.datetime.now().year):
        
    if year > end or year < start:
        raise(BaseException(f"The year passed in should be between {start} and current year"))


# extracting the age from the 'born' key
# person_info is a dicionary and we will pass in the key we want to modify
def get_age(person_info,key):
    age_pattern = "\(age \d+\)"
    results = re.findall(age_pattern,person_info[key])
    result = results[0]
    person_info[key] = person_info[key].replace(result,"")
    if re.findall("^| ",person_info[key]):
        person_info[key] = person_info[key].replace("| ","")
    age = int(re.findall("\d+",result)[0])
    return age


# creating a datetime object of the person's birth time
# person_info is a dicionary and we will pass in the key we want to modify
def get_bdate(person_info,key):
    date_pattern = "\w+ \d+, \d+"
    result = re.findall(date_pattern,person_info[key])[0]
    person_info[key] = person_info[key].replace(result,"")
    bdate = dt.datetime.strptime(result,"%B %d, %Y")
    return bdate


# this function takes the review or critic count of a movie as a string from imdb
# then it converts eg. '7,805' into 7805 and returns the found int value
def get_count(str):
    str = str.replace(",","")
    results = re.findall("\d+", str)
    if len(results) == 1: 
        return int(results[0])
    else:
        return results



# this function scrapes and returns a word object 
# you have to pass the word and the headers in json formot user-agent key is required
def get_word_info(word, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"}):
    
    r = requests.get("https://dictionary.cambridge.org/dictionary/english/"+word, headers=headers)

    soup = BeautifulSoup(r.content, "html.parser")

    word_info = {}
    word_info["word"] = word
    try:
        form = soup.select_one(".pos.dpos").get_text(" ",strip=True)
    except:
        form = None
    else:
        word_info["form"] = form 
    try:
        level = soup.select_one(".epp-xref.dxref").get_text(" ",strip=True)
    except:
        level = None
    else:
        word_info["level"] = level
    try:
        definition = soup.select_one(".def.ddef_d.db").get_text(" ",strip=True)
    except:
        definition = None
    else:
        word_info["definition"] = definition

    try:
        sentence_example_tags = soup.select(".eg.deg")
        sentence_examples = [sentence_example_tag.get_text(" ",strip=True) for sentence_example_tag in sentence_example_tags]
    except:
        sentence_examples = []
    else:
        word_info["sentence_examples"] = sentence_examples

    if not all(word_info.values()):
        return "No such word exists in the database"

    return word_info


def get_currency_ratio(current,target):
    r = requests.get(f"https://www.x-rates.com/calculator/?from={current}&to={target}&amount=1")

    soup = BeautifulSoup(r.content, "html.parser")

    container = soup.select_one(".ccOutputRslt")
    for span in container.find_all("span"):
        span.decompose()
    
    currency_ratio = float(container.get_text("",strip=True))

    return currency_ratio

