#!/usr/bin/env python 
import paramiko,os,sys 

class upload_files:

   def __init__(self,hostname,username,password):
      self.hostname = hostname 
      self.username = username 
      self.password = password 
      self.port = 22

      try: 
         self.ssh = paramiko.Transport((hostname,self.port)) 
         self.ssh.connect(username=username,password=password) 
      except (paramiko.BadHostKeyException, paramiko.AuthenticationException,paramiko.SSHException) as e:
         print str(e)
         sys.exit(-1)

   # this function dowload the files
   def getFiles(self,thefile): 
      
      sftp = paramiko.SFTPClient.from_transport(self.ssh) 

      print "[+] Uploading --> " + thefile 
      newFile = os.path.basename(thefile) 

      sftp.put(thefile,newFile)
      self.ssh.close() 
   
