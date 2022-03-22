from urllib.request import urlopen, Request
import re
import sys

# 웹 요청을 보내는 브라우저 명시
user_agent = 'Mozilla/5.0\(compatible, MSTE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
# 탐색 링크 정보를 담는 리스트
href_links = []

# 인자로 전달된 doc에 존재하는 모든 href 태그를 찾아 링크 정보를 얻는 함수
def getLinks(doc, home, parent):
    global href_links
    href_pattern = [r'href=\S+"', r'href=\S+ ', r'href=\S+\'']
    tmp_urls = []

    for n in range(len(href_pattern)):
        tmp_urls += re.findall(href_pattern[n], doc, re.I)

    for url in tmp_urls:
        url = url.strip()
        url = url.replace('\'', '"')
        if (url[-1] == ' ') or (url.find('"') == -1):
            url = url.split('=')[1]
        else:
            url = url.split('"')[1]
        if len(url) == 0:
            continue
        if url.find('https://') == -1:
            if url[0] == '/':
                url = home + url
            elif url[:2] == './':
                url = 'https://' + parent + url[1:]
            else:
                url = 'https://' + parent + '/' + url
        if url in href_links:
            continue
        if '.html' not in url:
            href_links.append(url)
            continue
        runCrawler(home, url)

# url로 접속하여 HTML 페이지를 읽어오는 함수
def readHtml(url):
    try:
        req = Request(url)
        req.add_header('User-Agent', user_agent)
        with urlopen(req) as h:
            doc = h.read()
    except Exception as e:
        print('ERROR: {}'.format(url))
        print(e)
        return None
    return doc.decode()

# url로 접속하여 HTML 페이지 호출 후 HTML 페이지에서 링크 정보를 추출하는 함수
def runCrawler(home, url):
    global href_links
    href_links.append(url)
    print('GETTING ALL LINKS in [{}]'.format(url))
    try:
        doc = readHtml(url)
        if doc is None:
            return
        tmp = url.split('/')
        parent = '/'.join(tmp[2:-1])
        if parent:
            getLinks(doc, home, parent)
        else:
            getLinks(doc, home, home)
    except KeyboardInterrupt:
        print('Terminated by USER..Saving Crawled Links')
        finalize()
        sys.exit(0)
    return

# 탐색 링크 정보를 파일로 저장하는 함수
def finalize():
    with open('crawled_links.txt', 'w+') as f:
        for href_link in href_links:
            f.write(href_link + '\n')
    print('+++ CRAWLED TOTAL href_links: [{}]'.format(len(href_links)))

def main():
    targeturl = 'https://www.naver.com'
    home = 'https://' + targeturl.split('/')[2]
    print('+++ WEB LINK CRAWLER START > [{}]'.format(targeturl))
    runCrawler(home, targeturl)
    finalize()

if __name__ == "__main__":
    main()