#!/bin/bash
if ! [ $(id -u) = 0 ]; then
   echo "Erro! Execute o instalador como root" 
   exit 1
fi

#Atualiza o repositorio
apt-get -y update && sudo apt-get -y upgrade

#Instala o apache
apt-get -y install apache2

#Instala o lftp
apt-get -y install lftp

#Instala o scrot
apt-get -y install scrot

#Baixa o GnPyPlayer
mkdir /var/www/html/GnPyPlayer
mkdir /var/www/html/gncontent
mkdir /var/www/html/jsplayer
chmod -R 777 /var/www/html/

lftp -f "
open gnsignage.com.br
user gnpyplayer gnpyplayer1515
lcd /var/www/html/GnPyPlayer
mirror --continue --delete --verbose / /var/www/html/GnPyPlayer
bye
"

#Copia o diretório do chrome-ext
cp -R /var/www/html/GnPyPlayer/chrome-ext/ /var/www/html/chrome-ext

#Instala as dependência do python
apt-get -y install python3-pip
pip3 install psutil
pip3 install python-engineio
pip3 install eventlet
pip3 install flask
pip3 install pyautogui
pip3 install Xlib

#Instala o browser
apt-get -y install chromium-browser
