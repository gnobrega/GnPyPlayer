#!/bin/bash

#get username and password
USER=gnsignagehomol             	#Your username
PASS=gnsignagehomol1515         	#Your password
HOST="gnsignage.com.br" 		#Keep just the address
LCD="/home/gnobrega/sync"     	#Your local directory
RCD="/"               			#FTP server directory

lftp -f "
open $1
user $2 $3
lcd $5
mirror --continue --delete --verbose $6 $4 $5
bye
"
