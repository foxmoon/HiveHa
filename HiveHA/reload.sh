if [ -f  ./node.pid ];
then
kill -9 `cat node.pid`
fi
if [ -f  ./server.pid ];
then
kill -9 `cat server.pid`
fi
twistd  -l node.log --pidfile node.pid -y  node.py
twistd -l server.log --pidfile server.pid -y haserver.py