#!/usr/bin/env python 
import paramiko,sys,os,socket,threading 

class ssh_session:

	# this function is responsible for remote command execution	
	def __init__(self,hostname,uname,passwd,cmd):
		self.uname = uname 
		self.passwd = passwd 
		self.hostname = hostname
		self.command = '' # command to be executed on the remote server 

		try: 
			self.ssh = paramiko.SSHClient() 
			self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.ssh.connect(hostname,username=uname, password=passwd)
		except (paramiko.BadHostKeyException, paramiko.AuthenticationException,paramiko.SSHException) as e:
			print str(e)
			sys.exit(-1)
	

		try:
			channel = self.ssh.invoke_shell() 
			timeout = 3600
			channel.settimeout(timeout)
			line_buffer = ''
			channel_buffer = '' 
			channel.send(cmd + ' ; exit ' + '\r' ) 

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

	
