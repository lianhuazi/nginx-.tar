#coding:utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import httplib2,re,commands
from django.template import loader,Context
from django.http import HttpResponse
import time,MySQLdb
def index(req):
	return render_to_response('bgindex.html',locals())
def index_add(req):
	cursor = connect()
	bm={
		'shuiguo':u'水果',
		'063game':u'063游戏',
		'kuping':u'酷屏',
		'dianxin':u'点心',
		}

	#cmd="select distinct `key` from traffic_info where vaild=0"
	cmd="SELECT distinct traffic_info.`key` from traffic_info WHERE traffic_info.`key` not in (SELECT domain from project)"
        
	cursor.execute(cmd)
	ym=cursor.fetchall()
	NO=0
	for i in ym:
		for j in i:
			NO=NO+1
	return render_to_response('bgadd.html',locals())	

def add_data(req):
	cursor = connect()
	ym= req.GET.getlist('select2','')
	bm=req.GET.get('select','')
	cmd="insert into project(pro_name,domain) VALUES (%s,%s)"
	cmd1="update traffic_info set vaild=1 where `key`=%s"
	for i in ym:
		cursor.execute(cmd,(bm,i))
		cursor.execute(cmd1,i)
	return HttpResponseRedirect("/bg") 

def index_del(req,argv1):
	cursor = connect()
	bm={
                'shuiguo':u'水果',
                '063game':u'063游戏',
                'kuping':u'酷屏',
		'dianxin':u'点心',
                }
	cmd="select  domain from project where pro_name=%s"
	cmd1="select  count(domain) from project where pro_name=%s"
        
	cursor.execute(cmd,argv1)
        ym=cursor.fetchall()
        
	cursor.execute(cmd1,argv1)
	NO=cursor.fetchall()[0]
        
	return render_to_response('bgdel.html',locals())
	
def del_data(req):
	mytest=req.META['HTTP_REFERER']
	argv1=mytest.split('/')[-1]
	ym=req.GET.getlist('select2','')
	cursor = connect()
	cmd="DELETE FROM project  WHERE pro_name=%s and domain=%s"
	cmd1="update traffic_info set vaild=0 where `key`=%s"
	for i in ym:
		cursor.execute(cmd,(argv1,i))
		cursor.execute(cmd1,i)
        return HttpResponseRedirect("/bgdel")
def connect():
                config = {
                  'user': 'root',
                  'password': '',
                  'host': '127.0.0.1',
                  'database': 'request_stat',
                  'port':3306
                }
                cnx =MySQLdb.connect(host=config['host'],user=config['user'],passwd=config['password'],db=config['database'],port=config['port'])
                cursor = cnx.cursor()
                return cursor
                                
