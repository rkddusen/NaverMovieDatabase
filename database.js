const mysql = require('mysql');

module.exports = function () {
    return {
        init: function () {
            return mysql.createConnection({
                host: '127.0.0.1',
                port: '3306',
                user: 'root',
                password: '',
                database: 'movie',
                dateStrings: 'date',
                multipleStatements : true//다중쿼리문 보낼수있음
            })
        },
        
        db_open: function (con) {
            con.connect(function (err) {
                if (err) {
                    console.error('mysql connection error :' + err);
                } else {
                    console.info('mysql is connected successfully.');
                }
            })
        }
    }
};