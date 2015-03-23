import web
import json
import time
import urllib, urllib2
import ping
import paravalues
import sys
from datetime import datetime
from threading import Timer

test_on=0
suppress=0
stat_and_cap=paravalues.stat_and_cap
urls= (
 "/ma/config", "config",
 "/ma/ins", "ins",
 "/ma/cap", "cap",
 "/ma/rep", "rep"
 )
do_task_data =[]

#def Do_task(self,data):
#   print 'come into  Do_task'
#   self.process_Ping(data);
#ִ��ping�ĺ�����ʵ��
def process_Ping(data):
  print "begin process_Ping"
  #print data;
  #print data[u'ma-instruction'][u'ma-instruction-tasks'][0]
  if data[u'ma-instruction'][u'ma-instruction-tasks'][0][u'ma-task-name'].lower()==u'ping' :
   i=0; parastring=''; 
   for  i in range(len(data[u'ma-instruction'][u'ma-instruction-tasks'][0][u'ma-task-options'])) :
     #print data[u'ma-instruction'][u'ma-instruction-tasks'][0][u'ma-task-options'][i];print parastring
     if data[u'ma-instruction'][u'ma-instruction-tasks'][0][u'ma-task-options'][i][u'name']!='destination-ip' :
       if i==0 :
         parastring=str(data[u'ma-instruction'][u'ma-instruction-tasks'][0][u'ma-task-options'][i][u'value'])
       else :
        parastring=parastring+','+str(data[u'ma-instruction'][u'ma-instruction-tasks'][0][u'ma-task-options'][i][u'value'])
     else :
        parastring=parastring+','+str(data[u'ma-instruction'][u'ma-instruction-tasks'][0][u'ma-task-options'][i][u'value'][u'ip-address'])
   parastring=parastring.split(',');
   #print parastring
   print 'suppress',suppress;
   while suppress==0 :
    testresult=list(ping.verbose_ping(parastring[2]));
    report=paravalues.rep
    report[u'ma-report'][u'ma-report-date']=str(datetime.now())
    report[u'ma-report'][u'ma-report-tasks'][0][u'ma-report-task-config']=data[u'ma-instruction'][u'ma-instruction-tasks'][0]
    rep_url=data[u'ma-instruction'][u'ma-report-channels'][0][u'ma-channel-target'];
    report[u'ma-report'][u'ma-report-tasks'][0][u'ma-report-task-rows']=testresult;    report=json.dumps(report);
    #rep_url="http://172.24.20.185:8080/ma/rep"
    req=urllib2.Request(rep_url, report);
    print "reportted here"
    print rep_url
    response=urllib2.urlopen(req)
    thepage=response.read();
    time.sleep(24*60*60)
    print "end process_Ping"
#time����ʱ����ִ�еĺ����壬���ǿ���δ�����кܶ��������ȫ�ֵ���������У�����Ŀǰֻ��һ���������do_task_data[0]�����ݣ�����Ŀǰ���������ִ��ping ָ�������Ҫ�����ж��������ͷ���ִ�С�
def Do_task():
   #self.process_Ping(data);
   process_Ping(do_task_data[0]);

   
#schedule�����һЩ��ʽ�ľ��������ʵ��,Ŀǰֻʵ����calendar��������ֻ����������    
#calendar
#��calendar ��Сʱ�����ӣ����������϶��г�������parastring�С�
def process_Timing_calendar(data):
  try:
      i=0; j=0; k=0; parastring=''; temp_hour='';temp_min='';temp_sec='';
      for i in range(len(data[u'ma-instruction'][u'ma-instruction-schedules'][0][u'ma-schedule-timing'][u'ma-timing-calendar'][u'ma-calendar-hours'])) :
         temp_hour=data[u'ma-instruction'][u'ma-instruction-schedules'][0][u'ma-schedule-timing'][u'ma-timing-calendar'][u'ma-calendar-hours'][i]
         temp_hour=str(datetime.now().hour)
         for j in range(len(data[u'ma-instruction'][u'ma-instruction-schedules'][0][u'ma-schedule-timing'][u'ma-timing-calendar'][u'ma-calendar-minutes'])) :
            temp_min=data[u'ma-instruction'][u'ma-instruction-schedules'][0][u'ma-schedule-timing'][u'ma-timing-calendar'][u'ma-calendar-minutes'][j]   
            temp_min=str(datetime.now().minute+1)
            #print   'temp_min' ,  temp_min;                  
            for k in range(len(data[u'ma-instruction'][u'ma-instruction-schedules'][0][u'ma-schedule-timing'][u'ma-timing-calendar'][u'ma-calendar-seconds'])) :
               temp_sec=data[u'ma-instruction'][u'ma-instruction-schedules'][0][u'ma-schedule-timing'][u'ma-timing-calendar'][u'ma-calendar-seconds'][k]
               if i==0:
                  if j==0:
                     if k==0:
                        parastring=parastring
                     else:
                        parastring=parastring + ';'
                  else:
                     parastring=parastring + ';'
               else:
                  parastring=parastring + ';'
               parastring = parastring +temp_hour +':'+ temp_min +':'+ temp_sec
   
      #else :
         #print 'calendar_wrong';
      return parastring
   
      print parastring;
      
  except Exception , e :
      print e; 

#periodic     
def process_Timing_periodic(data):
    try:
       pass
       #print 'periodic'
    except Exception , e :
       #print e;
       pass

#one_off     
def process_Timing_one_off(data):
  try:
     pass
     #print 'one-off'
  except Exception , e :
     #print e;
     pass
    
#immediate_obj     
def process_Timing_immediate_obj(data):
    try:
       pass
       #print 'immediate_obj'
    except Exception , e :
       #print e;
       pass
         
#startup_obj     
def process_Timing_startup_obj(data):
    try:
       pass
       #print 'startup_obj'
    except Exception , e :
       #print e;
       pass
         
#schedule
#��data�н���scheduleת����Ϊһ��һ���ľ���ʱ�䲢�ҷ����б��У��ĵ�������������schedule :calendar;one-off;immediate-obj�����֣��������Ԥ���˷�֧�Ĵ�������Ŀǰֻ��ʵ����calendar
def process_schedules(data):
    timelist = '';
    try:
       Timing_type = data[u'ma-instruction'][u'ma-instruction-schedules'][0][u'ma-schedule-timing'][u'ma-timing-calendar'];
       if Timing_type != u'ma-timing-calendar':
          timelist = process_Timing_calendar(data); 
    except Exception , e :
         
           test_on=0
          
    try:             
       Timing_type = data[u'ma-instruction'][u'ma-instruction-schedules'][0][u'ma-schedule-timing'][u'ma-one-off'];
       print Timing_type;
       if Timing_type != u'ma-one-off':
          timelist = process_Timing_one_off(data);
          #print timelist;
    except Exception , e :
         
         test_on=0
          
    try:             
       Timing_type = data[u'ma-instruction'][u'ma-instruction-schedules'][0][u'ma-schedule-timing'][u'ma-immediate-obj'];
       if Timing_type != u'ma-immediate-obj':
          timelist = process_Timing_immediate_obj(data);
          #print timelist;
          
    except Exception , e :

         test_on=0
          
    try:             
       Timing_type = data[u'ma-instruction'][u'ma-instruction-schedules'][0][u'ma-schedule-timing'][u'ma-startup-obj'];
       if Timing_type != u'ma-startup-obj':
          timelist = process_Timing_startup_obj(data);
          #print timelist;
    except Exception , e :

         test_on=0

    timelist=timelist.split(';')
    
    return timelist;
  
#ִ��һ��ָ�� 
def process_task(data):
  global test_on, suppress
  #��ָ��ִ�����ݷ���ȫ��do_task_data�����У�����timer���Լ����߳���ִ�����Խ����ݷ���ȫ�ֲ�������
  if len(do_task_data)==0:
     do_task_data.append(data)
  do_task_data[0] = data;
  if test_on :
    return
  else :
    if suppress==1:
      suppress=0
  test_on=1
  #�Դ����ָ�����������Ҫִ�е�schedule �е�ÿһ��ʱ�䲢�ҷ���timelist��
  timelist = process_schedules(data);
  #print timelist;        
   
  for i in range(len(timelist)) :
     #����timelist�����е�ʱ���ȡ���� �������Ҫ�ȴ���ʱ��delta
     tempTime=timelist[i];

     tempTime = tempTime.split(':')
     
     dt = datetime.now()  



     datetime_now = datetime.now();
     datetime_schedule = datetime.now();
     datetime_schedule = datetime_schedule.replace( datetime_schedule.year , datetime_schedule.month , datetime_schedule.day , int(tempTime[0]) , int(tempTime[1]) , int(tempTime[2]), 0)
     
     delta = datetime_schedule - datetime_now          
     #��������������еȴ�ʱ�䰴�մ�С�����˳����� tm_array������
     if i==0:
        tm_array = [delta]

     else:
        bFound = 0;
        array_size = len(tm_array);
        for j  in range(array_size) :
           if delta < tm_array[j]:
              tm_array.append(tm_array[array_size-1]);
              for k in range(array_size-j) :
                  tm_array[array_size-k] = tm_array[array_size-k-1];
              tm_array[j] = delta
              bFound = 1;
              break;
           elif delta == tm_array[j]:
              bFound = 1;
              break;
     
        if bFound == 0: 
           tm_array.append(delta);
                
  for j  in range(len(tm_array)) :
      #����tm_array���е�Ҫ�ȴ���ʱ�䣬
     print '';
     print 'schedule time:',tm_array[j] + datetime_now
     #print tm_array[j]
     #print tm_array[j].total_seconds()
     #���ʱ��>���ǽ�����ʱ�䣬������ǹ�ȥ��ʱ��Ӧ�ü���24Сʱ������86400��
     if tm_array[j].total_seconds() > 0:
        wait_sec = tm_array[j].total_seconds()
     else:
         wait_sec = 86400 + tm_array[j].total_seconds();
     print 'wait_sec:',wait_sec
     #t=Timer(wait_sec,Do_task(self,data))
     #��wait_sec��ʼִ��Do_task
     t=Timer(wait_sec,Do_task)
     t.setDaemon(bool)
     t.start()
     #timer_thread_array.append(t)


  
  
  test_on=0

def suppression():
  global test_on,suppress
  suppress=1;  

class rep:
   def POST(self) :
     data=web.data()
     web.header('Content-Type', 'application/json')
     print '---------------------new report coming-----------------------'
     print data
     print '---------------------new report end-----------------------'
class cap:
    def GET(self):
        web.header('Content-Type', 'application/json')
        return stat_and_cap
class ins:
     global test_on
     global suppress 
     def POST(self):
          data=web.data()
          web.header('Content-Type', 'application/json')
          print data
          data=json.loads(data); #print data[u'ma-instruction'].keys()
          try:
                 keys= data[u'ma-instruction'].keys();
                 
          	 if u'ma-suppression' in keys:
                    if  data[u'ma-instruction'][u'ma-suppression'][u'ma-suppression-enabled']:
                     print 'Suppression';suppression()                 
          	 elif u'ma-exit' in keys:       #ִ���˳�ָ��
                    if  data[u'ma-instruction'][u'ma-exit'][u'ma-exit-enabled']:
                     print 'exit';
                     #for i in range(len(timer_thread_array)):
                     #   print 'exit_timer';
                     #   timer_thread_array[i].start();
                     sys.exit(0);

          	 elif u'ma-instruction-tasks' in keys :    #ִ��һ��ָ��
                    process_task(data)
                    print 'process_task_finish'
                   
          except Exception, e :
         	  print e;test_on=0                     
        
class config:
    def PUT(self):
       web.header('Content-Type', 'application/json')
       data=web.data()
       print data

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

