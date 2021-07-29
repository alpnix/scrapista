.. _wikiscraper:

Wikipedia Scraper
===================

For taking a look at Wikipedia's robots.txt visit `here <https://www.wikipedia.com/robots.txt>`_.

Creating an WikiScraper Object
-------------------------------

While creating an instance of ``WikiScraper`` you can pass in optional ``headers`` argument for passing in your user agent and other headers. If you don't have any specific preferences, default user-agent should be fine for now::

    from scrapista.wikipedia import WikiScraper
    
    ws = WikiScraper()

And now let's take a look at the available attributes in the object we've just created::

    print(dir(ws))
    # ['__class__', '__delattr__', ... 'async_scrape_movies', 'async_scrape_people', 
    # 'base_url', 'disney_movies', 'highest_grossing_movies', 'most_important_people', 
    # 'scrape_american_movies_by_year', 'scrape_custom', 'scrape_movie', 
    # 'scrape_notable_movies_by_year', 'scrape_person']


disney_movies
--------------

This property returns a list of dictionaries containing url and name of each disney movie::

    disney_movies = ws.disney_movies

    print(disney_movies)
    # [{'name': 'Academy Award Review of Walt Disney Cartoons', 'url': 'https://en.
    # wikipedia.org/wiki/Academy_Award_Review_of_Walt_Disney_Cartoons'},  ... {'name': 
    # 'Better Nate Than Never', 'url': 'https://en.wikipedia.org/wiki/Tim_Federle#Fiction'}]


highest_grossing_movies
------------------------

This property returns a list of dictionaries containing url and name of the highest grossing movies of all time::

    highest_grossing_movies = ws.highest_grossing_movies

    print(highest_grossing_movies)
    # [{'name': 'Avatar', 'url': 'https://en.wikipedia.org/wiki/Avatar_(2009_film)'}, 
    # {'name': 'Avengers: Endgame', 'url': 'https://en.wikipedia.org/wiki/
    # Avengers:_Endgame'}, ... {'name': 'The Lion King', 'url': 'https://en.wikipedia.
    # org/wiki/The_Lion_King'}]


most_important_people
----------------------

This property returns the list of the people who has the most appearances in the most influential people list published by Time 100, each person's dictionary contains the name and their wikipedia URL::

    most_important_people = ws.most_important_people

    print(most_important_people)
    # [{'name': 'Barack Obama', 'url': 'https://en.wikipedia.org/wiki/Barack_Obama'}, 
    # {'name': 'Xi Jinping', 'url': 'https://en.wikipedia.org/wiki/Xi_Jinping'}, ... 
    # {'name': 'Taylor Swift', 'url': 'https://en.wikipedia.org/wiki/Taylor_Swift'}]


scrape_movie
-------------

There are multiple ways of scraping movie data in scrapista. One of the most obvious ways is using ``ImdbScraper`` by passing in the relevant IMDb URL. With this ``scrape_movie`` method you are expected to pass in Wikipedia URL of the movie::

    inception_url = "https://en.wikipedia.org/wiki/Inception"

    inception_data = ws.scrape_movie(inception_url)

    print(inception_data)
    # {'Name': 'Inception', 'Directed by': 'Christopher Nolan', 'Written by': 
    # 'Christopher Nolan', 'Produced by': ['Emma Thomas', 'Christopher Nolan'], 
    # 'Starring': ['Leonardo DiCaprio', 'Ken Watanabe', 'Joseph Gordon-Levitt', 'Marion 
    # Cotillard', 'Elliot Page', 'Tom Hardy', 'Cillian Murphy', 'Tom Berenger', 
    # 'Michael Caine'], 'Cinematography': 'Wally Pfister', 'Edited by': 'Lee Smith', 
    # 'Music by': 'Hans Zimmer', 'Production companies': ['Legendary Pictures', 
    # 'Syncopy'], 'Distributed by': 'Warner Bros. Pictures', 'Release date': ['July 8, 
    # 2010 ( 2010-07-08 ) ( Odeon Leicester Square )', 'July 16, 2010 ( 2010-07-16 ) 
    # (United States and United Kingdom)'], 'Countries': ['United States', 'United 
    # Kingdom'], 'Language': 'English', 'Running time(minutes)': 148, 'Gross($)': 
    # 836800000.0, 'Budget($)': 160000000.0}


async_scrape_movies
--------------------

This method is similar to the previous one. The difference is that, this method expects a list of URLs and this way of scraping multiple movies is much faster than using the previous method in a loop. This is because this method uses multiple threads for each page::

    # Let's scrape disney movie URLs instead of getting each url manually
    movie_url_list = [movie["url"] for movie in ws.disney_movies[:3]]

    movies_data = ws.async_scrape_movies(movie_url_list)

    print(movies_data)
    # [{{'Name': 'Snow White and the Seven Dwarfs', 'Directed by': ['David Hand'], 
    # 'Written by': ['Ted Sears', 'Richard Creedon', 'Otto Englander', 'Dick Rickard', 
    # 'Earl Hurd', 'Merrill De Maris', 'Dorothy Ann Blank', 'Webb Smith'], 'Based on': 
    # 'Snow White by The Brothers Grimm', 'Produced by': 'Walt Disney', 'Starring': 
    # ['Adriana Caselotti', 'Lucille La Verne', 'Harry Stockwell', 'Roy Atwell', 'Pinto 
    # Colvig', 'Otis Harlan', 'Scotty Mattraw', 'Billy Gilbert', 'Eddie Collins', 'Moroni 
    # Olsen', 'Stuart Buchanan'], 'Music by': ['Frank Churchill', 'Paul Smith', 'Leigh 
    # Harline'], 'Production company': 'Walt Disney Productions', 'Distributed by': 'RKO 
    # Radio Pictures', 'Release date': ['December 21, 1937 ( 1937-12-21 ) ( Carthay 
    # Circle Theatre , Los Angeles , CA , premiere)'], 'Country': 'United States', 
    # 'Language': 'English', 'Running time(minutes)': 83, 'Gross($)': 418000000.0, 'Budget
    # ($)': 1490000.0}, ...]


scrape_notable_movies_by_year
------------------------------

This method expects a year between 1920 until the year we are in. This method returns a list of movies' data of notable movies of the year you pass into the method::

    year = 1994

    notable_movies = ws.scrape_notable_movies_by_year(year)

    print(notable_movies)
    # [{'name': '1942: A Love Story', 'url': 'https://en.wikipedia.org/wiki/
    # 1942:_A_Love_Story'}, {'name': '71 Fragments of a Chronology of Chance', 'url': 
    # 'https://en.wikipedia.org/wiki/71_Fragments_of_a_Chronology_of_Chance'}, {'name': 
    # '8 Seconds', 'url': 'https://en.wikipedia.org/wiki/8_Seconds'}, {'name': 'Above 
    # the Rim', 'url': 'https://en.wikipedia.org/wiki/Above_the_Rim'} ... ]


scrape_american_movies_by_year
-------------------------------

This method almost exactly like the previous one, expects a year between 1920 and the current year. Instead of returning a list of notable movies that year, it returns american movies of the year::

    year = 1979

    american_movies = ws.scrape_american_movies_by_year(year)

    print(american_movies)
    # [{'name': 'Alien', 'url': 'https://en.wikipedia.org/wiki/Alien_(film)'}, 
    # {'name': 'Apocalypse Now', 'url': 'https://en.wikipedia.org/wiki/Apocalypse_Now'}# ... {'name': 'Yanks', 'url': 'https://en.wikipedia.org/wiki/Yanks'}]


scrape_person
--------------

This method returns a ``dict`` object containing the data of the person passed into the method. There are 2 ways of passing the person you want to scrape into the method:

 * passing a name string as the ``name`` argument.
 * passing the URL string as the ``url`` argument.

Now let's try one of them and add the alternative way as a comment::

    person_data = ws.scrape_person(name="Elon Musk")
    # alternative way: ws.scrape_person(url="https://en.wikipedia.org/wiki/Elon_Musk")

    print(person_data)
    # {'Name': 'Elon Musk', 'Born': 'Elon Reeve Musk | Pretoria, South Africa', 
    # 'Citizenship': ['South Africa (1971–present)', 'Canada (1971–present)', 'United 
    # States (2002–present)'], 'Alma mater': ['University of Pretoria', "Queen's 
    # University", 'University of Pennsylvania ( BS and BA ; 1997)'], 'Title': 
    #['Founder, CEO and Chief Engineer of SpaceX', 'CEO and product architect of Tesla, 
    # Inc.', 'Founder of The Boring Company and X.com (now part of PayPal )', 
    # 'Co-founder of Neuralink , OpenAI , and Zip2'], 'Spouse(s)': ['Justine Wilson 
    # (2000-2008)', ' Talulah Riley (2010-2012) (2013-2016)'], 'Partner(s)': 'Grimes 
    # (2018–present)', 'Children': 7, 'Parent(s)': ['Maye Musk (mother)'], 'Relatives': 
    # 'Tosca Musk (sister) Kimbal Musk (brother) Lyndon Rive (cousin)', 'Age': 50, 
    # 'Birth Date': datetime.datetime(1971, 6, 28, 0, 0)}
    


async_scrape_people
--------------------

This method, similarly to previous one, expects either a list of names or a list of URLs. For scraping data of multiple people, this method can come in handy because it makes the requests asynchronously and is almost exponentially faster than looping over the previous method.

Instead of collecting all the URLs manually we will use the URLs from ``most_important people`` property. And there will also be a demonstration of the alternative way commented::

    urls = [person["url"] for person in ws.most_important_people[-5:]]
    names = [person["name"] for person in ws.most_important_people[-5:]]

    movies_data = ws.async_scrape_people(urls=urls) 
    # alternative way: ws.async_scrape_people(names=names)

    print(movies_data)
    # [ ... {'Name': 'Taylor Swift', 'Born': 'Taylor Alison Swift | West Reading, 
    # Pennsylvania, U.S.', 'Other names': 'Nils Sjöberg', 'Occupation': 
    # ['Singer-songwriter', 'record producer', 'actress', 'director'], 'Years active': 
    # '2004–present', 'Relatives': ['Austin Swift (brother)', 'Marjorie Finlay 
    # (grandmother)'], 'Origin': 'Nashville, Tennessee, U.S.', 'Genres': ['Pop', 
    # 'country', 'rock', 'folk', 'alternative'], 'Instruments': ['Vocals', 'guitar', 
    # 'banjo', 'piano', 'ukulele'], 'Labels': ['Republic', 'Big Machine'], 'Website': 
    # 'taylorswift.com', 'Age': 31, 'Birth Date': datetime.datetime(1989, 12, 13, 0, 0)}]


scrape_custom
--------------

In Wikipedia there are data about almost anything. If want you wanted to scraped doesn't fit into previous methods, this method is just for you. This method expects you to pass in a Wikipedia URL that has an infobox.

Then let's just scrape data about a country::

    url = "https://en.wikipedia.org/wiki/Jamaica"

    jamaica_data = ws.scrape_custom(url)

    print(jamaica_data)
    # {'Name': 'Jamaica', 'Capital and largest city': 'Kingston 17°58′17″N 76°47′35″W  
    # /  17.97139°N 76.79306°W', 'Official languages': 'English', 'National language': 
    # 'Jamaican Patois', 'Ethnic groups (2011)': ['92.1% Afro-Jamaicans (incl. 25% 
    # mixed Irish Jamaican )', '6.1% Mixed', '0.8% Indian', '0.4% Other', '0.7% 
    # Unspecified'], 'Religion': ['68.9% Christianity', '—64.8% Protestantism', '—4.1% 
    # Other Christian', '21.3% No religion', '1.1% Rastafarianism', '6.5% Others', '2.
    # 3% Not stated'], 'Demonym(s)': 'Jamaican', 'Government': 'Unitary parliamentary 
    # constitutional monarchy', 'Monarch': 'Elizabeth II', 'Governor-General': 'Patrick 
    # Allen', 'Prime Minister': 'Andrew Holness', 'House Speaker': 'Marisa 
    # Dalrymple-Philibert', 'Senate President': 'Tom Tavares-Finson', 'Chief Justice': 
    # 'Bryan Sykes', 'Opposition Leader': 'Mark Golding', 'Legislature': 'Parliament', 
    # 'Upper house': 'Senate', 'Lower house': 'House of Representatives', 'Granted': '6 
    # August 1962', 'Total': '$15.424 billion ( 119th )', 'Water (%)': '1.5', '2018 
    # estimate': '2,726,667 ( 141st )', '2011 census': '2,697,983', 'Density': '266 /km 
    # (688.9/sq mi)', 'GDP ( PPP )': '2018 estimate', 'Per capita': '$5,393 ( 95th )', 
    # 'GDP (nominal)': '2018 estimate', 'Gini (2016)': '35 medium', 'HDI (2019)': '0.
    # 734 high · 101st', 'Currency': 'Jamaican dollar ( JMD )', 'Time zone': 'UTC -5', 
    # 'Driving side': 'left', 'Calling code': '+1-876 +1-658 ( Overlay of 876; active 
    # in November 2018)', 'ISO 3166 code': 'JM', 'Internet TLD': '.jm'}