#!/bin/bash
if ! [ $(id -u) = 0 ]; then
   echo "Erro! Execute o instalador como root" 
   exit 1
fi

#Atualiza o repositorio
apt-get -y update && sudo apt-get -y upgrade

#Instala os aplicativos
apt-get -y install apache2
apt-get -y install lftp
apt-get -y install scrot
apt-get -y install gnome-terminal

#Baixa o GnPyPlayer
mkdir /var/www/html/GnPyPlayer
mkdir /var/www/html/gncontent
mkdir /var/www/html/jsplayer
chmod -R 777 /var/www/html/

lftp -f "
set ftp:ssl-allow false
set ftp:use-feat false
set net:timeout 60
open ds.gnplay.com.br
user gnpyplayer gnpyplayer1515
lcd /var/www/html/GnPyPlayer
mirror --continue --delete --verbose / /var/www/html/GnPyPlayer
bye
"

#Cria os arquivos de inicialização
mkdir /home/$SUDO_USER/.config/autostart
cp /var/www/html/GnPyPlayer/extras/gnplayer-start.desktop /home/$SUDO_USER/.config/autostart/

#Instala as dependência do python
apt-get -y install python3-pip
pip3 install psutil
pip3 install python-engineio
pip3 install eventlet
pip3 install flask
pip3 install pyautogui
pip3 install Xlib
pip3 install netifaces
pip3 install websocket-server

#Instala o browser
apt-get -y install chromium-browser

#Cria os atalhos
xdg-user-dirs-update --set DESKTOP $HOME/Desktop
ln -s /home/$SUDO_USER/.config/autostart/gnplayer-start.desktop /home/$SUDO_USER/Desktop/

#Reinicia a máquina
reboot
