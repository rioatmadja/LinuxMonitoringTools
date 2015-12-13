#!/usr/bin/env python 
# coding: latin-1
########################################################
# Name: Rio Atmadja
# Date: 11/26/2015
########################################################
import os,sys,re,psutil,getpass,threading,paramiko,urllib2
from sshSession import * 
from fuzzywuzzy import fuzz 

# this function will print the banner to the screen 
def banner(): 
   print """
\033[31m 
####################################################################################
                                                                                
 ▄▄▄▄         ██                                             ▄▄▄▄▄▄       ▄▄▄▄  
 ▀▀██         ▀▀                                             ██▀▀▀▀██   ██▀▀▀▀█ 
   ██       ████     ██▄████▄  ██    ██  ▀██  ██▀            ██    ██  ██▀      
   ██         ██     ██▀   ██  ██    ██    ████              ███████   ██       
   ██         ██     ██    ██  ██    ██    ▄██▄              ██  ▀██▄  ██▄      
   ██▄▄▄   ▄▄▄██▄▄▄  ██    ██  ██▄▄▄███   ▄█▀▀█▄             ██    ██   ██▄▄▄▄█ 
    ▀▀▀▀   ▀▀▀▀▀▀▀▀  ▀▀    ▀▀   ▀▀▀▀ ▀▀  ▀▀▀  ▀▀▀            ▀▀    ▀▀▀    ▀▀▀▀  

####################################################################################

   1. Monitor Overall Performance 
   2. Spawn Shell 
   3. Update Servers
   4. Upload to the Servers
   5. Download from the Servers
   6. View Network Loads 
   7. Capture Network Traffic 
   8. Execute Remote Command 
   9. Remote Kernel Exploit  

"""
# get user's credentials 
def getCreds(): 
   hostname = str(raw_input("[+] Please Enter IP Address: "))
   username = str(raw_input("[+] Please Enter your username: " )) 
   password = getpass.getpass()  
   return hostname,username,password 


# run this script 
def runProgram(): 
   banner() # print the banner to the screen 
   args = input("[+] Please Enter Your Options: ")
   
   if( args == 1):
      print "[+] Under Development "

   elif( args == 2):
      hostname,username,password = getCreds() 
      shell = remoteShell.remote_session(hostname,username,password) 

   elif( args == 3):
      
      hostname,username,password = getCreds() 
      if "," in hostname: 
         threads = []
         
         for ip in hostname.split(","): 
            print "[+] Connecting to the IP: " + ip 
            #server_update = updateSystem.remote_session(ip,username,password) 
            t = threading.Thread(target=updateSystem.remote_session, args = (ip,username,password,))
            threads.append(t)
            t.start()
            t.join() 
      else: 
            server_update = updateSystem.remote_session(hostname,username,password) 


   elif( args == 4):
      hostname,username,password = getCreds() 
      thefile = str(raw_input("[+] Please Enter the files you wish to upload: " ))
      sftp = uploadFile.upload_files(hostname,username,password) 
      sftp.getFiles(thefile) 

   elif( args == 5):
      hostname,username,password = getCreds() 
      getAnswer = str(raw_input( "[+] Do you know the file to download [yes/no]: "))

      if "no" in getAnswer:
         getPath = str(raw_input( "[+] Please Enter the Directory Path : "))
         sftp = downloadFile.download_files(hostname,username,password) 
         sftp.listFiles(getPath) 

      elif "yes" in getAnswer: 
         getPath = str(raw_input( "[+] Please Enter the file you wish to download : "))
         sftp = downloadFile.download_files(hostname,username,password) 
         sftp.getFiles(getPath) 

      else:
         print "[+] Unkown Command, Good Bye "
         sys.exit(-1)

   elif( args == 6):
      print "[+] Under Development "

   elif( args == 7):
      print "[+] Under Development "

   # remote command execution 
   elif( args == 8):
      hostname,username,password = getCreds() 
      cmd = str(raw_input("[+] cmd > : "))
      
      # use thread if more than one ip 
      if "," not in hostname: 
         execute_cmd = executeCMD.ssh_session(hostname,username,password,cmd) 
      else:
         threads = [] 
         for ip in hostname.split(","):
            print "\n[+] Connecting to the following: " + ip 
            t = threading.Thread(target=executeCMD.ssh_session, args = (ip,username,password,cmd,))
            threads.append(t)
            t.start()
            t.join() 

   elif( args == 9):
      
      if os.path.exists('./exploit.txt'):
         pass 

      else: 
         
         userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
         headers = { 'User-Agent' : userAgent } 
         url = "https://raw.githubusercontent.com/offensive-security/exploit-database/master/files.csv"
         
         try:
            request = urllib2.Request(url,None,headers)
            files = urllib2.urlopen(request)
            write_file = open("exploit.txt", 'w') 
            write_file.write(files.read()) 
            write_file.close()
            print "[+] Downloading from exploit-db: " + url

         except:
            print "[X] Unable to Connect to the internet "
            sys.exit(-1) 
            
      hostname,username,password = getCreds() 
      kernel_version = remoteKernel.check_kernel(hostname,username,password) 
      
      kernel_version.checkExploit() 
      
   else:
      print "[X] Number out of range " 
      
if __name__ == "__main__": 

# try to parse the command and detect for interupt 
   try:
      runProgram() 
   except KeyboardInterrupt:
      print "\n\n Exiting the program <ctrl+c>"
   except:
      sys.exit() #exit out this program 
