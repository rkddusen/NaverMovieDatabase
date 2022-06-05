from itertools import count
import requests
from bs4 import BeautifulSoup
import pymysql


# 데이터베이스 네이버 영화 크롤링 작업 DB로 전송.


# db 열기
def open_db():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='movie', charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    return conn, cur

#  db 닫기
def close_db(conn, cur):
    cur.close()
    conn.close()
    

# 네이버 영화 크롤링
def crawl_naver_movie(number):
    
    conn, cur = open_db()
    mainsite = 'https://movie.naver.com'
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie_nation.naver'

    res = requests.get(url) # 네이버 영화 디렉토리 크롤링 할 곳.
    soup = BeautifulSoup(res.content, 'html.parser')

    movieList = soup.select('#old_content > dl.directory_item')


    sql = "INSERT INTO image (id, image) VALUES(%s, %s);"        

    TupleDataList = []



# *************************************************************************************************
    # 네이버 영화 디렉토리에 있는 각 나라의 영화 디렉토리 주소를 리스트에 저장
    movieDirectory = []

    for dl in movieList:
        
        # a = dl.select_one('dd > ul > li > a')["href"]
        li = dl.select('dd > ul > li')        
        
        for a in li:
            link = "https://movie.naver.com/movie/sdb/browsing/"
            link += a.select_one('a')['href']
            movieDirectory.append(link)
            
    # print(movieDirectory)    
# *************************************************************************************************
    
    
    url = movieDirectory[number]
    mainsite = 'https://movie.naver.com'
    
    
    # 반복 시작
    for url in movieDirectory[0:10]:
           

        flag = 0
        numb = 0
        while flag != 1:
            
            res = requests.get(url) # 네이버 현재 상영중인 영화 사이트 크롤링 할 곳.
            soup = BeautifulSoup(res.content, 'html.parser')
            
            print("현재 url : " + url)

            # *************************************************************************************************

            # 그 나라의 영화 디렉토리들 에서 사이트 들어가서 title 정보 출력 
            # url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?nation=GR'

            res = requests.get(url) # 네이버 영화 디렉토리 크롤링 할 곳.
            soup = BeautifulSoup(res.content, 'html.parser')

            movieList = soup.select('#old_content > ul > li')
                
            url2 = ''
            for li in movieList:
                ewew = li.select_one('a')['href']
                url2 = mainsite + ewew
                    
                res2 = requests.get(url2) # 네이버 영화 디렉토리 크롤링 할 곳.
                soup2 = BeautifulSoup(res2.content, 'html.parser')


                movie_id = int(url2.split('=')[1])
                # 각 영화 country
                photou = url2.replace('basic','photoView')
                print(photou)
                url3 = photou
                res3 = requests.get(url3) # 네이버 영화 디렉토리 크롤링 할 곳.
                soup3 = BeautifulSoup(res3.content, 'html.parser')
                choose = soup3.select_one('#photo_area > div > div.list_area._list_area > div > ul').find_all('li')
                image=''
                
                print(len(choose))
                for x in range(len(choose)):
                    print(choose[x].select_one('img')['src'])
                    image = choose[x].select_one('img')['src']
                    DataList = (movie_id, image)
                    TupleDataList.append(DataList)
                print("------")
                    
                
                # print(title) # 확인용 출력
                
                
                # 2개씩 Excute
                if len(TupleDataList)%2 == 0:
                    cur.executemany(sql, TupleDataList)
                    conn.commit()
                    TupleDataList = []
            # *************************************************************************************************
            try:
        
                # 다음 페이지 찾기
                # print(url) #현재 페이지 출력
                abc = soup.select_one('#old_content > div.pagenavigation > table > tr > td.next > a')['href']
                # print(abc)
                url = mainsite + abc
                # numb = (numb + 1)
                # print(numb)
                # print("페이지")
                
                    
            
            # 다음 페이지가 더 없으면 작동
            except:
                print("**********************페이지가 더 없습니다.****************")
                flag = 1
        
    
        
        
    # 혹시 1개가 남아있다면 나머지 1개도 Excute
    if TupleDataList:
        cur.executemany(sql, TupleDataList)
        conn.commit()
        
    print("성공")
    conn.commit()
    close_db(conn, cur)  



    

    
if __name__=='__main__':
    crawl_naver_movie(1)