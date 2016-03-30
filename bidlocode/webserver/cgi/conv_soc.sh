#!/bin/bash
PID=$$
DATE=`date +%Y%m%d`
SOC=/var/www/webserver/uploads/soc$DATE/$1
DBP=/var/www/webserver/uploads/soc$DATE/$2
	echo "$DBP:$SOC" > /var/www/webserver/uploads/dbp
WORKDIR=/var/www/webserver/uploads/soc$DATE
PASSWORD=$3
USER=root

soc(){
	dbview -b $SOC | recode cp866..utf8 > $WORKDIR/Req_PFR.txt
	cat $WORKDIR/Req_PFR.txt | awk -F: '{print $1": "$2": "$3":"$4 ":"$5}' | sed 's/\ //g'| awk -F: '{print $1", "$2", "$3", "$4 ", "$5}' > $WORKDIR/out.csv
	cut -c1-11 $WORKDIR/out.csv > $WORKDIR/cut0.csv
	cut -c12-300 $WORKDIR/out.csv > $WORKDIR/cut1.csv
	paste $WORKDIR/cut0.csv $WORKDIR/cut1.csv | sed 's/\t/\x20/g' > $WORKDIR/soc0.csv
	grep -v ^, $WORKDIR/soc0.csv > $WORKDIR/soc.csv
}

pfr(){
	libreoffice --headless --infilter="dbf:DBase:CP1251" --convert-to "dbf:DBase:utf8" --outdir "$WORKDIR" $DBP
	dbview -b $WORKDIR/dbp.dbf | awk -F":" '{print $1", " $3", "$6}' | grep 9999/99/99 | awk -F", " '{print $1 ", "$3}' > $WORKDIR/dbf.txt
	cut -c1-14 $WORKDIR/dbf.txt > $WORKDIR/dbf0.txt
	cut -c18-300 $WORKDIR/dbf.txt > $WORKDIR/dbf1.txt
	sed -i "s/^0*//" $WORKDIR/dbf1.txt
	sed -i "s/^.00/0.00/g" $WORKDIR/dbf1.txt
	paste $WORKDIR/dbf0.txt $WORKDIR/dbf1.txt | sed 's/\t/,\x20/g' > $WORKDIR/soc1.csv
}


socdbcreate(){
    mysql -u$USER -p$PASSWORD -e "drop database soc$DATE;"
    mysql -u$USER -p$PASSWORD -e "CREATE DATABASE soc$DATE CHARACTER SET utf8 COLLATE utf8_general_ci;"
    mysql -u$USER -p$PASSWORD -e "use soc$DATE;" -e " create table soc ( snils TEXT, name TEXT, fam TEXT, otch TEXT, nomer TEXT);"
    mysql -u$USER -p$PASSWORD -e "use soc$DATE;" -e " create table pfr ( snils TEXT, summ TEXT);"
}


csvload(){
IFS=,
while read column1 column2 column3 column4 column5
      do
        echo "INSERT INTO soc (snils,name,fam,otch,nomer) VALUES ('$column1', '$column2', '$column3', '$column4', '$column5');"
done < $WORKDIR/soc0.csv | mysql -u$USER -p$PASSWORD soc$DATE;

IFS=,
while read column1 column2
      do
        echo "INSERT INTO pfr (snils, summ) VALUES ('$column1', '$column2');"
done < $WORKDIR/soc1.csv | mysql -u$USER -p$PASSWORD soc$DATE;
}

getinner() {
mysql -u$USER -p$PASSWORD soc$DATE <<EOF
SELECT soc.snils, soc.name, soc.fam, soc.otch, soc.nomer, pfr.summ FROM soc INNER JOIN pfr ON soc.snils = pfr.snils
INTO OUTFILE '$WORKDIR/output.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
EOF
}
	echo "$PID" > /var/www/webserver/uploads/pid
soc
	echo "1"
pfr
	echo "2"
socdbcreate
	echo "3"
csvload
	echo "4"
getinner
	echo "Завершено!" > /var/www/webserver/uploads/pid
