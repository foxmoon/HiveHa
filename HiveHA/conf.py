#-*-coding:UTF-8 -*-
##### for HA SERVER
hostTmp={}#hive host template ,format host_port = port
hostTmp["192.168.1.55_10001"]="10001"
hostTmp["192.168.1.55_10002"]="10002"
hostTmp["192.168.1.55_10003"]="10003"
hostTmp["192.168.1.55_10004"]="10004"
hostTmp["192.168.1.55_10005"]="10005"
#restart hive to notify
notify_url="http://127.0.0.1/send.php"
#restart hive msg to notify mail
notify_mail="notify@sb.com"
#must string,the kill hive node listen port
manage_port=2003
#must int, ha proxy server listen port
ha_port=8088
#time to check hive alive in blacklist
black_check_time=10
#whether to  log the sql send to proxy
send_sql_debug=1
#whether to  log the sql error happened in query
rec_error_debug=1
#whether to  log proxy server state
server_stat_debug=1
#logic sql to valid hive alive,like "show databases",or other logic SQL
hive_valid_sql="show databases"
########## for admin Node
start_hive_cmd="export HADOOP_HOME=/usr; export JAVA_HOME=/usr/java/default;/usr/bin/hive --service hiveserver"
