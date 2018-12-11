#!/bin/bash

#get username and password
USER=gnsignagehomol             	#Your username
PASS=gnsignagehomol1515         	#Your password
HOST="gnsignage.com.br" 		#Keep just the address
LCD="/home/gnobrega/sync"     	#Your local directory
RCD="/"               			#FTP server directory

lftp -f "
open $HOST
user $USER $PASS
lcd $LCD
mirror --continue --delete --verbose $1 $2
bye
" 
