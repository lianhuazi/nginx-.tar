#coding:utf-8
from django.shortcuts import render_to_response
import httplib2,re,commands
from django.template import loader,Context
from django.http import HttpResponse
import time,MySQLdb

def index(req):
	menu={
'6.6.6.6':'6.6.6.6/req-status',

		}
	cursor = connect()
	cmd="select distinct pro_name from project"
	cursor.execute(cmd)
	bm=cursor.fetchall()
	j=36100
	k=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	return render_to_response('index.html',locals())

def look(req,ip,argv1,argv2):
	myhttp=httplib2.Http(timeout=5)
	jg=[]
	req,html=myhttp.request("http://"+argv1,method='GET')	
	now=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	for i in html.split("\n"):
		if not i in "":
			if  re.split(r"\s+",i)[0] in 'zone_name' or re.split(r"\s+",i)[1] in 'localhost' or re.findall(r'\d+\.\d+\.\d+\.\d+',re.split(r"\s+",i)[1]):
				mm=(re.split(r"\s+",i)[0],re.split(r"\s+",i)[1],re.split(r"\s+",i)[2],re.split(r"\s+",i)[3],\
				re.split(r"\s+",i)[4],re.split(r"\s+",i)[5],re.split(r"\s+",i)[6],re.split(r"\s+",i)[7])
			else:
				mm=(re.split(r"\s+",i)[0],re.split(r"\s+",i)[1],re.split(r"\s+",i)[2],re.split(r"\s+",i)[3],\
				re.split(r"\s+",i)[4],re.split(r"\s+",i)[5],re.split(r"\s+",i)[6],re.split(r"\s+",i)[7])
				kk=(re.split(r"\s+",i)[0],re.split(r"\s+",i)[1],re.split(r"\s+",i)[2],re.split(r"\s+",i)[3],\
				re.split(r"\s+",i)[4],re.split(r"\s+",i)[5],re.split(r"\s+",i)[6],re.split(r"\s+",i)[7],now,ip)
				if	argv2 == "insert":
					add_data(kk,ip,re.split(r"\s+",i)[1],now)
			jg.append(mm)
			
	return render_to_response('1.html',locals())

def add_data(param,_IP,_key,_now):
        try:
		cursor = connect()
        	cmd="insert into traffic_info(zone_name,`key`,max_active,max_bw,traffic,requests,active,bandwidth,r_date,IP) \
		values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		cmd1="select * from traffic_info where IP=%s and `key`=%s and r_date=%s"
		cmd2="delete from traffic_info where IP=%s and `key`=%s and r_date=%s"
                n=cursor.execute(cmd1,(_IP,_key,_now))
		if n == 0:
			cursor.execute(cmd,param)
		else:
			cursor.execute(cmd2,(_IP,_key,_now))
			cursor.execute(cmd,param)
		cursor.close()
		cnx.close()
        except:
		return	HttpResponse("insert is error")

def calc_sum(req,_IP,_now):
	try:
		cursor = connect()
		cmd="""insert into traffic_sum(IP,t_sum,r_date) select IP,sum(traffic),r_date from traffic_info where  IP=%s and r_date=%s and traffic like '%%G%%'"""
                cursor.execute(cmd,(_IP,_now))
		return  HttpResponse("insert is ok")
	except:
		return  HttpResponse("insert is error")
def feiyong(req,argv1):
	try:
		now=time.strftime('%Y-%m-%d',time.localtime(time.time()))
                cursor = connect()
		cmd="select * from traffic_info where IP=%s and r_date=%s"
		param=(argv1,now)
		n=cursor.execute(cmd,param)
		querys=cursor.fetchall()
		return render_to_response('feiyong.html',locals())
	except:
		return  HttpResponse("insert is error")
		
def out(req):
	if req.GET['feiyong'] and req.GET['IP']:
		idc=req.GET['feiyong']
		ip=req.GET['IP']
	else:
		return HttpResponse('Please submit a term.')
	cursor = connect()
	now=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	cmd1="select t_sum from traffic_sum where ip=%s and r_date=%s"
	cursor.execute(cmd1,(ip,now))
 	querys=cursor.fetchall()
	ssum=querys[-1][-1]
	
	#cmd="select `key`,traffic,format(traffic/%s*%s,2) from traffic_info where ip=%s and r_date=%s and traffic like '%%G%%'"
	cmd="select a.domain,b.traffic,format(b.traffic/%s*%s,2),a.pro_name from traffic_info as b   join project as a \
	where b.`key`=a.domain and b.ip=%s and b.r_date=%s and b.traffic like '%%G%%' "
	cursor.execute(cmd,(ssum,idc,ip,now))
	isok=cursor.fetchall()
	return render_to_response('out.html',locals())

def bmlook(req,argv1,argv2,argv3):
	cursor = connect()
	#now=time.strftime('%Y-%m-%d',time.localtime(time.time()))
#	now="2014-09-15"
	now=argv2
	isok=[]
	jj=[]
	cmd1="select sum(t_sum) from traffic_sum where r_date=%s "
	cursor.execute(cmd1,now)
	querys=cursor.fetchall()
	NO=0
	for i in querys:
		ssum=i[0]
	#cmd="select b.ip,a.domain,b.traffic,format(b.traffic/%s*%s,2),a.pro_name from traffic_info as b   join project as a \
	#where b.`key`=a.domain and b.r_date=%s and b.traffic like '%%G%%' "
	cmd1="set @fff=%s"
	cursor.execute(cmd1,(ssum))
	if argv3 == "ym":
		cmd="select a.domain ,sum(b.traffic),round(sum(b.traffic)/%s*%s,2) as fy ,@fff,a.pro_name  from traffic_info as b join project as a \
		where b.`key`=a.domain and r_date=%s and traffic like '%%G%%' group by `key` order by `key` "
		
	elif argv3 == "fy":
		cmd="select a.domain ,sum(b.traffic),round(sum(b.traffic)/%s*%s,2) as fy ,@fff,a.pro_name  from traffic_info as b join project as a \
		where b.`key`=a.domain and r_date=%s and traffic like '%%G%%' group by `key` order by fy "
	elif argv3 == "xm":
		cmd="select a.domain ,sum(b.traffic),round(sum(b.traffic)/%s*%s,2) as fy ,@fff,a.pro_name  from traffic_info as b join project as a \
		where b.`key`=a.domain and r_date=%s and traffic like '%%G%%' group by `key` order by a.pro_name "
	del_cmd="TRUNCATE TABLE test"
	cmd_copy="\
		 INSERT INTO test(domain,traffic,feiyong,sum_traffic,project_name) \
		 select a.domain ,sum(b.traffic),round(sum(b.traffic)/%s*%s,2) as fy ,@fff,a.pro_name  from traffic_info as b join project as a \
		 where b.`key`=a.domain and r_date=%s and traffic like '%%G%%' group by `key` order by `key` "
	cursor.execute(del_cmd)
	cursor.execute(cmd_copy,(ssum,argv1,now))
	cursor.execute(cmd,(ssum,argv1,now))
	isok.append(cursor.fetchall())
	return render_to_response('bmlook.html',locals())

def test(req):
	isok=[]
	NO=0
	cursor = connect()
	cmd="select project_name from test group by project_name"
	cursor.execute(cmd)
	querys=cursor.fetchall()
	for i in querys:
		f=i[0]
		cmd1="SET @ff=%s"
		cursor.execute(cmd1,f)
		cmd2="SELECT domain,traffic,feiyong,sum_traffic,project_name, (SELECT sum(feiyong)	FROM test WHERE project_name =@ff ) AS f FROM 	test WHERE project_name =@ff order by project_name,feiyong"
		cursor.execute(cmd2)
		isok.append(cursor.fetchall())
	return render_to_response('xbmlook.html',locals())
def looksql(req):
	cursor = connect()
	if req.GET.has_key('Submit'):
		try:
			cmd=req.GET.get('textfield','')
			cursor.execute(cmd)
			result=cursor.fetchall()
		except:
			return  HttpResponse(u"sql 语句有问题")
	return render_to_response('sql.html',locals())
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
