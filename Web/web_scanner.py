from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import quote
from queue import Queue
from threading import Thread

# 웹 요청을 보내는 브라우저 명시
user_agent = 'Mozilla/5.0\(compatible, MSTE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'

# 주어진 targethost에서 스캔 대상 확장자인 exts가 포함된 URL들의 정보를 스캔하는 함수
def webScanner(q, targethost, exts):
    while not q.empty():
        scanlist = []
        toscan = q.get()
        if '.' in toscan:
            scanlist.append('{}'.format(toscan))
            for ext in exts:
                scanlist.append('{}{}'.format(toscan, ext))
        else:
            scanlist.append('{}/'.format(toscan))

    for toscan in scanlist:
        url = '{}/{}'.format(targethost, quote(toscan))
        try:
            req = Request(url)
            req.add_header('User-Agent', user_agent)
            res = urlopen(req)
            if len(res.read()):
                print('[{}]: {}'.format(res.code, url))
            res.close()
        except URLError as e:
            pass

def main():
    targethost = 'http://test.nanum.info:81/'
    wordlist = './target/all.txt'
    exts = ['~', '~1', '.back', '.bak', '.old', '.orig', '_backup']
    q = Queue()

    with open(wordlist, 'rt') as f:
        words = f.readlines()

    for word in words:
        word = word.rstrip()
        q.put(word)

    print('+++[{}] SCANNING START..'.format(targethost))
    for i in range(50):
        t = Thread(target=webScanner, args=(q, targethost, exts))
        t.start()

if __name__ == "__main__":
    main()