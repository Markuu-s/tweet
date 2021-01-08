import os
from selenium import webdriver
import time
from threading import Thread
from bs4 import BeautifulSoup as BS

class parse_twitter_account(object):

    def __init__(self, URL):
        self.URL = URL
        chromedriver = '/home/mark/PycharmProjects/pythonProject/chromedriver'
        os.environ['webdriver.chrome.driver'] = chromedriver

        self.driver = webdriver.Chrome(chromedriver)
        self.driver.get(URL)
        #self.scroll_to_end()

    def scroll_to_end(self):
        lenOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while match == False:
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == lenOfPage:
                match = True


    def parse0(self):
        #time.sleep(30) -- for debagin
        ls = self.driver.find_elements_by_css_selector(
            'div.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo'
            '.r-bnwqim.r-qvutc0')

        with open('tweets/' + self.URL[str(self.URL).rfind('/') + 1::] + '.txt', 'w') as file:
            for l in ls:
                file.write(l.text + '\n'+ '*-'*10+'\n')
            file.close()

    def parse1(self):
        self.scroll_to_end()
        html = self.driver.page_source
        soup = BS(html, 'html.parser')

        #tweets = soup.findAll('div',
#                              {'class':
#                                        ['css-901oao', 'r-18jsvk2', 'r-1qd0xha', 'r-a023e6', 'r-16dba41', 'r-ad9z0x', 'r-bcqeeo', 'r-qvutc0']
#                                      })
        tweets = soup.findAll('div.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0')
        with open('output.txt', 'w') as file:
            #file.write(soup.prettify())
            for tweet in tweets:
                file.write(tweet.text + '\n' + '*-' * 10 + '\n')

    def parse2(self):
        none_repeat = set()
        cnt = 0
        lenOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        with open('tweets/' + self.URL[str(self.URL).rfind('/') + 1::] + '.txt', 'w') as file:
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            match = False
            while match == False:
                time.sleep(3)
                ls = self.driver.find_elements_by_css_selector(
                    'div.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo'
                    '.r-bnwqim.r-qvutc0')
                for l in ls:
                    text = l.text
                    if text not in none_repeat:
                        cnt += 1
                        file.write(text + '\n' + '*-' * 10 + '\n')
                        none_repeat.add(text)

                lastCount = lenOfPage
                time.sleep(3)
                lenOfPage = self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount == lenOfPage:
                    match = True

        print('cnt tweets: ', cnt)

def main():
    pta0 = parse_twitter_account('https://twitter.com/_bulletproof_18')
    #pta1 = parse_twitter_account('https://twitter.com/Plzsenpailovem1')

    th0 = Thread(target=pta0.parse2, args=())
    th0.start()

    #th1 = Thread(target=pta1.parse2, args=())
    #th1.start()

if __name__ == '__main__':
    main()