#!/usr/bin/env python 
import paramiko,sys,os,socket,threading,re
from fuzzywuzzy import fuzz

class check_kernel:

   def __init__(self,hostname,uname,passwd):
      self.uname = uname 
      self.passwd = passwd 
      self.hostname = hostname
      self.os_kernel = ''

      # attempt connection to the remote server 
      try: 
         self.ssh = paramiko.SSHClient() 
         self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         self.ssh.connect(hostname,username=uname, password=passwd)

      except (paramiko.BadHostKeyException, paramiko.AuthenticationException,paramiko.SSHException) as e:
         print str(e)
         sys.exit(-1)
   

   def checkExploit(self): 

         self.stdin,self.stdout,self.stderr  = self.ssh.exec_command('uname -a') # read the banner 
         self.os_kernel = self.stdout.read() 
         
         kernel_version = self.os_kernel.split(" ")[2]
         kernel_version =  "linux kernel " + kernel_version.split("-")[0] 
         
         print "[+] Remote Kernel: " + kernel_version

         for line in open('exploit.txt'):
            line = line[:-1].split(",") 
            ratio = fuzz.token_set_ratio(kernel_version, line[2] )
            if (ratio >= 75):
               print "[+] Exploit Found : "  + line[2] + " , " + line[1] 


