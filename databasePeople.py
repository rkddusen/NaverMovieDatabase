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
    url = 'https://movie.naver.com/movie/sdb/browsing/bpeople_nation.naver'

    res = requests.get(url) # 네이버 영화 디렉토리 크롤링 할 곳.
    soup = BeautifulSoup(res.content, 'html.parser')

    movieList = soup.select('#old_content > dl.directory_item')


    sql = "INSERT INTO actor (actor_id, name, eng_name, birth, d_name, body, image) VALUES(%s, %s, %s, %s, %s, %s, %s);"        
    #sql2 = "INSERT INTO cast (movie_id, person_id, total_role, role) VALUES(%s, %s, %s, %s);"        


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
    for url in movieDirectory[0:]:
           

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
                ewew = li.select_one('a')['href']
                # ewew = li.select_one('a')['href'].replace("basic", "detail")
                url2 = mainsite + ewew
                # print(url2)
                # ewew = /movie/bi/mi/basic.naver?code=137202
                

                res2 = requests.get(url2) # 네이버 영화 디렉토리 크롤링 할 곳.
                soup2 = BeautifulSoup(res2.content, 'html.parser')
    

                try:
                    actorName=soup2.select_one("#content > div.article > div.mv_info_area > div.mv_info.character > h3 > a").text
                except:
                    actorName=None
                
                try:
                    actor_eng=soup2.select_one("#content > div.article > div.mv_info_area > div.mv_info.character > strong").text.replace('\r','').replace('\n','').replace('\t','')
                except:
                    actor_eng=None
                
                try:
                    actor_id=int(url2.split('=')[1])
                except:
                    actor_id=None

                d_name=None
                body=None

                tbody=soup2.select("#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > table > tbody > tr")
                for tr in tbody:
                    th=tr.select('th')
                    for idx, img in enumerate(th):
                        try:
                            alt=img.select_one('img')['alt']
                            if(alt=="다른이름"):
                                try:
                                    d_name=th[idx].next_sibling.next_sibling.text
                                except:
                                    d_name=None
                            elif(alt=="신체"):
                                try:
                                    body=th[idx].next_sibling.next_sibling.text.replace(' ','').replace('\t','').replace('\n','').replace('\r','')
                                except:
                                    body=None        
                        except:
                            pass
                                
                            

                try:
                    image=soup2.select_one("#content > div.article > div.mv_info_area > div.poster > img")['src']
                except:
                    image=None

                try:
                    birth=(soup2.select_one("#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step5")).next_sibling.next_sibling.text.replace('\r','').replace('\n','').replace('\t','').split('/')[0]
                    if(birth[0]!='1' and birth[0]!='2' and birth[0]!='~'):
                        birth=None
                except:
                    birth=None

                DataList = (actor_id, actorName, actor_eng, birth, d_name, body, image)
                    
                    
                TupleDataList.append(DataList)

                # print(DataList)

            # else:
            #     print("링크가 없는 배우")

                try:
                    if len(TupleDataList)%10 == 0:
                        cur.executemany(sql, TupleDataList)
                        conn.commit()
                        TupleDataList = []
                except:
                    TupleDataList = []
                    print("중복 값은 뺍니다.")
                
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