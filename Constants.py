class Constants:
    #SERVER = "http://homol.gnsignage.com.br:81/";
    APP_NAME = "Gn Signage"
    SERVER = "http://gnsignage.com.br/";
    SERVER_API_AUTH = SERVER + "api/get-authorization?mac=";
    SERVER_API_DATA = SERVER + "api/get-player-content/?id_player="
    SERVER_API_PING = SERVER + "api/ping/?id_player="
    SERVER_API_UPLOAD_SCREENSHOT = SERVER + "api/send-screenshot/id_player/"
    PATH_CONTENT = "/var/www/html/gncontent/"
    PATH_JSPLAYER = "/var/www/html/jsplayer/"
    PATH_CLIENT_CONTENT = "/var/www/html/content/"
    FTP_JS_HOST = 'gnsignage.com.br';
    FTP_JS_USER = 'jsplayer';
    FTP_JS_PASS = 'jsplayer1515';
    FTP_CONTENT_HOST = FTP_JS_HOST;
    #FTP_CONTENT_USER = 'gnsignagehomol';
    #FTP_CONTENT_PASS = 'gnsignagehomol1515';
    FTP_CONTENT_USER = 'gnsignage';
    FTP_CONTENT_PASS = 'gnsignage1515';
    COMMAND_START_PLAYER = "chromium-browser --kiosk --no-sandbox --load-and-launch-app=/var/www/html/chrome-ext"
    TIME_PLAYER_ON = ""
    TIME_PLAYER_OFF = ""
