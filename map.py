#coding:utf-8
#
import sys, time, datetime
import json
from DaemonClass import Daemon
class TestMonitor(Daemon):
    intvl = 10
    def __init__(self,
               pidfile='/tmp/test-monitor.pid',
               stdin='/dev/stdin',
               stdout='/dev/stdout',
               stderr='/dev/stderr',
               intvl=10):
        Daemon.__init__(self, pidfile=pidfile, stdin=stdin, stdout=stdout, stderr=stderr)
        # Set poll interval
        TestMonitor.intvl = intvl

    '''
    Basic poll task
    '''
    def _poll(self):
	# 全球
	gname={'274':'南非茨瓦','277':'埃及开罗','51':'美国达拉斯','52':'美国旧金山','122':'美国纽约','101':'英国伦敦','111':'德国法兰克福','129':'巴西圣保罗','130':'阿根廷','133':'加拿大蒙特利尔','142':'澳大利亚悉尼','212':'荷兰阿姆斯特丹','213':'美国华盛顿','214':'法国巴黎','217':'墨西哥','220':'美国洛杉矶','239':'意大利米兰','258':'卢森堡','259':'立陶宛','260':'罗马尼亚','261':'美国芝加哥','262':'美国亚特兰大','263':'美国菲尼克斯','264':'美国盐湖城','265':'美国新泽西','266':'英国曼彻斯特','267':'美国奥兰多','110':'韩国首尔','117':'日本东京','121':'新加坡','149':'印度尼西亚','190':'韩国仁川','191':'日本长野','221':'泰国曼谷','222':'越南河内','223':'印度孟买','272':'菲律宾马尼拉','31':'台湾台北','104':'香港','184':'台湾台中'}
	# 电信
	dname={'1':'西安','11':'上海','12':'深圳','13':'四川','15':'浙江','107':'长沙','108':'武汉','113':'江苏','114':'重庆','116':'福建','124':'安微','126':'广州','127':'江西','128':'云南','131':'贵州','137':'乌鲁木齐','138':'南宁','139':'兰州','141':'四川眉山','143':'南京','145':'衡阳','146':'厦门','147':'北京','148':'内蒙','152':'湛江','153':'佛山','154':'茂名','155':'上饶','156':'梧州','157':'九江','158':'天津','163':'合肥','168':'泉州','171':'十堰','172':'鄂州','174':'宜昌','176':'嘉兴','177':'丽水','178':'杭州','179':'金华','180':'徐州','181':'扬州','182':'宁波','183':'镇江','187':'绵阳','188':'乐山','207':'常州','208':'海口','209':'衢州','215':'昆山','219':'拉萨','226':'株洲','231':'大庆','236':'太原','237':'石家庄','243':'许昌','244':'济南','245':'辽阳','247':'宁夏','248':'西宁','257':'延吉'}	
	# 联通
	lname={'2':'大连','14':'北京','16':'济南','102':'辽宁','106':'上海','112':'河南','115':'黑龙江','123':'天津','132':'石家庄','134':'太原','136':'长春','140':'吉林四平','144':'内蒙','159':'唐山','160':'厦门','162':'宿迁','164':'青岛','165':'牡丹江','166':'伊春','167':'黑河','173':'阜新','192':'枣庄','193':'菏泽','194':'莱芜','195':'潍坊','196':'三门峡','197':'新乡','198':'商丘','199':'郑州','200':'信阳','201':'南昌','202':'开封','203':'临汾','204':'秦皇岛','205':'宝鸡','206':'晋城','216':'宁夏','218':'西宁','224':'张家口','225':'西安','232':'长沙','233':'眉山','234':'鄂州','235':'重庆','241':'东莞','242':'合肥','246':'云南','249':'拉萨','250':'乌鲁木齐','251':'贵州','252':'南宁','253':'海口','254':'兰州','255':'绍兴'}
	# 移动
	yname={'118':'浙江','120':'上海','125':'天津','150':'济南','151':'北京','161':'苏州','169':'武汉','175':'沈阳','185':'杭州','186':'泉州','189':'厦门','211':'常州','227':'郑州','228':'深圳','229':'广东','230':'成都','238':'贵阳','256':'西安','268':'合肥','278':'重庆','279':'南昌','280':'长沙','281':'石家庄','282':'兰州'}
	type = {"gname":gname,"dname":dname,"lname":lname,"yname":yname}
	for k,v in type.items():
		self._filterdata(k,v)
	
    def _filterdata(self,tag,name):
	files = {"dig":"/tmp/monitor/dig.txt","domain":"/tmp/monitor/domain.txt","gateway":"/tmp/monitor/gateway.txt"}
	for k,v in files.items():
            r = open(v)
            res = r.read()
            r.close()
            res  = eval(res)
            tip = []
            data = []
            top = []
            for i in res:
                key = i.keys()[0]
                if name.has_key(key):
               	    param = name[key]+':"'+i.values()[0]+'"'
                    tip.append(param)
		    if "503" in i.values()[0]:
                        data.append("{name:'"+name[key]+"',"+"value:20}")
                        top.append("{\"name\":\""+name[key]+"\","+"\"value\":20}")
		    elif "/: 404" in i.values()[0]:
                        data.append("{name:'"+name[key]+"',"+"value:30}")
                        top.append("{\"name\":\""+name[key]+"\","+"\"value\":30}")
		    elif "file" in i.values()[0]:
                        data.append("{name:'"+name[key]+"',"+"value:30}")
                        top.append("{\"name\":\""+name[key]+"\","+"\"value\":30}")
		    elif "stop" in i.values()[0]:
                        data.append("{name:'"+name[key]+"',"+"value:40}")
                        top.append("{\"name\":\""+name[key]+"\","+"\"value\":40}")
		    elif "timeout" in i.values()[0]:
                        data.append("{name:'"+name[key]+"',"+"value:50}")
                        top.append("{\"name\":\""+name[key]+"\","+"\"value\":50}")	
		    elif "error" in i.values()[0]:
                        data.append("{name:'"+name[key]+"',"+"value:20}")
                        top.append("{\"name\":\""+name[key]+"\","+"\"value\":20}")
		    else:
                        data.append("{name:'"+name[key]+"',"+"value:10}")
					
            info = open("/tmp/monitor2/"+tag+k+"_info.txt",'w+')
            info.write(str(tip))
            info.close()

            info2 = open("/tmp/monitor2/"+tag+k+"_name.txt",'w+')
            data = {"name":data,"top":top}
            info2.write(str(data))
            info2.close()	

    def run(self):
	c = 0
        while True:
	    data = self._poll()
            time.sleep(TestMonitor.intvl)
            c = c + 1
            
if __name__ == "__main__":
    daemon = TestMonitor(pidfile='/tmp/map.pid', 
                           intvl=10)
   
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print 'Unknown command'
            sys.exit(2)
    else:
        print 'USAGE: %s start/stop/restart' % sys.argv[0]
        sys.exit(2)

