if [ -f  ./node.pid ];
then
kill -9 `cat node.pid`
fi
twistd  -l node.log --pidfile node.pid -y  node.py
