HiveHa
======

Hive HA server for multi hive backend,with blacklist  pool to detect hive alive and  with admin node server to manage
hive server.
Hive Ha server base on Twisted Python Framework.
So with install Twisted ,Hive HA can settle down on any *unix system.
Hive HA support follow features :
dymatic  start of hive servers,just setup hive params in conf file.
timer to detect alive hives server in black list.
notify hive server start through mail.
automatic kill and restart dead hive server through admin node server.

Installation:
======

wget http://tmrc.mit.edu/mirror/twisted/Twisted/8.1/Twisted-8.1.0.tar.bz2
tar jxvf  Twisted-8.1.0.tar.bz2 
cd Twisted-8.1.0
python setup.py install 
wget  --no-check-certificate  https://pypi.python.org/packages/source/z/zope.interface/zope.interface-3.6.6.tar.gz
tar zxf zope.interface-3.6.6.tar.gz
cd zope.interface-3.6.6
python setup.py install 

edit conf.py

sh reload.sh




