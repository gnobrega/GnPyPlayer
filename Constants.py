VERSION = 1.07

global SERVER
global SERVER2
global SERVER_URL
global SERVER_API_AUTH
global SERVER_API_DATA
global SERVER_API_PING
global SERVER_API_UPLOAD_SCREENSHOT
global FTP_JS_HOST
global FTP_CONTENT_HOST

APP_NAME = "Gn Signage"
SERVER = "http://srv1.gnsignage.com.br/";
SERVER2 = "http://plux.gnsignage.com.br/";
SERVER_URL = SERVER + "downloads/gnpyplayer/version.txt"
SERVER_API_AUTH = SERVER + "api/get-authorization?linux=true&mac=";
SERVER_API_DATA = SERVER + "api/get-player-content/?id_player="
SERVER_API_PING = SERVER + "api/ping/?id_player="
SERVER_API_UPLOAD_SCREENSHOT = SERVER + "api/send-screenshot/id_player/"
PATH_CONTENT = "/var/www/html/gncontent/"
PATH_JSPLAYER = "/var/www/html/jsplayer/"
PATH_VERSION = PATH_CONTENT + "/version.txt"
PATH_CLIENT_CONTENT = "/var/www/html/content/"
FTP_JS_HOST = 'srv1.gnsignage.com.br';
FTP_JS_USER = 'jsplayer';
FTP_JS_PASS = 'jsplayer1515';
FTP_LOGS_HOST = FTP_JS_HOST;
FTP_LOGS_USER = 'gnlogs';
FTP_LOGS_PASS = 'gnlogs1515';
FTP_CONTENT_HOST = FTP_JS_HOST;
FTP_CONTENT_USER = 'gnsignage';
FTP_CONTENT_PASS = 'gnsignage1515';
COMMAND_START_PLAYER = "chromium-browser --enable-logging --v=1 --kiosk --app=http://localhost/jsplayer/index-linux.html"
#COMMAND_START_PLAYER = "chromium-browser --enable-logging --v=1 http://localhost/jsplayer/index-linux.html"
TIME_PLAYER_ON = ""
TIME_PLAYER_OFF = ""
TIME_PLAYER_OFF = ""

