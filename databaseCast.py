from itertools import count
from tkinter.messagebox import NO
import requests
from bs4 import BeautifulSoup
import pymysql


# 데이터베이스 네이버 영화 크롤링 작업 DB로 전송.


# db 열기
def open_db():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='eeldhd4120', db='movie', charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    return conn, cur

#  db 닫기
def close_db(conn, cur):
    cur.close()
    conn.close()

def crawl_naver_movie(number):
    
    conn, cur = open_db()
    mainsite = 'https://movie.naver.com'
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie_nation.naver'

    res = requests.get(url) # 네이버 영화 디렉토리 크롤링 할 곳.
    soup = BeautifulSoup(res.content, 'html.parser')

    movieList = soup.select('#old_content > dl.directory_item')


    #sql = "INSERT INTO people (actor_id, name, eng_name, birth, information, image) VALUES(%s, %s, %s, %s, %s, %s);"        
    sql = "INSERT INTO cast (movie_id, actor_id, total_role, role) VALUES(%s, %s, %s, %s);"        


    TupleDataList = []
    TupleDataList2 = []

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
    for url in movieDirectory[63:64]:
           

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
                # 배우/제작진으로 이동
                ewew = li.select_one('a')['href'].replace("basic", "detail")
                url2 = mainsite + ewew
                # ewew = /movie/bi/mi/basic.naver?code=137202
                

                res2 = requests.get(url2) # 네이버 영화 디렉토리 크롤링 할 곳.
                soup2 = BeautifulSoup(res2.content, 'html.parser')

                movie_id = int(url2.split('=')[1])
                
            

                choose=soup2.select("#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li")
                
                for li in choose:
                    try:
                        actor_id=li.select_one("div > a")['href'].split('=')[1]
                    except:
                        actor_id=None

                    try:
                        total_role=li.select_one("div > div > p > em").text
                        
                    except:
                        total_role=None

                    try:
                        role=li.select_one("div > div > p.pe_cmt > span").text
                    except:
                        role=None

                    #print(actor_id, total_role, role)
                    DataList=(movie_id, actor_id, total_role, role)
                    TupleDataList.append(DataList)
                    
                
                if len(TupleDataList)%2 == 0:
                    cur.executemany(sql, TupleDataList)
                    conn.commit()
                    TupleDataList = []
            try:
        
                # 다음 페이지 찾기
                # print(url) #현재 페이지 출력
                abc = soup.select_one('#old_content > div.pagenavigation > table > tr > td.next > a')['href']
                # print(abc)
                url = mainsite + abc
                if(url=="https://movie.naver.com/movie/sdb/browsing/bmovie.naver?nation=US&page=2"):
                    url = "https://movie.naver.com/movie/sdb/browsing/bmovie.naver?nation=US&page=444"
                
                # numb = (numb + 1)
                # print(numb)
                # print("페이지")
                
                    
            
            # 다음 페이지가 더 없으면 작동
            except:
                print("**********************페이지가 더 없습니다.****************")
                flag = 1      

    try:
        if TupleDataList:
            cur.executemany(sql, TupleDataList)
            conn.commit()
    except:
        pass

    print("성공")
    conn.commit()
    close_db(conn, cur)

if __name__=='__main__':
     crawl_naver_movie(1)
                    