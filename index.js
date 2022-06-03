//모듈을 추출
const express = require("express"); http = require('http'), path = require('path');

//express 미들웨어 불러오기
var static = require('serve-static'), bodyParser = require('body-parser'); var session = require('express-session');
const ejs = require('ejs');
const fs = require('fs');
const { rawListeners } = require("process");
const { text } = require("express");

//서버를 생성, express 객체 생성
const server = express();
var router = express.Router();

//기본 속성 설정
server.set('port', process.env.PORT || 8080);
server.set('hostname', '127.0.0.1');

//정적(css,일부js,사진)파일을 사용 가능하게끔
server.use(express.static(__dirname + "/public"));
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
let search='';
const index = fs.readFileSync('./index.ejs', 'utf8');
server.post("/title", (req, res) => {
    search = req.body.text;
    let id = '';
    let title = '';
    let movie_rate = '';
    let netizen_rate = '';
    let netizen_count = '';
    let journalist_score = '';
    let scope = '';
    let playing_time = '';
    let sql='SELECT * FROM movie where title LIKE "%'+search+'%";';
    let sqll='SELECT COUNT(*) AS number FROM movie where title like "%'+search+'%";';
    connection.query(sql+sqll,
        function (error, rows, fields) {
            if (error) {
                console.log(error);
            }
            else {
                let dataResult=rows[0];
                let countResult=rows[1];
                let number = countResult[0].number;
                for (var i in rows[0]) {
                    title += dataResult[i].title+"/"+dataResult[i].id+"//"

                }//데이터 생성
                var page = ejs.render(index, {
                    title: title
                });
                //응답
                console.log(title);
                res.send(page);
            }
        }
    );
});


http.createServer(server).listen(server.get('port'), server.get('host'), () => {
    console.log('Express server running at ' + server.get('hostname') + ':' + server.get('port'));
});