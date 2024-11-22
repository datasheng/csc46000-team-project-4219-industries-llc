from Sentiment import Sentiment

'''
each day (weekday) should have two articles scraped 
timeline goes as far back as 5 years
for testing i will do one day
'''

class WebScrape:

    def __init__(self) -> None:
        # self.emotion = Sentiment()
        pass

    def get_links(self, query: str, num_days: int) -> list[(str, str)]:
        '''
        gets links for the specified number of days for AMD and NVIDIA
        selenium -> chrome instance 
            make google search 
            get top 2 links per day for `num_days`

        returns dict with array of links
            each element is a tuple of two articles
        '''
        # https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from datetime import datetime, timedelta
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)

        result = []
        num_links_to_skip = 35
        today = datetime.today()
        date_format = "{0}/{1}/{2}"
        url = "https://www.google.com/search?q={0}&num=10&sca_esv=21c38533450dea46&sxsrf=ADLYWIJ3l27vO1gJ2FnAVnnGDJEt0tUsvg:1731969105337&source=lnt&tbs=cdr:1,cd_min:{1},cd_max:{2}&tbm="
        
        for i in range(num_days):
            day = today + timedelta(days=-i)
            local_date = date_format.format(day.month, day.day, day.year)
            day_url = url.format(query, local_date, local_date)

            driver.get(day_url)
            links = driver.find_elements(By.TAG_NAME, "a")
            n = len(links)
            i = 0
            res = []

            while len(res) < 3 and i < n:
                href = links[i].get_dom_attribute('href')
                if href and "https://" == href[:8] and "google.com" not in  href:
                    res.append(links[i].get_dom_attribute('href'))
                i += 1
                
            result.append(res)

        driver.close()
        return result

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
    amd_links = web.get_links('amd+stocks', 2)
    print(amd_links)