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


def hostIP(url):
    try:
        ipaddress.ip_address(urlparse(url).netloc)
        result = 1
    except:
        result = 0
    return result

def containAt(url):
    try:
        urlparse(url).netloc.split('@')[1].split(':')[0]
        result = 1    
    except:
        urlparse(url).netloc.split('@')[0].split(':')[0]
        result = 0    
    return result

def checkLen(url):
    if len(url) < 54:
        result = 0            
    else:
        result = 1            
    return result

def getDepth(url):
    fragURL = urlparse(url).path.split('/')
    depth = -1
    for i in range(len(fragURL)):
        if len(fragURL[i]) != 2:
            depth = depth+1
    return depth

def URLinURL(url):
    pos = url.rfind('//')
    if pos > 6:
        if pos > 7:
            return 1
        else:
            return 0
    else:
        return 0

def httpDomain(url):
    domain = urlparse(url).scheme
    if 'https' in domain:
        return 1
    else:
        return 0

def shortining(url):
    match=re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',url)
    if match:
        return 1
    else:
        return 0

def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1
    else:
        return 0 

def popularity(url):
    try:
        url = urllib.parse.quote(url)
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        rank = int(rank)
    except TypeError:
        return 1
    if rank < 100000:
        return 0
    else:
        return 1

def site(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        }

        google = "https://www.google.com/search?q=site:" + url + "&hl=en"
        response = requests.get(google, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        not_indexed = re.compile("did not match any documents")

        if soup(text=not_indexed):
            return 0
        else:
            return 1
    except requests.exceptions.ConnectionError:
        return 0

def domainAge(url):
    w = whois.whois(url)
    creation_date = w.creation_date
    expiration_date = w.expiration_date
    if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
        try:
            creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
        except:
            return 1
    if ((expiration_date is None) or (creation_date is None)):
        return 1
    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
        return 1
    else:
        ageofdomain = abs((expiration_date - creation_date).days)
        if ((ageofdomain/30) < 6):
            age = 1
        else:
            age = 0
    return age

def domainEnd(url):
    w = whois.whois(url)
    expiration_date = w.expiration_date
    if isinstance(expiration_date,str):
        try:
            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
        except:
            return 1
    if (expiration_date is None):
        return 1
    elif (type(expiration_date) is list):
        return 1
    else:
        today = datetime.datetime.now()
        end = abs((expiration_date - today).days)
        if ((end/30) < 6):
            end = 0
        else:
            end = 1
    return end

def iframe(response):
    try:
        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
                        }
        response = requests.get(response, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        if response == "":
            return 0
        else:
                if re.findall(r"<iframe", response.text):
                    return 1
                else:
                    return 0
    except requests.exceptions.ConnectionError:
        return 0

def mouseOver(response):
    try:
        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
                        }
        response = requests.get(response, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser') 
    
        if response == "" :
            return 1
        else:
            if re.findall("mouseover", response.text):
                return 1
            else:
                return 0
    except requests.exceptions.ConnectionError:
        return 0

def rightClick(response):
    headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
                        }
    response = requests.get(response, headers=headers)
    if response == "":
        return 0
    else:
        if re.findall('contextmenu', response.text):
            return 1
        else:
            return 0

def forwarding(response):
    try:
        headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
                            }
        response = requests.get(response, headers=headers)
        if response == "":
            return 1
        else:
            if len(response.history) <= 2:
                return 0
            else:
                return 1
    except requests.exceptions.ConnectionError:
        return 0

def checkFavicon(url):
    try:
        hostname= urlparse(url).netloc
        headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
                            }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser') 
        if soup=="":
            return 1
        else:
            for head in soup.find_all('head'):
                for head.link in soup.find_all('link', href=True):
                    dots = [x.start() for x in re.finditer(r'\.', head.link['href'])]
                    return 0 if url in head.link['href'] or len(dots) == 1 or hostname in head.link['href'] else 1
            return 0
    except requests.exceptions.ConnectionError:
        return 0

url=" " 
url2=" " 
url3=" " 
url4=" /"
url5=" "
url6=" "
url7=" "

print(domainAge(url))
print(domainAge(url2))
print(domainAge(url3))
print(domainAge(url4))


# print(site(url))
# print(site(url2))
# print(site(url3))
# print(site(url4))


