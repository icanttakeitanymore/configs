#!/bin/bash
i=`cat /var/www/webserver/uploads/pid`
kill $i
echo "процесс был остановлен c PID $i" > /var/www/webserver/uploads/pid
