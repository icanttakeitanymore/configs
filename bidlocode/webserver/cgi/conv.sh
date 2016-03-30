#!/bin/bash
DATE=`date +%Y%m%d`
touch /var/www/webserver/uploads/pid
echo $$ > /var/www/webserver/uploads/pid
OUTPUT=out.csv
    printf "Название файла Список Персо: "
f1=/var/www/webserver/uploads/pers$DATE/$1
    printf "Название файла Соглашения: "
f2=/var/www/webserver/uploads/pers$DATE/$2
USER=root
    printf "Пароль MYSQL"
PASSWORD=$3

convert(){
    xls2csv -s windows-1251 -d utf-8 $f1 > ${f1/.xls/.csv}
    xls2csv -s windows-1251 -d utf-8 $f2 > ${f2/.xls/.csv}
}


edit() {
    sed -i '1,2d ' ${f1/.xls/.csv}
    sed -i -e :a -e '$d;N;1,1ba' -e 'P;D' ${f1/.xls/.csv}
    sed -i 's/"//g' ${f1/.xls/.csv}
    sed -i 's/"//g' ${f2/.xls/.csv}
}

dbcreate() {
    mysql -u$USER -p$PASSWORD -e "drop database db$DATE;"
    mysql -u$USER -p$PASSWORD -e "CREATE DATABASE db$DATE CHARACTER SET utf8 COLLATE utf8_general_ci;"
    mysql -u$USER -p$PASSWORD -e "use db$DATE;" -e " create table full ( nomer TEXT, name TEXT, kolvo varchar(20));"
    mysql -u$USER -p$PASSWORD -e "use db$DATE;" -e " create table output ( nomer TEXT, name TEXT, kolvo varchar(20));"
    mysql -u$USER -p$PASSWORD -e "use db$DATE;" -e " create table short ( nomer TEXT);"
}

csvload() {

IFS=,
while read column1 column2 column3
      do
        echo "INSERT INTO full (nomer,name,kolvo) VALUES ('$column1', '$column2', '$column3');"

done < ${f1/.xls/.csv} | mysql -u$USER -p$PASSWORD db$DATE;

IFS=,
while read column1
      do
        echo "INSERT INTO short (nomer) VALUES ('$column1');"

done < ${f2/.xls/.csv} | mysql -u$USER -p$PASSWORD db$DATE;
}

getinner() {
rm -f /var/www/webserver/uploads/pers$DATE/out.csv
mysql -u$USER -p$PASSWORD db$DATE <<EOF
SELECT full.nomer,full.name,full.kolvo FROM full WHERE NOT EXISTS(SELECT * FROM short WHERE full.nomer = short.nomer)
INTO OUTFILE '/var/www/webserver/uploads/pers$DATE/out.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
EOF

IFS=,
while read column1 column2 column3
      do
        echo "INSERT INTO output (nomer,name,kolvo) VALUES ('$column1', '$column2', '$column3');"

done < /var/www/webserver/uploads/pers$DATE/out.csv | mysql -u$USER -p$PASSWORD db$DATE;
}

queryes(){
rm -F /var/www/webserver/uploads/pers$DATE/*.csv
mysql -u$USER -p$PASSWORD db$DATE <<EOF
SELECT * FROM output WHERE kolvo between 1 and 5 INTO OUTFILE '/var/www/webserver/uploads/pers$DATE/out1-5.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
EOF

mysql -u$USER -p$PASSWORD db$DATE <<EOF
SELECT * FROM output WHERE kolvo between 6 and 15 INTO OUTFILE '/var/www/webserver/uploads/pers$DATE/out6-15.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
EOF

mysql -u$USER -p$PASSWORD db$DATE <<EOF
SELECT * FROM output WHERE kolvo between 16 and 24 INTO OUTFILE '/var/www/webserver/uploads/pers$DATE/out16-24.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
EOF

mysql -u$USER -p$PASSWORD db$DATE <<EOF
SELECT * FROM output WHERE kolvo between 25 and 999999 INTO OUTFILE '/var/www/webserver/uploads/pers$DATE/out25-more.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
EOF

mysql -u$USER -p$PASSWORD db$DATE <<EOF
SELECT * FROM output WHERE kolvo = 0 INTO OUTFILE '/var/www/webserver/uploads/pers$DATE/out-nol.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
EOF
}

    printf "конвертация\n"
    printf "16 процентов\n"
convert
    printf "подготовка к загрузке\n"
    printf "32 процентов\n"
edit
    printf "создание бд\n"
    printf "48 процентов\n"
dbcreate
    printf "загрузка csv\n"
    printf "64 процентов\n"
csvload
    printf "соединение таблиц\n"
    printf "80 процентов\n"
getinner
    printf "выполнение запросов\n"
    printf "завершение\n"
queryes
    printf "done!\n"
echo "Завершено" > /var/www/webserver/uploads/pid
cp -R /var/www/webserver/uploads/pers$DATE/ /srv/smb/serv_doc/DOC/0/Выгрузки
chmod 777 /srv/smb/serv_pers/БОРИС/gen/pers$DATE/*
