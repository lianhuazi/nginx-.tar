nginx-.tar
==========

基于nginx 流量统计，python +django 每天抓取数据存入数据库，根据项目部的使用域名，统计出项目部门承担费用


###不会美化。希望能有人美化一个ＵＩ　热爱开源。
###ＱＱ　１２３７６９７５２
###问题交流技术群 35666534
####重庆话语　罗宏江
配置服务是用python+django 编写的
服务端：nginx+uwsgi+mysql
python2.6
Django-1.6.4


!!nginx 须要装req-status
nginx 插件配置：
  req_status_zone server_name $server_name 256k;
  req_status_zone server_addr $server_addr 256k;
  req_status server_name server_addr;


[１]配置更改
１.views.py 文件
更改你想要的ＩＰ地址
	menu={
'6.6.6.6':'6.6.6.6/req-status',
		}

基于mysql 建库名为：request_stat

２.bg.py 文件
更改你想要的部门名：
	bm={
		'shuiguo':u'水果',
		'063game':u'063游戏',
		'kuping':u'酷屏',
		'dianxin':u'点心',
		}


[２]后台　地址路由　非页面显出：
１　http://192.168.7.44/bgdel/　删部门中的域名关联
２　http://192.168.7.44/bg/　添加域名到部门进行关联
3　http://192.168.7.44/sqllook/　写出你牛Ｂ　ＳＱＬ语句进行查询

[３]后台入库地址　非页面显出：、

这是一个shell 内容
一天执行一次。自己加入定时
curl -s "http://192.168.7.44/look/６.６.６.６/６.６.６.６/req-status/insert"
sleep 30
now=$(date +%Y-%m-%d)
curl -s "http://192.168.7.44/tj/６.６.６.６/$now/"


#########热爱技术的同时。请热爱你自己身体。关注养生保建 [四季养生　www.sijiyang.com　]　我的网站。希望能帮助到你
