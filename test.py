import requests
import re
import os
import json
from bs4 import BeautifulSoup
import whois
import datetime
from dateutil.parser import parse as date_parse
from urllib.parse import urlparse,urlencode
import ipaddress
import re
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
from datetime import datetime
import requests
import json

def checkRequestUrl(url):
    hostname= urlparse(url).netloc
    headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
                            }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup=="":
        return 1
    else:
        i = 0
        success = 0
        for img in soup.find_all('img', src=True):
            dots = [x.start() for x in re.finditer(r'\.', img['src'])]
            if url in img['src'] or hostname in img['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for audio in soup.find_all('audio', src=True):
            dots = [x.start() for x in re.finditer(r'\.', audio['src'])]
            if url in audio['src'] or hostname in audio['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for embed in soup.find_all('embed', src=True):
            dots = [x.start() for x in re.finditer(r'\.', embed['src'])]
            if url in embed['src'] or hostname in embed['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for i_frame in soup.find_all('i_frame', src=True):
            dots = [x.start() for x in re.finditer(r'\.', i_frame['src'])]
            if url in i_frame['src'] or hostname in i_frame['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        try:
            percentage = success / float(i) * 100
        except Exception:
            return 0

        if percentage < 22.0:
            return 0
        else:
            return 1

url=" " 
url2=" " 
url3=" " 
url4=" /"
url5=" "
url6=" "
url7=" "

print(checkRequestUrl(url))
print(checkRequestUrl(url2))
print(checkRequestUrl(url5))
print(checkRequestUrl(url6))
print(checkRequestUrl(url7))
