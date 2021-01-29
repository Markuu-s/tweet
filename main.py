from twitter import ParseTwitterAccount
from threading import Thread
import time


def main():
    k = 2
    pta0 = ParseTwitterAccount('https://twitter.com/_Kill_13')
    # pta1 = parse_twitter_account('https://twitter.com/Plzsenpailovem1')
    while k > 0:
        print(k, ' start')

        pta0.parse()
        #th0 = Thread(target=pta0.parse2, args=())
        #th0.start()

        # th1 = Thread(target=pta1.parse2, args=())
        # th1.start()
        k -= 1
        time.sleep(30)

if __name__ == '__main__':
    main()
