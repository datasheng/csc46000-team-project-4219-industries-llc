from Sentiment import Sentiment

'''
each day (weekday) should have two articles scraped 
timeline goes as far back as 5 years
for testing i will do one day
'''

class WebScrape:

    def __init__(self) -> None:
        self.emotion = Sentiment()
        self.n = 1028

    def get_links(self, query: str) -> list[(str, str)]:
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
        today = datetime.today()
        date_format = "{0}/{1}/{2}"
        url = "https://www.google.com/search?q={0}&num=10&sca_esv=21c38533450dea46&sxsrf=ADLYWIJ3l27vO1gJ2FnAVnnGDJEt0tUsvg:1731969105337&source=lnt&tbs=cdr:1,cd_min:{1},cd_max:{2}&tbm="

        for i in range(self.n, 365*5):
            day = today + timedelta(days=-i)
            print(day)
            local_date = date_format.format(day.month, day.day, day.year)
            day_url = url.format(query, local_date, local_date)

            driver.get(day_url)
            links = driver.find_elements(By.TAG_NAME, "a")
            n = len(links)
            j = 33
            res = []
            print(n)

            if n == 3:
                driver = webdriver.Chrome(options=chrome_options)
                driver.get(day_url)
                links = driver.find_elements(By.TAG_NAME, "a")
                n = len(links)
                j = 33
                res = []
                # print(n)

            while len(res) < 2 and j < n:
                link_text = str(links[j].text)
                # print(link_text)
                if link_text:
                    res.append(link_text) 
                j += 1

            result.append(res)
            print(f"Day {i} done")

        driver.close()
        return result

    def get_html(self, links: list[str]) -> list[str]:
        from bs4 import BeautifulSoup
        import requests

        html_bodies = []
        for link in links:
            if not link:
                html_bodies.append("")
                continue

            try:
                response = requests.get(link, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, features="html.parser")
                html_bodies.append(str(soup.get_text()))
            except requests.exceptions.RequestException as e:
                html_bodies.append("")
        return html_bodies
    
    def validate_link(self, href):
        import requests

        try:
            _ = requests.get(href, timeout=5)
        except Exception as e:
            return False

        conds = href is not None
        conds *= href.startswith("https://")
        conds *= "google.com" not in href
        return bool(conds)

    def get_sentiment(self, htmls: list[str]):
        '''
        averages the sentiments of both days into one and stores in list
        '''
        res = []
        for html in htmls:
            print(html)
            sentiment = sum(self.emotion.get_sentiment(html)) / 2
            res.append(sentiment)

        return res

    def save(self, arr):
        from datetime import datetime, timedelta
        
        today = datetime.today()
        date_format = "{0}/{1}/{2}"

        with open("data.json", "a") as f:
            # f.write("{\n")
            j = 0
            for i in range(self.n, self.n * 2):
                if i != 0:
                    f.write(",\n")
                day = today + timedelta(days=-i)
                local_date = date_format.format(day.month, day.day, day.year)
        
                f.write(f"\t\"{local_date}\": {arr[j]}")
                j += 1
            # f.write("\n}")        
        

if __name__ == "__main__":
    web = WebScrape()
    print("Getting HTML Links")
    amd_links = web.get_links('amd+stocks')
    print("Getting Sentiment")
    sentiment = web.get_sentiment(amd_links)
    web.save(sentiment)

