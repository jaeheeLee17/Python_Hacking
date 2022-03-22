from urllib.request import Request, urlopen

def addReferer(url):
    req = Request(url)
    req.add_header('Referer', 'http://www.mysite.com')
    with urlopen(req) as h:
        print(h.read())

def main():
    url = 'http://www.google.com'
    addReferer(url)

if __name__ == "__main__":
    main()