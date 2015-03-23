import socket
import urllib
import urllib2
import paravalues
import  msvcrt 

timeout=5
socket.setdefaulttimeout(timeout)
def do_exit():
    exit(0)
      
def sent_conf():
      values = paravalues.conf
      req=urllib2.Request('http://127.0.0.1:8080/ma/config',values)
      req.get_method=lambda:"PUT"
      response =urllib2.urlopen(req)
      raw_input("The configuration sent, press enter to continue\n")

def sent_ins():
      url = 'http://127.0.0.1:8080/ma/ins'
      values = paravalues.ins
      try:
        req = urllib2.Request(url, values)
        response = urllib2.urlopen(req)
      except Exception,e:
        pass
      raw_input('The instruction sent, press enter to continue\n'),


def sent_superss():
      url = 'http://127.0.0.1:8080/ma/ins'
      values= paravalues.sup
      try:
        req = urllib2.Request(url, values)
        response = urllib2.urlopen(req)
      except Exception,e :
        pass
      raw_input('The supression_instruction sent, press enter to continue\n')
      
#新增的通知agent退出运行的指令
def sent_exit_ins():
      url = 'http://127.0.0.1:8080/ma/ins'
      values= paravalues.exit_ins
      try:
        req = urllib2.Request(url, values)
        response = urllib2.urlopen(req)
      except Exception,e :
        pass
      raw_input('The exit_instruction sent, press enter to continue\n')

def print_wrong_input():
      raw_input('wrong number \npress enter to continue')

#新增加的指令的说明打印
print """
Usage: number [OPTIONS]
1 Sent config Demo
2 Sent Normal  instruction Demo
3 Sent Supress instruction Demo
4 Sent exit    instruction Demo
5 quit
"""

#循环接收指令并发送指令,根据不同的value构造不同的指令并发送
while True:
  ch = raw_input("please input a number\n");

  values = {'5':do_exit,

            '1':sent_conf,
            
            '2':sent_ins,
            
            '3':sent_superss,

            '4':sent_exit_ins,
          }
  values.get(ch, print_wrong_input)()
 









