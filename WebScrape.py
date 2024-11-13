from Sentiment import Sentiment

'''
each day (weekday) should have two articles scraped 
timeline goes as far back as 5 years
for testing i will do one day
'''

class WebScrape:

    def __init__(self) -> None:
        self.emotion = Sentiment()

    def get_links(self, num_days: int) -> dict:
        '''
        gets links for the specified number of days for AMD and NVIDIA

        returns dict with array of links
            each element is a tuple of two articles
        '''
        pass

    def get_html(self, links: list[(str, str)]) -> list[(str, str)]:
        '''
        converts list of tuples of urls to list of html body (no div tags)
        '''
        from bs4 import BeautifulSoup

        for i, link1, link2 in enumerate(links):
            # get html of link
            link1, link2 = links[i]
            link1 = BeautifulSoup(link1)
            link2 = BeautifulSoup(link2)
            
            # parse html for body (beauitfy)
            link1 = link1.get_text()
            link2 = link2.get_text()
            
            # replace value in place
            links[i] = (link1, link2)
        return links
    
    def get_sentiment(self, htmls: list[str]):
        '''
        averages the sentiments of both days into one and stores in list
        '''
        res = []
        for html in htmls:
            sentiment = sum(self.emotion.get_sentiment(html)) // 2
            res.append(sentiment)

        return res


if __name__ == "__main__":
    web = WebScrape()
    links = web.get_links(1)

    amd_html = web.get_html(links['amd'])
    nvidia_html = web.get_html(links['nvidia'])

