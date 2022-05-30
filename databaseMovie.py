from itertools import count
import requests
from bs4 import BeautifulSoup
import pymysql


# 데이터베이스 네이버 영화 크롤링 작업 DB로 전송.


# db 열기
def open_db():
    conn = pymysql.connect(host='localhost', port=3307, user='root', passwd='root', db='practice', charset='utf8')
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


    sql = "INSERT INTO movies (movie_id, title, country) VALUES(%s, %s, %s);"        

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
    for url in movieDirectory[64:]:
           

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
                    
                # 각 영화 title
                try:
                    title = soup2.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
                except:
                    title = None
                    
                    
                # 각 영화 고유번호
                movie_id = int(url2.split('=')[1])
                
                
                # 각 영화를 제작한 나라
                    
                # country.split(':')[0]      
                
                try:
                    country = soup2.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p').text.replace(" ", "").replace("\n", "/").replace("\r", "").replace("\t", "").replace('////', "").replace('///', ':').replace("//", ':').replace('/', '')[1:]

                except:
                    country = None


                
                # print(title) # 확인용 출력
                DataList = (movie_id, title, country)
                TupleDataList.append(DataList)
                
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