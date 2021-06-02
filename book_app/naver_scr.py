import requests
from bs4 import BeautifulSoup

#책 코드 출력
def books(name) :
    url = f"https://book.naver.com/search/search.nhn?sm=sta_hty.book&sug=&where=nexearch&query={name}&ie=utf8"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    return int(soup.find('div', class_='thumb_type thumb_type2').find('a').get('href').split('=')[1])


#책 코드 입력 시, 책 이름  출력
def code(code):
    url = f"https://book.naver.com/bookdb/book_detail.nhn?bid={code}"
    page1 = requests.get(url)
    soup = BeautifulSoup(page1.content, 'html.parser')
    name = soup.find('div', class_='book_info').find('img').get('alt')
    
    return name


#책 코드 입력 시, 저자 출력
def code2(code):
    url = f"https://book.naver.com/bookdb/book_detail.nhn?bid={code}"
    page1 = requests.get(url)
    soup = BeautifulSoup(page1.content, 'html.parser')
    s_author = soup.find('div', class_='book_info_inner').text.replace(', \r','').split('\n')[7]
    author = s_author.replace('저자 ','').split('|')[0]
    
    return author