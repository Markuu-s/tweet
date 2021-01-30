import os
from selenium import webdriver
import time
import re

class ParseTwitterAccount(object):
    URL: str
    time_sleep = 8
    driver: webdriver
    last_tweets = set()
    first_parse = False
    chromedriver: str
    CssSelectorForTweets = 'div.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0'
    CssSelectorForPin = 'div.css-901oao.css-cens5h.r-m0bqgq.r-1qd0xha.r-n6v787.r-b88u0q.r-1sf4r6n.r-bcqeeo.r-qvutc0'
    const_pin_tweet = '@' * 1000
    pin_tweet_str = const_pin_tweet

    def __init__(self, URL):
        self.URL = URL
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # self.chromedriver = '/home/mark/Desktop/git/tweet/chromedriver'  # for me
        self.chromedriver = '/usr/src/bin/chromedriver'  # for docker
        self.driver = webdriver.Chrome(self.chromedriver, chrome_options=chrome_options)
        os.environ['webdriver.chrome.driver'] = self.chromedriver

    def _format_text(self, text):
        results = re.findall(r'\n[@]\w*\n', text)
        for result in results:
            text = text.replace(result, result[1:len(result) - 1])

        #print(text)
        return text

    def _first_parse_fun(self):
        ls = self.driver.find_elements_by_css_selector(self.CssSelectorForTweets)

        try:
            ls = list([tx.text for tx in ls])
            k = 0
            if ls[0] == self.pin_tweet_str:
                k += 1
            text = self._format_text(ls[k])  # .text
            self.last_tweets.add(text)
        except IndexError:
            text = 'Warning: Profile is blocked/frozen or has no tweets or does`t exist'

        return [text]

    def parse_part(self):
        new_tweets = []
        ls = self.driver.find_elements_by_css_selector(self.CssSelectorForTweets)
        ls = list([self._format_text(tx.text) for tx in ls])
        for text in ls:
            if text == self.pin_tweet_str:
                continue

            if text not in self.last_tweets:
                new_tweets.append(text)
                self.last_tweets.add(text)
            else:
                return [True, new_tweets]
        return [False, new_tweets]

    def _pin_tweet(self):      # Return True / False
        ls = self.driver.find_elements_by_css_selector(self.CssSelectorForPin)
        if len(ls) != 0:
            ls = self.driver.find_elements_by_css_selector(self.CssSelectorForTweets)
            self.pin_tweet_str = self._format_text(ls[0].text)
        # print(self.pin_tweet_str)

    def parse(self):

        # If it`s first time, when we parse tweet
        # We start parse with last tweet and later
        if not self.first_parse:
            self.driver.get(self.URL)
            time.sleep(self.time_sleep)
            self._pin_tweet()
            self.first_parse = True
            return self._first_parse_fun()
        else:
            # Refresh page to get new tweets
            # try:
            self.driver.refresh()
            # except

            time.sleep(self.time_sleep)

        # match == True, if page is not end
        # or match == True, if not found all tweets
        match, new_tweets = self.parse_part()

        len_of_page = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

        while not match:
            time.sleep(self.time_sleep)
            match, temp = self.parse_part()
            new_tweets.append(temp)

            last_count = len_of_page
            time.sleep(self.time_sleep)
            len_of_page = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")
            if last_count == len_of_page:
                match = True

        # self.driver.close()
        # self.driver.quit()
        return new_tweets[::-1]


class _TweetAcc:
    data: str
    time: str
    id: str  # maybe hash data + time
    media: []
    type: str  # pin tweet or just tweet
    # how to parse emoji ??

def main():
    ParseTwitterAccount('')
main()