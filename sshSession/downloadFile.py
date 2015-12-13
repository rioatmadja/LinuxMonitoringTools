#!/usr/bin/env python 
import paramiko,os,sys 

class download_files:

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

   # this function list all possible files on the server
   def listFiles(self,dirPath): 
      sftp = paramiko.SFTPClient.from_transport(self.ssh) 
      files = sftp.listdir(dirPath)
      print "[+] Listing All the files on the given directory "
      for f in files:
         print os.path.join(dirPath,f) 
      
      thefile = str(raw_input("[+] Please Enter the files you wish to download: " ))
      self.getFiles(thefile)

   # this function dowload the files
   def getFiles(self,thefile): 
      
      sftp = paramiko.SFTPClient.from_transport(self.ssh) 
      print "[+] Retrieving --> " + thefile 
      newFile = os.path.basename(thefile) 

      sftp.get(thefile,newFile)
      self.ssh.close() 
   
