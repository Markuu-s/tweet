import os
from selenium import webdriver
import time
from bs4 import BeautifulSoup as BS
from send_to_bd import send

class parse_twitter_account(object):

    URL: str
    driver: webdriver
    last_tweets = set()
    first_parse = False
    chromedriver = '/home/mark/Desktop/git/tweet/chromedriver'

    def __init__(self, URL):
        self.URL = URL
        os.environ['webdriver.chrome.driver'] = self.chromedriver

        #self.driver = webdriver.Chrome(chromedriver)
        #self.driver.get(URL)
        # self.scroll_to_end()

    def scroll_to_cnt(self, cnt=10 ** 10):
        lenOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        k = 0
        while match == False and k < cnt:
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == lenOfPage:
                match = True
            k += 1

    def parse1(self):
        self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.get(self.URL)

        time.sleep(3)
        self.first_parse = True # debug
        if not self.first_parse:
            self.first_parse = True
            self.first_parse_fun()
            return

        self.scroll_to_cnt(5)
        html = self.driver.page_source
        soup = BS(html, 'html.parser')

        tweets = soup.find_all('div', {'class': ['css-901oao', 'r-18jsvk2', 'r-1qd0xha', 'r-a023e6', 'r-16dba41',
                                                 'r-ad9z0x', 'r-bcqeeo', 'r-bnwqim', 'r-qvutc0']})
        with open('output.txt', 'w') as file:
            # file.write(soup.prettify())
            for tweet in tweets:
                file.write(tweet.text + '\n' + '*-' * 10 + '\n')

    def first_parse_fun(self):
        ls = self.driver.find_elements_by_css_selector(
            'div.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo'
            '.r-bnwqim.r-qvutc0')

        text = ls[0].text
        self.last_tweets.add(text)

        self.send([text])

    def parse_part(self):
        new_tweets = []
        ls = self.driver.find_elements_by_css_selector(
            'div.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo'
            '.r-bnwqim.r-qvutc0')
        ls = list([l.text for l in ls])
        for text in ls:
            if text not in self.last_tweets:
                new_tweets.append(text)
                self.last_tweets.add(text)
            else:
                return [True, new_tweets]
        return [False, new_tweets]

    def parse2(self):
        self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.get(self.URL)

        time.sleep(3)

        if not self.first_parse:
            self.first_parse = True
            self.first_parse_fun()
            return

        match, new_tweets = self.parse_part()

        len_of_page = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

        while match == False:
            time.sleep(3)
            match, new_tweets = self.parse_part()

            last_count = len_of_page
            time.sleep(3)
            len_of_page = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if last_count == len_of_page:
                match = True

        self.send(new_tweets)
        self.driver.quit()

    def send(self, tweets):
        send(tweets)
