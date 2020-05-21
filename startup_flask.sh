/bin/sleep 15
cd /home/pi/Documents/Pi-Music-Server
git pull
sudo su pi -c "python3 -m music_backend.music_api"
/bin/sleep 20
