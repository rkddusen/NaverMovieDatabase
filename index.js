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
// const index = fs.readFileSync('./index.ejs', 'utf8');
// server.post("/title", (req, res) => {
//     search = req.body.text;
//     let sql = 'SELECT * FROM movie where title LIKE "%' + search + '%";';
//     let sqll = 'SELECT COUNT(*) AS number FROM movie where title like "%' + search + '%";';
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
//                 let id = new Array();
//                 let title = new Array();
//                 let movie_rate = new Array();
//                 let netizen_rate = new Array();
//                 let netizen_count = new Array();
//                 let journalist_score = new Array();
//                 let journalist_count = new Array();
//                 let playing_time = new Array();
//                 let opening_date = new Array();
//                 let image = new Array();
//                 for (var i in rows[0]) {
//                     id[i] = dataResult[i].id
//                     title[i] = dataResult[i].title
//                     movie_rate[i] = dataResult[i].movie_rate
//                     netizen_rate[i] = dataResult[i].netizen_rate?dataResult[i].netizen_rate:0
//                     netizen_count[i] = dataResult[i].netizen_count?dataResult[i].netizen_count:0
//                     journalist_score[i] = dataResult[i].journalist_score?dataResult[i].journalist_score:0
//                     journalist_count[i] = dataResult[i].journalist_count?dataResult[i].journalist_count:0
//                     playing_time[i] = dataResult[i].playing_time
//                     opening_date[i] = dataResult[i].opening_date
//                     image[i] = dataResult[i].image
//                 }//데이터 생성
//                 var page = ejs.render(index, {
//                     title: title,
//                     id:id,
//                     movie_rate:movie_rate,
//                     netizen_rate:netizen_rate,
//                     netizen_count:netizen_count,
//                     journalist_score:journalist_score,
//                     journalist_count:journalist_count,
//                     playing_time:playing_time,
//                     opening_date:opening_date,
//                     image:image,
//                     number:number
//                 });
//                 //응답
//                 console.log(title);
//                 res.send(page);
//             }
//         }
//     );
// });

const index = fs.readFileSync('./index.ejs', 'utf8');
server.get("/title", (req, res) => {
    let titurl = req.url;
    let query = url.parse(titurl,true).query.text;
    console.log(query);
    let sql = 'SELECT * FROM movie where title LIKE "%' + query + '%";';
    let sqll = 'SELECT COUNT(*) AS number FROM movie where title like "%' + query + '%";';
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
                let img = new Array();
                for (var i in rows[0]) {
                    movie_id[i] = dataResult[i].movie_id;
                    title[i] = dataResult[i].title;
                    title2[i] = dataResult[i].title2;
                    opening_date[i] = dataResult[i].opening_date?dataResult[i].opening_date:"-";
                    playing_time[i] = dataResult[i].playing_time?dataResult[i].playing_time:"-분";
                    audience_score[i] = dataResult[i].audience_score?dataResult[i].audience_score:"-";
                    audience_count[i] = dataResult[i].audience_count?dataResult[i].audience_count:0;
                    netizen_score[i] = dataResult[i].netizen_score?dataResult[i].netizen_score:"-";
                    netizen_count[i] = dataResult[i].netizen_count?dataResult[i].netizen_count:0;
                    journalist_score[i] = dataResult[i].journalist_score?dataResult[i].journalist_score:"-";
                    journalist_count[i] = dataResult[i].journalist_count?dataResult[i].journalist_count:0;
                    open_rating_korea[i] = dataResult[i].open_rating_korea?dataResult[i].open_rating_korea:"-";
                    open_rating_overseas[i] = dataResult[i].open_rating_overseas?dataResult[i].open_rating_overseas:"-";
                    img[i] = dataResult[i].img;
                }//데이터 생성
                var page = ejs.render(index, {
                    movie_id:movie_id,
                    title: title,
                    title2: title2,
                    opening_date:opening_date,
                    playing_time:playing_time,
                    audience_score:audience_score,
                    audience_count:audience_count,
                    netizen_score:netizen_score,
                    netizen_count:netizen_count,
                    journalist_score:journalist_score,
                    journalist_count:journalist_count,
                    open_rating_korea:open_rating_korea,
                    open_rating_overseas:open_rating_overseas,
                    img:img,
                    number:number
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
    let queryId = url.parse(idurl,true).query.id;
    let sql = 'SELECT * FROM movie where movie_id = ' + queryId + ';';
    connection.query(sql,
        function (error, rows, fields) {
            if (error) {
                console.log(error);
            }
            else {

                //검색 결과 화면에 영화제목, 관람객 평점, 관람객 수, 네티즌 평점, 네티즌 수, 평론가 평점, 평론가 수,
                //상영시간, 개봉일을 담을 예정
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
                let img = '';
                for (var i in rows) {
                    movie_id = rows[i].movie_id;
                    title = rows[i].title;
                    title2 = rows[i].title2;
                    opening_date = rows[i].opening_date?rows[i].opening_date:"-";
                    playing_time = rows[i].playing_time?rows[i].playing_time:"-분";
                    audience_score = rows[i].audience_score?rows[i].audience_score:"-";
                    audience_count = rows[i].audience_count?rows[i].audience_count:0;
                    netizen_score = rows[i].netizen_score?rows[i].netizen_score:"-";
                    netizen_count = rows[i].netizen_count?rows[i].netizen_count:0;
                    journalist_score = rows[i].journalist_score?rows[i].journalist_score:"-";
                    journalist_count = rows[i].journalist_count?rows[i].journalist_count:0;
                    open_rating_korea = rows[i].open_rating_korea?rows[i].open_rating_korea:"-";
                    open_rating_overseas = rows[i].open_rating_overseas?rows[i].open_rating_overseas:"-";
                    img = rows[i].img;
                }//데이터 생성
                var page = ejs.render(basic, {
                    movie_id:movie_id,
                    title: title,
                    title2: title2,
                    opening_date:opening_date,
                    playing_time:playing_time,
                    audience_score:audience_score,
                    audience_count:audience_count,
                    netizen_score:netizen_score,
                    netizen_count:netizen_count,
                    journalist_score:journalist_score,
                    journalist_count:journalist_count,
                    open_rating_korea:open_rating_korea,
                    open_rating_overseas:open_rating_overseas,
                    img:img
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