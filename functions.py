#!/usr/bin/env python3

"""This module includes functions for querying the clubfinder.sqlite database and scraping data from the web."""

import sys
import sqlite3
import requests
from bs4 import BeautifulSoup
import urllib3
import re
import csv
import socket
import _socket
import random

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.158 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    #Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.109',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43',
    'Mozilla/5.0 (Windows Mobile 10; Android 8.0.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36 Edge/40.15254.603',
    #Safari
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
    #Firefox
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
]

def user_agent():
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    return headers

def connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def dbread(db, query):
    """Read data from the clubfinder sqlite database for use by other functions"""
    conn = None
#    count = 0
    try:
        print('Starting...')
        conn = sqlite3.connect(db)
        print(sqlite3.version)
        c = conn.cursor()
        rows = c.execute(query).fetchall()
        return rows

    except sqlite3.Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
            print('Connection Successfully Closed.')

def dbwrite(db, query):
    """Write new data into the clubfinder sqlite database"""
    conn = None
    #    count = 0
    try:
        print('Starting...')
        conn = sqlite3.connect(db)
        print(sqlite3.version)
        c = conn.cursor()
        c.execute(query)

    except sqlite3.Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def generateclubcsv():
    """Performs a hardcoded SQL query against the clubfinder.sqlite database and outputs a csv of the results.
    No arguments are accepted for this function. """
    conn = None
    count=0
    try:
        conn = sqlite3.connect('clubfinder.sqlite')
        gen_cursor = conn.cursor()
        rows = gen_cursor.execute('SELECT clubname, university, countyname, cluburl, facebook, twitter, instagram, countryname FROM clubs \
                                    LEFT JOIN counties ON counties.countyid = clubs.county \
                                    LEFT JOIN countries ON countries.countryid = clubs.country;').fetchall()
        print(sqlite3.version)
        print(type(rows))
        writefile('clubsnew.csv', 'w', ('clubname', 'university', 'countyname', 'cluburl', 'facebook', 'twitter', 'instagram', 'countryname'))
        for i in rows:
            writefile('clubsnew.csv', 'a', i)
            count += 1
        print(count, " rows written.")

    except sqlite3.Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
            print('Connection Successfully Closed.')


def writefile(file, mode, data):
    """Writes a row of data into a csv file.

    Args:
        file: 'file.csv' The desired filename
        mode: the appropriate mode (r/w/a) for the 'with open' statement
        data: ('string, 0, None) An iterable collection of items to be written as a row

    Returns:
        No API return. Just the output file."""
    with open(file, mode=mode, newline='') as csvfile:
        resultwriter = csv.writer(csvfile, delimiter=',')
        resultwriter.writerow(data)


def scrapeurl(url, target):
    """Visit a provided url and looks for links containing your 'target' argument
    url = 'domain.com' with or without schema
    target = 'string' representing the targeted site (e.g. 'facebook'; 'twitter'; 'insta')"""
    if ('http' not in url):
        url = 'http://' + url
    try:
        soup = BeautifulSoup(requests.post(url, headers=user_agent()).text, features="lxml", )
        for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
            if target in link.get('href'):
                result = link.get('href')
                print(link.get('href'))
                return result

    except socket.gaierror as e:
        print(f'1.Scraping {url} failed!')
        print(e)
        return None

    except requests.exceptions.ConnectionError as e:
        print(f'2.Scraping {url} failed!')
        print(e)
        return None

    except requests.exceptions.InvalidURL:
        return None


def getsoup(url):
    """Visit a provided url and parses it with bs4
    url = 'domain.com' without schema"""
    try:
        soup = BeautifulSoup(requests.get(url, headers=user_agent()).text, features="lxml")
        return soup

    except socket.gaierror as e:
        print(f'1.Scraping {url} failed!')
        print(e)
        return None

    except requests.exceptions.ConnectionError as e:
        print(f'2.Scraping {url} failed!')
        print(e)
        return None

    except requests.exceptions.InvalidURL:
        return None


def searchsoup(soup, target):
    """Searches a soup object for the target phrase. Best used after .getsoup
    Args:
        soup = a BeautifulSoup object
        target = 'string' representing the targeted site (e.g. 'facebook'; 'twitter'; 'insta')

    Returns:
        A URL containing the target phrase (if one exists)"""
    for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
        if target in link.get('href'):
            result = link.get('href')
            print(link.get('href'), ': ', result)
            return result


def searchwikidata():
    """Search wikidata for objects that may match organisations in clubfinder"""
    pass

# print(__name__)
# if __name__ == '__main__':
#    main(url = sys.argv[1]) # The 0th arg is the module filename.
