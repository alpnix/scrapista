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