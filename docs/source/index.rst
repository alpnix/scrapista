.. scrapista documentation master file, created by
   sphinx-quickstart on Sat Apr 10 00:21:04 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to scrapista's documentation!
=====================================

Welcome to the complete beginner's guide to Scrapista! Scrapista is a tool that helps you scraping useful information from some of the most well known websites such as Amazon, Wikipedia or IMDb. 

Who is this package for?

This package is for everyone who don't know much about scraping data from websites or for the ones who know how to scrape but looking for an efficient and feasible way of doing it. 

If you are completely new to scrapista, :ref:`install scrapista first <settingup>` then get started with it. 

If you already have scrapista installed on your system, you can :ref:`check if everything is working well <installationproblems>` or skip the set up phase and :ref:`get started with scrapista <gettingstarted>`. 

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   settingup
   moreabout


.. toctree::
   :maxdepth: 2
   :caption: Scrapers:

   scrapers/amazon
   scrapers/imdb
   scrapers/wiki
   scrapers/goodreads

.. _gettingstarted:

Quick Start
=============

In scrapista there are currently 4 different scrapers that help you scrape data from distinct webpages. They are WikiScraper, AmazonScraper, GoodReadsScraper and ImdbScraper. 

Creating an Instance 
----------------------

In order create instance of any of these classes, you will need to import them from scrapista first. 

As an example let's create an instance of the WikiScraper. I'll be using this instance object throughtout the following documentation::

    from scrapista.wikipedia import WikiScraper

    ws = WikiScraper()

Now let's see what functions or properties we can use of this instance::

   print(dir(ws))
   # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
   # '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__',
   # '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
   # '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
   # '__repr__', '__setattr__', '__sizeof__', '__str__', 
   # '__subclasshook__', '__weakref__', 'async_scrape_movies', 
   # 'async_scrape_people', 'base_url', 'disney_movies', 
   # 'highest_grossing_movies', 'most_important_people', 
   # 'scrape_american_movies_by_year', 'scrape_custom','scrape_movie', 
   # 'scrape_notable_movies_by_year', 'scrape_person']


Exploring Attributes of the Instance
-------------------------------------
Every scraper has different attributes and able to scrape different types of stuff. Since we took WikiScraper as an example, we will scrape info about a famous person.

There are two ways of scraping data about a person from wikipedia via scrapista. First of all, you can pass a ``name`` argument to the ``scrape_person`` method::

   person_name = "Stephen King"

   # passing in the name of the person as a 'name' argument
   person_info = ws.scrape_person(name=person_name)

   print(person_info)
   # {'Name': 'Stephen King', 'Born': 'Portland, Maine, U.S.', 
   # 'Pen name': ['Richard Bachman', 'John Swithen', 'Beryl Evans'], 
   # 'Occupation': 'Author', 'Alma mater': 'University of Maine', 
   # 'Period': '1967–present', 'Genre': ['Horror', 'fantasy','supernatural fiction', 
   # 'drama', 'gothic', 'genre fiction', 'dark fantasy', 
   # 'post-apocalyptic fiction', 'crime fiction', 'suspense', 
   # 'thriller'], 'Spouse': 'Tabitha Spruce (1971-present)', 
   # 'Children': 3, 'Age': 73, 'Birth Date': datetime.datetime(1947,9, 21, 0, 0)}

As you may notice ``scrape_person`` method returns a python ``dict`` object. Most of the methods that scrape a single variable returns a ``dict`` object in scrapista. However, you will also see python ``list`` object returned from methods that scrape multiple amount of that variable. 

Of course, there are more ways to scrape data with scrapista than just passing in a ``name`` argument.

By passing a wikipedia link you can pretty much scrape any data you want with the help of scrapista. Let's now scrape a movie info by passing in an URL as an argument::

   url = "https://en.wikipedia.org/wiki/The_Shawshank_Redemption"

   # this method expects a wikipedia url of the movie you will scrape
   movie_info = ws.scrape_movie(url)

   print(movie_info)
   # {'Name': 'The Shawshank Redemption', 'Directed by': 'Frank 
   # Darabont', 'Screenplay by': 'Frank Darabont', 'Based on': 'Rita 
   # Hayworth and Shawshank Redemption by Stephen King', 'Produced by': 
   # 'Niki Marvin', 'Starring': ['Tim Robbins', 'Morgan Freeman', 'Bob 
   # Gunton', 'William Sadler', 'Clancy Brown', 'Gil Bellows', 'James 
   # Whitmore'], 'Cinematography': 'Roger Deakins', 'Edited by': #
   # 'Richard Francis-Bruce', 'Music by': 'Thomas Newman', 'Production 
   # company': 'Castle Rock Entertainment', 'Distributed by': 'Columbia 
   # Pictures', 'Release date': ['September 10, 1994 ( 1994-09-10 ) ( 
   # TIFF )', 'September 23, 1994 ( 1994-09-23 ) (United States)'], 
   # 'Country': 'United States', 'Language': 'English', 'Running time
   # (minutes)': 142, 'Gross($)': 58300000.0, 'Budget($)': 25000000.0}


As you might have noticed already, same values are presented as integer, float or datetime depending on the most useful data structures they could be used in. This feature helps you execute math operations with the number values with ease. 

Wikipedia is a huge website and it is not only limited to movies or famous people. That's why there is a ``scrape_custom`` method in WikiScraper. With this method you can basically pass in any wikipedia URL as an argument and the method will return the data on that page in a ``dict`` form::

   url = "https://en.wikipedia.org/wiki/Oracle_Corporation"

   oracle_data = ws.scrape_custom(url)

   print(oracle_data)
   # {'Name': 'Oracle Corporation', 'Type': 'Public', 'Traded as': 
   # ['NYSE : ORCL', 'S&P 100 Component', 'S&P 500 Component'], 'ISIN': 
   # 'US68389X1054', 'Industry': ['Enterprise software', 'Cloud 
   # computing', 'Computer hardware'], 'Founded': 'June 16, 1977 ; 44 
   # years ago Santa Clara, California , U.S.', 'Founders': ['Larry 
   # Ellison', 'Bob Miner', 'Ed Oates'], 'Headquarters': 'Austin, Texas, 
   # United States', 'Area served': 'Worldwide', 'Key people': 
   # ['Larry Ellison (Executive Chairman & CTO)', 'Jeff Henley (Vice 
   # Chairman)', 'Safra Catz (CEO)'], 'Products': ['Oracle 
   # Applications', 'Oracle Database', 'Oracle Cloud', 'Enterprise 
   # Manager', 'Fusion Middleware', 'Servers', 'Workstations', 
   # 'Storage', '( See Oracle products )'], 'Services': ['Business 
   # software', 'applications', 'consulting'], 'Revenue': 'US$ 39.07 
   # billion (2020)', 'Operating income': 'US$13.89 billion (2020)', 
   # 'Net income': 'US$10.14 billion (2020)', 'Total assets': 'US$115.
   # 44 billion (2020)', 'Total equity': 'US$12.72 billion (2020)', 
   # 'Owner': 'Larry Ellison (36%)', 'Number of employees': '135,000 
   # (2020)', 'Subsidiaries': 'List of Oracle subsidiaries', 'Website': 
   # 'https://www.oracle.com/'}


There are many more methods and details you can explore in WikiScraper objects. If you want to learn more about :ref:`WikiScraper click here<wikiscraper>`. Or you can check out the other scrapers in scrapista:

   * :ref:`AmazonScraper<amazonscraper>`
   * :ref:`ImdbScraper<imdbscraper>`
   * :ref:`GoodReadsScraper<goodreadsscraper>`

You might also want to see `scrapista's full source code <https://github.com/alpnix/scrapista>`_ 