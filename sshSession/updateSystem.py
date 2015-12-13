#!/usr/bin/env python 
import paramiko,sys,os,socket,threading 

class remote_session:

   def __init__(self,hostname,uname,passwd):
      self.uname = uname 
      self.passwd = passwd 
      self.hostname = hostname
      self.command = '' # command to be executed on the remote server 
      self.os_flavor = ''
      self.cmd = ''

      try: 
         self.ssh = paramiko.SSHClient() 
         self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         self.ssh.connect(hostname,username=uname, password=passwd)
         self.stdin,self.stdout,self.stderr  = self.ssh.exec_command('cat /etc/issue') # read the banner 
         self.os_flavor = self.stdout.read() 

         # check the os flavor 
         if "ubuntu" in self.os_flavor.lower() or "debian" in self.os_flavor.lower(): 
            self.cmd = 'apt-get update ; apt-get dist-upgrade -y'
         #elif "centos" in self.os_flavor.lower() or "redhat" in self.os_flavor.lower(): 
         else:
            self.stdin,self.stdout,self.stderr  = self.ssh.exec_command('cat /etc/redhat-release') # read the banner 
            self.os_flavor = self.stdout.read() 
            if "centos" in self.os_flavor.lower()  or "redhat" in self.os_flavor.lower():
               self.cmd = "yum update"

         self.update_server(self.cmd)
      except (paramiko.BadHostKeyException, paramiko.AuthenticationException,paramiko.SSHException) as e:
         
         print str(e)
         sys.exit(-1)
   
   # this function is responsible for updating the server 
   def update_server(self,cmd):
      try:
         channel = self.ssh.invoke_shell() 
         timeout = 3600
         channel.settimeout(timeout)
         line_buffer = ''
         channel_buffer = '' 
         channel.send( cmd + ' ; exit ' + '\r' ) 
         while True:

            channel_buffer = channel.recv(1).decode('UTF-8')
            if len(channel_buffer) == 0:
               break 
            channel_buffer = channel_buffer.replace('\r', '')
            
            if channel_buffer != '\n' :
               line_buffer += channel_buffer 
            else:
               print line_buffer 
               line_buffer = '' 

      except paramiko.SSHException as e:
         print str(e) 
         sys.exit(-1) 

   
