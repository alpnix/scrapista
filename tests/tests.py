from scrapista.amazon import AmazonScraper
from scrapista.wikipedia import WikiScraper
import unittest 


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7,en-GB;q=0.6"
}
class TestAmazonScraper(unittest.TestCase):
    
    def test_scrape_keyword(self):
        # you don't have to pass them in since they are already default
        scraper = AmazonScraper(headers=headers)
        data_list = scraper.scrape_keyword("pencil")

        self.assertEqual(type(data_list), list)
        self.assertGreater(len(data_list), 50)

    def test_track_item(self):
        scraper = AmazonScraper(headers=headers)
        item_info = scraper.track_item("https://www.amazon.de/-/en/23-8-inch-Full-all-one/dp/B089PJ5S5B/ref=sr_1_3?currency=USD&dchild=1&keywords=computer&qid=1617312928&sr=8-3")

        self.assertEqual(type(item_info), dict)
        

class TestWikiScraper(unittest.TestCase):

    def test_scrape_movie(self):
        scraper = WikiScraper()
        url = "https://en.wikipedia.org/wiki/Fight_Club"
        
        print(dir(scraper))
        #movie_data = scraper.scrape_movie(url)
        #print(movie_data)




if __name__ == "__main__":
    unittest.main()
