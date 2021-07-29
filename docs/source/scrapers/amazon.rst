.. _amazonscraper:

Amazon Scraper
===============

For taking a look at Amazon's robots.txt visit `here <https://www.amazon.com/robots.txt>`_.

With AmazonScraper you can scrape data about almost all the products available on Amazon and track some of the products that you are planning to buy. 

Creating an AmazonScraper Object 
---------------------------------

First of all we will import the AmazonScraper class from the relative file:: 

    from scrapista.amazon import AmazonScraper

While creating an instance you can pass in amazon.de or amazon.fr for the ``base_url`` argument, but the default is amazon.com.
The other arguments you can change is ``headers`` and ``params``. Unless you have specific ones you want to pass in you would mostly use the default ones for both of these optional arguments. 

So, let's leave everything as default and create an AmazonScraper instance::
     
    azs = AmazonScraper()

    print(dir(azs))
    # ['__class__', '__delattr__', ... 'async_scrape_keywords', 'async_track_items', 
    # 'base_url', 'headers', 'params', 'scrape_keyword', 'scrape_keywords', 
    # 'track_item', 'track_items', 'tracked']


scrape_keyword
---------------

With the helps of ``scrape_keyword`` method you can pass a keyword or an object name as an argument and get data about the market in Amazon. For example let's search for computers in amazon.com::

    keyword = "computer"
    computers_data = azs.scrape_keyword(keyword)

    print(len(computers_data))
    # 46

    # taking a look at the first product
    print(computers_data[0])
    # {'name': 'Goodtico Mini PC Intel i7 10510U Windows 10 Pro/Support Windows 11, 
    # Mini Gaming Computer, 16GB DDR4 RAM(Max 64GB), 512G NVME SSD, Support 2.5inch HDD/
    # SSD USB×6, 2.4G/5.0G WiFi 6, BT 5.0', 'price($)': 719.0, 'stars(5)': 5.0, 'url': ,
    # 'https://www.amazon.com/gp/slredirect/picassoRedirect.html/
    # ref=pa_sp_atf_aps_sr_pg1_1?ie=UTF8&adId=A0739476GIXAIXHLY0I0&
    #url=%2FGoodtico-Windows-Support-Computer-2-5inch%2Fdp%2FB0918MVYBC%2Fref%3Dsr_1_1_s
    #spa%3Fcurrency%3DUSD%26dchild%3D1%26keywords%3Dcomputer%26qid%3D1627236115%26sr%3D8
    # -1-spons%26psc%3D1&qualifier=1627236115&id=6408420411097718&widgetName=sp_atf', 
    # 'img_src': 'https://m.media-amazon.com/images/I/61V1L10X16L._AC_UY218_.jpg'}


scrape_keywords
----------------

This method is almost identical to the previous ``scrape_keyword`` method. The only difference is that this method expects a list of keywords as a first argument. Therefore, this method makes multiple requests to different pages and it takes quite some time to make all these requests synchronously.  
Let's take a look at an example::

    import time

    start = time.time()
    keywords = ["pen","chair","towel"]

    object_data = azs.scrape_keywords(keywords)
    
    print(len(object_data))
    # 169

    print(time.time() - start)
    # 7.088 seconds

async_scrape_keywords
----------------------

As it is discussed above, making all the requests for different objects synchronously takes a lot of time. Making these requests asynchronously is the solution presented in scrapista:: 

    import time

    start = time.time()
    keywords = ["pen","chair","towel"]

    object_data = azs.async_scrape_keywords(keywords)
    
    print(len(object_data))
    # 169

    print(time.time() - start)
    # 4.166 seconds

We can see a noticable amount of time reducement. If we had a bigger scale in terms of the length of the list. We could have even reduce the time enourmously.  

track_item
-----------

With the AmazonScraper instance you can select particular products that you want to buy in the near future and add them into your tracked items list. This method expects the URL of the item you want to track::

    azs.track_item("https://www.amazon.com/AmazonBasics-Nylon-Braided-Lightning-Cable/dp/B082T6GVKJ/")

    azs.track_item("https://www.amazon.com/AmazonBasics-Legal-Orchid-Color-6-Pack/dp/B086LW3VDD/")

This way you add these products into your tracked items list. You can view the list by the following block of code::

    print(azs.tracked)
    # ["https://www.amazon.com/AmazonBasics-Nylon-Braided-Lightning-Cable/dp/B082T6GVKJ/", 
    # "https://www.amazon.com/AmazonBasics-Legal-Orchid-Color-6-Pack/dp/B086LW3VDD/"]

With this property you can keep track of items you want to buy in the near future and get the useful data that is presented on the website about them. 

track_items
------------

This method is just like the ``track_item`` method but it expects a list of prodcut URLs instead of a single one. For example::

    azs.track_items([
        "https://www.amazon.com/AmazonBasics-Nylon-Braided-Lightning-Cable/dp/B082T6GVKJ/", 
        "https://www.amazon.com/AmazonBasics-Legal-Orchid-Color-6-Pack/dp/B086LW3VDD/"
    ])

    print(azs.tracked)
    # ["https://www.amazon.com/AmazonBasics-Nylon-Braided-Lightning-Cable/dp/B082T6GVKJ/", 
    # "https://www.amazon.com/AmazonBasics-Legal-Orchid-Color-6-Pack/dp/B086LW3VDD/"]


async_track_items
------------------

``async_track_items`` is almost the same method as ``track_items`` but it makes requests asynchronously, thus it is much faster::

    azs.async_track_items([
        "https://www.amazon.com/AmazonBasics-Nylon-Braided-Lightning-Cable/dp/B082T6GVKJ/", 
        "https://www.amazon.com/AmazonBasics-Legal-Orchid-Color-6-Pack/dp/B086LW3VDD/"
    ])

    print(azs.tracked)
    # ["https://www.amazon.com/AmazonBasics-Nylon-Braided-Lightning-Cable/dp/B082T6GVKJ/", 
    # "https://www.amazon.com/AmazonBasics-Legal-Orchid-Color-6-Pack/dp/B086LW3VDD/"]
