git checkout .
git pull origin master
cp ../web.conf web.conf
nohup python3 web.py &