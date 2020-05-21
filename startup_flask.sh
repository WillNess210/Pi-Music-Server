cd /home/pi/Documents/Pi-Music-Server
git pull
cd music_controller_webserver
npm i
npm start &
cd ..
sudo su pi -c "python3 -m music_backend.music_api"
/bin/sleep 20