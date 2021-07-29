.. _goodreadsscraper:

GoodReads Scraper
==================

For taking a look at GoodReads's robots.txt visit `here <https://www.goodreads.com/robots.txt>`_.

With GoodReadsScraper you can scrape popular quotes said by famous people, scrape quotes by their topics. You can scrape books by their genre or any book you have a GoodReads URL to. 

Creating an GoodReadsScraper Object
------------------------------------

While creating an instance of ``GoodReadsScraper`` you can pass in the arguments of ``headers`` and ``base_url`` if you have any specific preferences about the goodreads domain or your user agent etc. For now, we will go on create an object on a default set up as it is the best way most of the times::

    from scrapista.goodreads import GoodReadsScraper

    grs = GoodReadsScraper()


Now let's take a look at the available attributes of this object:: 

    print(dir(grs))
    # ['__class__', '__delattr__', ... 'async_scrape_books', 'base_url', 
    # 'popular_quotes', 'scrape_book', 'scrape_books_by_genre', 'scrape_quotes_by_tag']


popular_quotes
---------------

With this property you can access to most popular quotes said by famous people. You will be returned with a list containing a single dictionary for each of the keys. In this dictionaries you will get to access the quote itself, the amount of likes the quote got and by whom this quote was told:: 

    popular_quotes = grs.popular_quotes

    print(popular_quotes)
    # [{'quote': '“Be yourself; everyone else is already taken.”', 'by': 'Oscar Wilde', 
    # 'likes': 156908}, {'quote': "“Two things are infinite: the universe and human 
    # stupidity; and I'm not sure about the universe.”", 'by': 'Albert Einstein', 
    # 'likes': 137367}, {'quote': '“So many books, so little time.”', 'by': 'Frank 
    # Zappa', 'likes': 134668},  ... ]


scrape_quotes_by_tag
---------------------

This method expects a quote topic such as, 'hope', 'motivation' or 'life'. As a result you will be returned a list of quote dictionaries in the same format as the previous property:: 

    motivational_quotes = grs.scrape_quotes_by_tag("motivation")

    print(motivational_quotes)
    # [{'quote': "“Don't be pushed around by the fears in your mind. Be led by the 
    # dreams in your heart.”", 'by': 'Roy T. Bennett,', 'likes': 7590}, {'quote': '“It’s 
    # only after you’ve stepped outside your comfort zone that you begin to change, 
    # grow, and transform.”', 'by': 'Roy T. Bennett', 'likes': 5581}, ... ]


scrape_book
------------

With this method you can pass in a GoodReads book URL as the only argument. A dictionary containing the data of the book will be returned:: 

    book_data = grs.scrape_book("https://www.goodreads.com/book/show/157993.The_Little_Prince")

    print(book_data)
    # {'name': 'The Little Prince', 'rating(5)': 4.31, 'rating_count': 1544181, 
    # 'review_count': 45300, 'img_src': 'https://i.gr-assets.com/images/S/compressed.
    # photo.goodreads.com/books/1367545443l/157993.jpg'}


scrape_books_by_genre
----------------------

Just like scraping a particular book's data, you can also get data of books belonging to a particular genre. For example:: 

    fiction_books = grs.scrape_books_by_genre("fiction")

    print(fiction_books)
    # [{'title': 'Harry Potter and the Prisoner of Azkaban (Harry Potter, #3)', 'genre': 
    # 'fiction', 'url': 'https://www.goodreads.com/book/show/5.
    # Harry_Potter_and_the_Prisoner_of_Azkaban', 'img_src': 'https://i.gr-assets.com/
    # images/S/compressed.photo.goodreads.com/books/1499277281l/5.jpg'}, {'title': 'Ace 
    # of Spades', 'genre': 'fiction', 'url': 'https://www.goodreads.com/book/show/
    # 42603984-ace-of-spades', 'img_src': 'https://i.gr-assets.com/images/S/compressed.
    # photo.goodreads.com/books/1607008002l/42603984._SY475_.jpg'}, ... ]


async_scrape_books
-------------------

This function comes in handy when you want to scrape info about more than a single book.  This method expects a list of URLs and returns a list of each book's data dictionary. Since, the requests are made asynchronously to each book URL in the list, the method executes quickly.

In order to get multiple book URLs without a manuel method, we will use the previous ``scrape_books_by_genre`` and get the URLs out of all the books returned. Let's get the biography book URLs as an example::

    biography_books = grs.scrape_books_by_genre("biography")

    book_urls = [book["url"] for book in biography_books]

Now let's move on and use these URLs in order to asynchronously scrape all those data::

    books_data = grs.async_scrape_books(book_urls[-3:])

    print(books_data)
    # [{'name': 'Into the Wild', 'rating(5)': 3.99, 'rating_count': 936303, 
    # 'review_count': 22972, 'img_src': 'https://i.gr-assets.com/images/S/compressed.
    # photo.goodreads.com/books/1403173986l/1845.jpg'}, {'name': 'The Autobiography of 
    # Malcolm X', 'rating(5)': 4.32, 'rating_count': 229339, 'review_count': 7205, 
    # 'img_src': 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/
    # 1434682864l/92057.jpg'}]

