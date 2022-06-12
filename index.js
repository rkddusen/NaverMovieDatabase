//모듈을 추출
const express = require("express"); http = require('http'), path = require('path');

//express 미들웨어 불러오기
var static = require('serve-static'), bodyParser = require('body-parser'); var session = require('express-session');
const ejs = require('ejs');
const fs = require('fs');
const url = require('url');
const request = require('request');
const querystring = require('querystring');
const { rawListeners } = require("process");
const { text } = require("express");

//서버를 생성, express 객체 생성
const server = express();
var router = express.Router();

//기본 속성 설정
server.set('port', process.env.PORT || 8080);
server.set('hostname', '127.0.0.1');

//정적(css,일부js,사진)파일을 사용 가능하게끔
server.use(express.static(__dirname));
server.use(bodyParser.urlencoded({ extended: false }));
server.use(bodyParser.json());

const mysql = require('./database')();

const connection = mysql.init();

mysql.db_open(connection);
//db 데이터를 받을 변수

//request 이벤트 리스너 설정//라우터 설정
server.get("/", (req, res) => {

    res.sendFile(__dirname + "/index.html");
});
let search = '';
// server.get("/title", (req, res) => {
//     let titurl = req.url;
//     let queryTitle = url.parse(titurl, true).query.text;
//     let queryOrder = url.parse(titurl, true).query.order;
//     if(queryOrder=='1'){
//         queryOrder = "title"
//     }
//     else if(queryOrder=='2'){
//         queryOrder = "title desc"
//     }
//     else if(queryOrder=='3'){
//         queryOrder = "opening_date"
//     }
//     else if(queryOrder=='4'){
//         queryOrder = "opening_date desc"
//     }
//     else if(queryOrder=='5'){
//         queryOrder = "playing_time"
//     }
//     else if(queryOrder=='6'){
//         queryOrder = "playing_time desc"
//     }
    
//     let sql = 'SELECT * FROM movie where title LIKE "%' + queryTitle + '%" ORDER BY ' + queryOrder + ';';
//     let sqll = 'SELECT COUNT(*) AS number FROM movie where title like "%' + queryTitle + '%";';
//     connection.query(sql + sqll,
//         function (error, rows, fields) {
//             if (error) {
//                 console.log(error);
//             }
//             else {
//                 let dataResult = rows[0];
//                 let countResult = rows[1];
//                 let number = countResult[0].number;

//                 //검색 결과 화면에 영화제목, 관람객 평점, 관람객 수, 네티즌 평점, 네티즌 수, 평론가 평점, 평론가 수,
//                 //상영시간, 개봉일을 담을 예정
//                 let movie_id = new Array();
//                 let title = new Array();
//                 let title2 = new Array();
//                 let opening_date = new Array();
//                 let playing_time = new Array();
//                 let audience_score = new Array();
//                 let audience_count = new Array();
//                 let netizen_score = new Array();
//                 let netizen_count = new Array();
//                 let journalist_score = new Array();
//                 let journalist_count = new Array();
//                 let open_rating_korea = new Array();
//                 let open_rating_overseas = new Array();
//                 let img = new Array();
//                 for (var i in rows[0]) {
//                     movie_id[i] = dataResult[i].movie_id;
//                     title[i] = dataResult[i].title;
//                     title2[i] = dataResult[i].title2;
//                     opening_date[i] = dataResult[i].opening_date ? dataResult[i].opening_date : "-";
//                     playing_time[i] = dataResult[i].playing_time ? dataResult[i].playing_time : "-분";
//                     audience_score[i] = dataResult[i].audience_score ? dataResult[i].audience_score : "-";
//                     audience_count[i] = dataResult[i].audience_count ? dataResult[i].audience_count : 0;
//                     netizen_score[i] = dataResult[i].netizen_score ? dataResult[i].netizen_score : "-";
//                     netizen_count[i] = dataResult[i].netizen_count ? dataResult[i].netizen_count : 0;
//                     journalist_score[i] = dataResult[i].journalist_score ? dataResult[i].journalist_score : "-";
//                     journalist_count[i] = dataResult[i].journalist_count ? dataResult[i].journalist_count : 0;
//                     open_rating_korea[i] = dataResult[i].open_rating_korea ? dataResult[i].open_rating_korea : "-";
//                     open_rating_overseas[i] = dataResult[i].open_rating_overseas ? dataResult[i].open_rating_overseas : "-";
//                     img[i] = dataResult[i].img;
//                 }//데이터 생성
//                 var page = ejs.render(index, {
//                     movie_id: movie_id,
//                     title: title,
//                     title2: title2,
//                     opening_date: opening_date,
//                     playing_time: playing_time,
//                     audience_score: audience_score,
//                     audience_count: audience_count,
//                     netizen_score: netizen_score,
//                     netizen_count: netizen_count,
//                     journalist_score: journalist_score,
//                     journalist_count: journalist_count,
//                     open_rating_korea: open_rating_korea,
//                     open_rating_overseas: open_rating_overseas,
//                     img: img,
//                     number: number
//                 });
//                 //응답
//                 res.send(page);
//             }
//         }
//     );
// });

const index = fs.readFileSync('./index.ejs', 'utf8');

server.get("/search", (req, res) => {
    let geturl = req.url;
    let queryName = url.parse(geturl, true).query.name;
    let queryText = url.parse(geturl, true).query.text;
    let queryOrder = url.parse(geturl, true).query.order;
    if(queryOrder=='1'){
        queryOrder = "title"
    }
    else if(queryOrder=='2'){
        queryOrder = "title desc"
    }
    else if(queryOrder=='3'){
        queryOrder = "opening_date"
    }
    else if(queryOrder=='4'){
        queryOrder = "opening_date desc"
    }
    else if(queryOrder=='5'){
        queryOrder = "playing_time"
    }
    else if(queryOrder=='6'){
        queryOrder = "playing_time desc"
    }
    else if(queryOrder=='7'){
        queryOrder = "audience_score"
    }
    else if(queryOrder=='8'){
        queryOrder = "audience_score desc"
    }
    else if(queryOrder=='9'){
        queryOrder = "total_count"
    }
    else if(queryOrder=='10'){
        queryOrder = "total_count desc"
    }
    let sql=''
    let sqll=''
    //무슨 기준으로 검색했는지
    if(queryName=='title'){
        sql = 'SELECT * FROM movie where title LIKE "%' + queryText + '%" ORDER BY ' + queryOrder + ';';
        sqll = 'SELECT COUNT(*) AS number FROM movie where title like "%' + queryText + '%";';
    }
    else if(queryName=='genre'){
        sql = 'SELECT * FROM movie, genre where movie.movie_id = genre.movie_id and genre.genre = "' + queryText + '" ORDER BY movie.' + queryOrder + ';';
        sqll = 'SELECT COUNT(*) AS number FROM movie, genre where movie.movie_id = genre.movie_id and genre.genre = "' + queryText + '";';
    }
    else if(queryName=='country'){
        sql = 'SELECT * FROM movie, country where movie.movie_id = country.movie_id and country.country = "' + queryText + '" ORDER BY movie.' + queryOrder + ';';
        sqll = 'SELECT COUNT(*) AS number FROM movie, country where movie.movie_id = country.movie_id and country.country = "' + queryText + '";';
    }
    connection.query(sql + sqll,
        function (error, rows, fields) {
            if (error) {
                console.log(error);
            }
            else {
                let dataResult = rows[0];
                let countResult = rows[1];
                let number = countResult[0].number;
                //검색 결과 화면에 영화제목, 관람객 평점, 관람객 수, 네티즌 평점, 네티즌 수, 평론가 평점, 평론가 수,
                //상영시간, 개봉일을 담을 예정
                let movie_id = new Array();
                let title = new Array();
                let title2 = new Array();
                let opening_date = new Array();
                let playing_time = new Array();
                let audience_score = new Array();
                let audience_count = new Array();
                let netizen_score = new Array();
                let netizen_count = new Array();
                let journalist_score = new Array();
                let journalist_count = new Array();
                let open_rating_korea = new Array();
                let open_rating_overseas = new Array();
                let total_count = new Array();
                let img = new Array();
                for (var i in rows[0]) {
                    movie_id[i] = dataResult[i].movie_id;
                    title[i] = dataResult[i].title;
                    title2[i] = dataResult[i].title2;
                    opening_date[i] = dataResult[i].opening_date ? dataResult[i].opening_date : "-";
                    playing_time[i] = dataResult[i].playing_time ? dataResult[i].playing_time : "-분";
                    audience_score[i] = dataResult[i].audience_score ? dataResult[i].audience_score : "-";
                    audience_count[i] = dataResult[i].audience_count ? dataResult[i].audience_count : 0;
                    netizen_score[i] = dataResult[i].netizen_score ? dataResult[i].netizen_score : "-";
                    netizen_count[i] = dataResult[i].netizen_count ? dataResult[i].netizen_count : 0;
                    journalist_score[i] = dataResult[i].journalist_score ? dataResult[i].journalist_score : "-";
                    journalist_count[i] = dataResult[i].journalist_count ? dataResult[i].journalist_count : 0;
                    open_rating_korea[i] = dataResult[i].open_rating_korea ? dataResult[i].open_rating_korea : "-";
                    open_rating_overseas[i] = dataResult[i].open_rating_overseas ? dataResult[i].open_rating_overseas : "-";
                    total_count[i] = dataResult[i].total_count ? dataResult[i].total_count : 0;
                    img[i] = dataResult[i].img?dataResult[i].img:"https://ssl.pstatic.net/static/movie/2012/06/dft_img203x290.png";
                }//데이터 생성
                var page = ejs.render(index, {
                    movie_id: movie_id,
                    title: title,
                    title2: title2,
                    opening_date: opening_date,
                    playing_time: playing_time,
                    audience_score: audience_score,
                    audience_count: audience_count,
                    netizen_score: netizen_score,
                    netizen_count: netizen_count,
                    journalist_score: journalist_score,
                    journalist_count: journalist_count,
                    open_rating_korea: open_rating_korea,
                    open_rating_overseas: open_rating_overseas,
                    total_count:total_count,
                    img: img,
                    number: number
                });
                //응답
                res.send(page);
            }
        }
    );
});





const basic = fs.readFileSync('./basic.ejs', 'utf8');
server.get("/movie", (req, res) => {
    let idurl = req.url;
    let queryId = url.parse(idurl, true).query.id;
    let sql = 'SELECT * FROM movie where movie_id = ' + queryId + ';';
    let sqlCast = 'SELECT * FROM cast, actor where cast.actor_id = actor.actor_id and movie_id = ' + queryId + ';';
    let sqlCountry = 'SELECT * FROM country where movie_id = ' + queryId + ';';
    let sqlGenre = 'SELECT * FROM genre where movie_id = ' + queryId + ';';
    connection.query(sql+sqlCast+sqlCountry+sqlGenre,
        function (error, rows, fields) {
            if (error) {
                console.log(error);
            }
            else {
                let movieResult = rows[0];
                let castResult = rows[1];
                let countryResult = rows[2];
                let genreResult = rows[3];
                //검색 결과 화면에 영화제목, 관람객 평점, 관람객 수, 네티즌 평점, 네티즌 수, 평론가 평점, 평론가 수,
                //상영시간, 개봉일을 담을 s예정
                let movie_id = 0;
                let title = '';
                let title2 = '';
                let opening_date = '';
                let playing_time = 0;
                let audience_score = 0.0;
                let audience_count = 0;
                let netizen_score = 0.0;
                let netizen_count = 0;
                let journalist_score = 0.0;
                let journalist_count = 0;
                let open_rating_korea = '';
                let open_rating_overseas = '';
                let total_count=0;
                let img = '';
                let actor_id =new Array();
                let total_role =new Array();
                let role =new Array();
                let name =new Array();
                let eng_name =new Array();
                let birth =new Array();
                let d_name =new Array();
                let body =new Array();
                let actor_img = new Array();

                let country = new Array();

                let genre =new Array();
                for (var i in rows[0]) {
                    movie_id = movieResult[i].movie_id;
                    title = movieResult[i].title;
                    title2 = movieResult[i].title2;
                    opening_date = movieResult[i].opening_date ? movieResult[i].opening_date : "-";
                    playing_time = movieResult[i].playing_time ? movieResult[i].playing_time : "-분";
                    audience_score = movieResult[i].audience_score ? movieResult[i].audience_score : "-";
                    audience_count = movieResult[i].audience_count ? movieResult[i].audience_count : 0;
                    netizen_score = movieResult[i].netizen_score ? movieResult[i].netizen_score : "-";
                    netizen_count = movieResult[i].netizen_count ? movieResult[i].netizen_count : 0;
                    journalist_score = movieResult[i].journalist_score ? movieResult[i].journalist_score : "-";
                    journalist_count = movieResult[i].journalist_count ? movieResult[i].journalist_count : 0;
                    open_rating_korea = movieResult[i].open_rating_korea ? movieResult[i].open_rating_korea : "-";
                    open_rating_overseas = movieResult[i].open_rating_overseas ? movieResult[i].open_rating_overseas : "-";
                    total_count = movieResult[i].total_count ? movieResult[i].total_count : 0;
                    img = movieResult[i].img?movieResult[i].img:"https://ssl.pstatic.net/static/movie/2012/06/dft_img203x290.png";
                }//데이터 생성
                // for(var j in rows[1]){
                //     director[j]=directorResult[j].director;
                // }
                
                for(var h in rows[1]){
                    actor_id[h]=castResult[h].actor_id;
                    total_role[h]=castResult[h].total_role?castResult[h].total_role:"-";
                    role[h]=castResult[h].role?castResult[h].role:"-";
                    name[h] =castResult[h].name?castResult[h].name:"-";
                    eng_name[h] =castResult[h].eng_name?castResult[h].eng_name:"-";
                    birth[h] =castResult[h].birth?castResult[h].birth:"-";
                    d_name[h] =castResult[h].d_name?castResult[h].d_name:"-";
                    body[h] =castResult[h].body?castResult[h].body:"-";
                    actor_img[h] = castResult[h].image?castResult[h].image:"https://movie.naver.com/movie/bi/pi/basic.naver?code=379173";
                }
                for(var j in rows[2]){
                    country[j] = countryResult[j].country;
                }
                for(var k in rows[3]){
                    genre[k] = genreResult[k].genre;
                }
                var page = ejs.render(basic, {
                    movie_id: movie_id,
                    title: title,
                    title2: title2,
                    opening_date: opening_date,
                    playing_time: playing_time,
                    audience_score: audience_score,
                    audience_count: audience_count,
                    netizen_score: netizen_score,
                    netizen_count: netizen_count,
                    journalist_score: journalist_score,
                    journalist_count: journalist_count,
                    open_rating_korea: open_rating_korea,
                    open_rating_overseas: open_rating_overseas,
                    total_count:total_count,
                    img: img,

                    actor_id:actor_id,
                    total_role:total_role,
                    role:role,
                    name,
                    eng_name,
                    birth,
                    d_name,
                    body,
                    actor_img,

                    country:country,
                    genre:genre
                });
                //응답
                res.send(page);
            }
        }
    );
});

http.createServer(server).listen(server.get('port'), server.get('host'), () => {
    console.log('Express server running at ' + server.get('hostname') + ':' + server.get('port'));
});