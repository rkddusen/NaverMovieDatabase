from dataclasses import dataclass
from itertools import count
import requests
from bs4 import BeautifulSoup
import pymysql


# 데이터베이스 네이버 영화 크롤링 작업 DB로 전송.


# db 열기
def open_db():
    conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', passwd='root', db='practice', charset='utf8')
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


    sql = "INSERT INTO movie (movie_id, title, title2, opening_date, playing_time, audience_score, audience_count, netizen_score, netizen_count, journalist_score, journalist_count, open_rating_korea, open_rating_overseas, total_count, img) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"        

    TupleDataList = []

# 삭제하기
    index = 5

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
                # url2 = "https://movie.naver.com/movie/bi/mi/point.naver?code=62266"
                # url2 = "https://movie.naver.com/movie/bi/mi/point.naver?code=196576"
                # url2 = "https://movie.naver.com/movie/bi/mi/point.naver?code=191646"
                # url2 = "https://movie.naver.com/movie/bi/mi/point.naver?code=15605"
                    
                res2 = requests.get(url2) # 네이버 영화 디렉토리 크롤링 할 곳.
                soup2 = BeautifulSoup(res2.content, 'html.parser')
                    
                # 각 영화 title
                try:
                    title = soup2.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
                except:
                    title = None
                    
                    
                # 각 영화 고유번호
                movie_id = int(url2.split('=')[1])


                # 영화 부제목(영어제목?)
                try:                
                    title2 = soup2.select_one('#content > div.article > div.mv_info_area > div.mv_info > strong').text
                except:
                    title2 = None


                # 개요 따오기 개봉 날짜
                choose = soup2.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p').find_all('a')
                opening_date=''
                
                try:
                    for x in range(len(choose)):
                        if("open" in choose[x]["href"]):
                            opening_date += choose[x].text
                    opening_date = opening_date.replace(" ", "").replace(".","-")
                    if(opening_date == ""):
                        opening_date = None
                except:
                    opening_date = None

                # .text.replace("\n", "").replace("\r", "").replace("\t", "")
                choose = soup2.select('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span')

                try:
                    for span in choose:    
                        minute = span.text.replace("\n", "").replace("\r", "").replace("\t", "")
                        if(minute.find("분") > 0):
                            # print(playing_time)
                            playing_time = int(minute.replace(" ", "").replace("분", ""))
                except:
                    playing_time = None



                # 평점 가져오기.
                url3 = mainsite + ewew.replace('basic', 'point')
                # url3 = mainsite + "/movie/bi/mi/point.naver?code=196854"    
                res3 = requests.get(url3) # 네이버 영화 디렉토리 크롤링 할 곳.
                soup3 = BeautifulSoup(res3.content, 'html.parser')


                # 관람객 평점
                try:
                    em_text = ""
                    div = soup3.select('#actual_point_tab_inner > div > em')
                    for em in div:
                        em_text += em.text

                    audience_score = float(em_text)
                except:
                    audience_score = None

                # 관람객 평점 참여자 수
                try:
                    audience_count = int(soup3.select_one('#actual_point_tab_inner > span > em').text.replace(",", ""))
                except:
                    audience_count = None


                # 네티즌 평점
                try:
                    em_text = ""
                    div = soup3.select('#netizen_point_tab_inner > em')
                    for em in div:
                        em_text += em.text

                    netizen_score = float(em_text)
                except:
                    netizen_score = None
                # print(netizen_score)

                # 네티즌 평점 참여자 수
                try:
                    netizen_count = int(soup3.select_one('#graph_area > div.grade_netizen > div.title_area.grade_tit > div.sc_area > span > em').text.replace(",", ""))
                except:
                    netizen_count = None



                # 저널리스트 평점
                try:
                    em_text = ""
                    div = soup3.select('#content > div.article > div.section_group.section_group_frst > div.obj_section > div > div.title_area > div > em')
                    for em in div:
                        em_text += em.text

                    journalist_score = float(em_text)
                except:
                    journalist_score = None

                # 저널리스트 평점 참여자 수
                try:
                    journalist_count = int(soup3.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section > div > div.title_area > span > em').text.replace(",", ""))
                except:
                    journalist_count = None


                # 개봉 등급
                open_rating_korea = None
                open_rating_overseas = None
                
                try:
                    open_rating = soup2.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step4').next_sibling.next_sibling.text.replace("\n", "").replace("\r", "").replace("\t", "").replace("도움말", "")
                    try:
                        open_rating_korea = open_rating.split(" [해외]")[0]
                        if(open_rating_korea.find("국내") < 0):
                            open_rating_korea = None
                        else:
                            open_rating_korea = open_rating_korea.replace("[국내] ", "")
                    except:
                        open_rating_korea = None

                    try:
                        open_rating_overseas = open_rating.split("[해외]")[1].replace(" ", "")
                    except:
                        open_rating_overseas = None            
                except:
                    pass
                

                # 누적 관객
                try:
                    total_count = (soup2.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step9').next_sibling.next_sibling).div.p
                    total_count.find('span').decompose()
                    total_count = int(total_count.text.replace("명", "").replace(",", ""))
                except:
                    total_count = None


                # 영화 이미지
                try:
                    img = soup2.select_one('#content > div.article > div.mv_info_area > div.poster > a > img')['src']
                except:
                    img = None



                # choose = soup2.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p').find_all('span')
                # print(choose)
                # for x in range(len(choose)):
                #     if("open" in choose[x]["href"]):
                #         playing_time += choose[x].text
                # playing_time = playing_time.replace(" ", "").replace(".","-")


                # print(title) # 확인용 출력
                # DataList = (type(movie_id), type(title), type(title2), type(opening_date), type(playing_time), type(audience_score), type(audience_count), type(netizen_score), type(netizen_count), type(journalist_score), type(journalist_count), type(open_rating_korea), type(open_rating_overseas), type(total_count), type(img))
                DataList = (movie_id, title, title2, opening_date, playing_time, audience_score, audience_count, netizen_score, netizen_count, journalist_score, journalist_count, open_rating_korea, open_rating_overseas, total_count, img)
                # DataList = (index, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
                # print(DataList)
                # index = index +1
                TupleDataList.append(DataList)
                # print(TupleDataList)
                
                try:
                    # 2개씩 Excute
                    # sql = "INSERT INTO movie (movie_id, title, title2, opening_date, playing_time, audience_score, audience_count, netizen_score, netizen_count, journalist_score, journalist_count, open_rating_korea, open_rating_overseas, total_count, img) VALUES(2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);"
                    if len(TupleDataList)%10 == 0:
                        cur.executemany(sql, TupleDataList)
                        conn.commit()
                        TupleDataList = []
                except:
                    TupleDataList = []
                    print("띠용")
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