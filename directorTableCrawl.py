from itertools import count
from tkinter.messagebox import NO
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


    sql = "INSERT INTO director (director_id, name, birth, image) VALUES(%s, %s, %s, %s);"        
    sql2 = "INSERT INTO director_country (director_id, country) VALUES(%s, %s);"        


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
    for url in movieDirectory:
           

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
                    
                #content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.dir_obj > div > a

                res2 = requests.get(url2) # 네이버 영화 디렉토리 크롤링 할 곳.
                soup2 = BeautifulSoup(res2.content, 'html.parser')


                try:
                    directorlink = soup2.select_one("#content > div.article > div.section_group.section_group_frst > div > div > div.dir_obj > div > a")['href']
                except:
                    directorlink = None
                # directorName = soup2.select_one("#content > div.article > div.section_group.section_group_frst > div > div > div.dir_obj > div > a").text
                #content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div > div.dir_obj > div
                # print(url3)
                if(directorlink != None):
                    url3 = mainsite+directorlink

                    # url3 = 'https://movie.naver.com/movie/bi/pi/basic.naver?code=148341'


                    res3 = requests.get(url3) # 감독 정보 url 들어감
                    soup3 = BeautifulSoup(res3.content, 'html.parser')
                    
                    
                    
                    # 감독 이름
                    try:
                        directorName = soup3.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > h3 > a').text
                    except:
                        directorName = None
                    # 감독 번호
                    try:
                        director_id = int(url3.split('=')[1])
                    except:
                        director_id = None    

                    # 출생
                    try:
                        birth = (soup3.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step5').next_sibling.next_sibling).text.replace("\t", "").replace("\n", "").split('/')[0]
                        if(birth[1] != '1' and birth[1] != '~'):
                            birth = None
                    except:
                        birth = None

                    # 나라
                    countryList = []
                    try:
                        country = (soup3.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step5').next_sibling.next_sibling).text.replace("\t", "").replace("\n", "").split('/')[1]
                        countryList = country.split(',')
                        # for i in countryList:
                            # print(i)
                    except:
                        try:
                            country = (soup3.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step5').next_sibling.next_sibling).text.replace("\t", "").replace("\n", "")
                            if(country[1] == '1' or country[1] == '~'):
                                country = None
                            
                            try:
                                countryList = country.split(',')
                                # for i in countryList:
                                #     print(i)
                            except:
                                country = (soup3.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step5').next_sibling.next_sibling).text.replace("\t", "").replace("\n", "")
                                if(country[1] == '1' or country[1] == '~'):
                                    country = None

                        except:
                            country = None

                    try:
                        for coun in countryList:
                            DataList2 = (director_id, coun)
                            TupleDataList2.append(DataList2)
                            try:
                                if len(TupleDataList2)%1 == 0:
                                    cur.executemany(sql2, TupleDataList2)
                                    conn.commit()
                                    TupleDataList2 = []
                            except:
                                TupleDataList2 = []                            

                    except:
                        countryList = []

                    # 작품  TODO ->>> 필모그래피에서 따로 빼내서 새로운 감독작품 테이블로 만들것.
                    try:
                        work = (soup3.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step7').next_sibling.next_sibling).a.text
                    except:
                        work = None 
                    # 수상  TODO ->>> 수상정보 따로 테이블로 빼내기.
                    try:
                        prime = (soup3.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step8').next_sibling.next_sibling).text.replace("\n", "").replace("\t", "")
                    except:
                        prime = None


                    # 감독 사진
                    try:
                        image = soup3.select_one('#content > div.article > div.mv_info_area > div.poster > img')['src']
                    except:
                        image = None

                    DataList = (director_id, directorName, birth, image)
                    TupleDataList.append(DataList)
                    
                    # print(directorName)
                    # print(image)
                else:
                    print("감독 세부 정보 없음")

                
                    
                # # 각 영화 title
                # try:
                #     title = soup2.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
                # except:
                #     title = None
                    
                    
                # # 각 영화 고유번호
                # movie_id = int(url2.split('=')[1])
                
                
                # 각 영화를 제작한 나라
                    
                # country.split(':')[0]      
                
                # try:
                #     country = soup2.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p').text.replace(" ", "").replace("\n", "/").replace("\r", "").replace("\t", "").replace('////', "").replace('///', ':').replace("//", ':').replace('/', '')[1:]

                # except:
                #     country = None


                
                # print(title) # 확인용 출력
                
                # 10개씩 Excute
                
                try:
                    if len(TupleDataList)%1 == 0:
                        cur.executemany(sql, TupleDataList)
                        conn.commit()
                        TupleDataList = []
                except:
                    TupleDataList = []
                    # print("DB excute fault 똑같은 것이 또 들어옴")
                    
            
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
                print("*****************페이지가 더 없습니다.****************")
                flag = 1
        
    
        
        
    # 혹시 1개가 남아있다면 나머지 1개도 Excute
    # if TupleDataList:
    #     cur.executemany(sql, TupleDataList)
    #     conn.commit()
        
    print("성공")
    conn.commit()
    close_db(conn, cur)  



    

    
if __name__=='__main__':
    crawl_naver_movie(1)