import argparse
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
sys.path.append('./trainer')
from nutszebra_utility import Utility as utility
import downloader


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download CVPR2017 paper')
    parser.add_argument('--browser', '-b',
                        default='./chromedriver',
                        help='path to chromedriver')
    parser.add_argument('--url', '-u',
                        default='http://openaccess.thecvf.com/CVPR2017.py',
                        help='url page')
    parser.add_argument('--destination', '-d',
                        default='./papers',
                        help='destination')
    parser.add_argument('--header', '-header',
                        default='http://openaccess.thecvf.com/',
                        help='header of href')
    parser.add_argument('--thread', '-thread', type=int,
                        default=5,
                        help='number of thread')
    parser.add_argument('--timeout', '-timeout', type=int,
                        default=300,
                        help='timeout')
    args = parser.parse_args().__dict__
    print(args)
    destination = args['destination'][:-1] if args['destination'][-1] == '/' else args['destination']
    utility.make_dir(destination)

    browser = webdriver.Chrome(args['browser'])
    browser.get(args['url'])
    html = BeautifulSoup(browser.page_source, 'html.parser')
    urls = ['{}{}'.format(args['header'], a.get('href')) for a in html.find_all('a') if type(a.get('href')) is str and a.get('href')[-9:] == 'paper.pdf']
    paths = ['{}/{}'.format(destination, url.split('/')[-1]) for url in urls]
    cvpr = downloader.ThreadDownloadMaster(howmany_thread=args['thread'], urls=urls, paths=paths, timeout=args['timeout'])
    cvpr.run()
