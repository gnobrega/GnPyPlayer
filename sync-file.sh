#!/bin/bash

#get username and password
USER=gnsignagehomol             	#Your username
PASS=gnsignagehomol1515         	#Your password
HOST="gnsignage.com.br" 		#Keep just the address
LCD="/home/gnobrega/sync"     	#Your local directory
RCD="/"               			#FTP server directory

lftp -c "
open $1
user $2 $3
mirror --continue --delete --verbose -i $6 $4 $5
bye
"
