More About Scrapista
=====================
Here you can find more details about how scrapista is built or how scraping a website works. Unless you are interested in the development of scrapista you should probably move onto scrapers' documentation or :ref:`quick start<gettingstarted>`

.. _scrapingpolicy:

Scraping Policy
----------------
Scraping can be not allowed in most of the websites you encounter on internet. For checking each website's policy you can take a look at their robots.txt which is most likely going to be placed in the main directory of the website. 

.. admonition:: Quick Note

    The scrapers in scrapista doesn't scrape data against the websites' will, unless you use them excessively in a short period of time.

Sync/Async Mehtods
-------------------

In all of scrapista's scrapers there are synchronous methods and their respective asynchronous ones for some of them. The methods with any prefix are mostly synchronous and the ones start with ``async`` are asynchronous methods. 

So, what are the differences between synchronous and asynchronous methods?

When you scrape data from multiple pages, you will have to make more than a single request. In synchronous functions each request is made after the response from the prior request is received. In asynchronous methods each request is made simultaniously without waiting for the response, therefore making the whole process much quicker. 

For the asynchronous methods scrapista uses ``concurrent.futures`` module in Python. It has a class called ``ThreadPoolExecutor`` which assigns the functions you submitted into the distinct cores your computer has. 

As a result these types of methods return a ``list`` object that consists of ``dict`` object of every single page that's been scraped out of all the requests.

.. admonition:: Remember!

    Using too much back to back async methods might not be permitted by most of the websites, since it makes numerous requests in a little amount of time. As mentioned in the :ref:`Scraping Policy<scrapingpolicy>`, you might want to read the robots.txt of each website before making too many requests asynchronously. 


Input/Output Data
------------------

In some of the scrapers the country you are in can make a difference in terms of the scraped data. For example, while creating an instance of ``AmazonScraper`` you can specify whether you want amazon.de, amazon.com or any other website of amazon. 

Some methods expect a list of URLs or a list of titles that will allow it to make request to different web pages. These methods will return Python ``list`` object that compromises of ``dict`` objects. 

In these ``dict`` objects there are a lot of numerical or date values. Scrapista converts most of these numerical data into integers or floats which are usually scrapped as ``string`` objects. Also most of the dates are automatically converted to Python ``datetime`` objects. Both of these conversions being done automatically under the hood allows you to use these values for your calculations without any difficulties. 

With that being said, there might still be some exceptions that weren't detected and stood as ``string`` objects that were supposed to be converted to different data types. 

If you encounter any of these mistakes, you can create an issue or make a pull request in `scrapista's Github repository <https://github.com/alpnix/scrapista>`_.


Helper Functions  
-----------------

There are some helper functions that are used in the scraper class methods. However, you can use these helper functions externally as well. 

In order to see and utilize some of the functions you can start by importing helpers.py file:: 

    from scrapista.helpers import helpers

    print(dir(helpers))
    # ['BeautifulSoup', '__builtins__', '__cached__', '__doc__', 
    # '__file__', '__loader__', '__name__', '__package__', '__spec__', 
    # 'dt', 'get_age', 'get_bdate', 'get_count', 'get_currency_ratio', 
    # 'get_word_info', 'money_string_to_int', 'put_year_limit', 're', 
    # 'requests']

Some of these functions might not be useful outside of scraper methods. Let's take a look at some of the useful ones.

Get Word Info 
++++++++++++++

This function expects two arguments, first of them being the word you want to get info about, the second of them being a headers dict. The data is scraped from Cambridge Dictionary, you can access their robots.txt from `here <https://dictionary.cambridge.org/robots.txt>`_:: 

    word_data = helpers.get_word_info("scrape",{"User-Agent":"""
    Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
    AppleWebKit/537.36 (KHTML, like Gecko) 
    Chrome/91.0.4472.164 Safari/537.36"""})

    print(word_data)
    # {'word': 'scrape', 'form': 'verb', 'definition': 'to remove an 
    # unwanted covering or a top layer from something, especially 
    # using a sharp edge or something rough :', 'sentence_examples': 
    # ['Scrape your boots clean before you come in.', "We'll have to 
    # scrape the snow off the car before we go out in it.", 'Emily 
    # scraped away the dead leaves to reveal the tiny shoot of a new 
    # plant .', ... 'Oh, he’s had a few scrapes with the law when he 
    # was younger , but he’s straightened his life out now.']}

Get Currency Ratio
+++++++++++++++++++

This function expects two different currency abbreviations for the first and second argument with the first one being the currency you own to the second one being the target currency you want to have::

    euro_to_dollars = helpers.get_currency_ratio("EUR","USD")

    print(euro_to_dollars)
    # 1.177
    # So, 100 euro is equivalent to 117.7 U.S dollars by today's currency