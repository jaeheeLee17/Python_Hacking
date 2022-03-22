from urllib.request import urlopen, Request

user_agent = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
cookie = 'NID=1234; expires=Thu, 25-Aug-2016 06:26:36 GMT; path=/; domain=.google.co.kr; HttpOnly'

def cookieSpoofer(url):
    req = Request(url)
    req.add_header('User-Agent', user_agent)
    req.add_header('Cookie', cookie)
    with urlopen(req) as h:
        print(h.read())

def main():
    url = 'http://www.google.com'
    cookieSpoofer(url)

if __name__ == "__main__":
    main()