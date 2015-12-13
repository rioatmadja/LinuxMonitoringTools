#!/usr/bin/env python 
import paramiko,getpass,socket,sys,termios,tty,select
from paramiko.py3compat import u

class remote_session: 
   def __init__(self,hostname,uname,passwd):
      self.uname = uname 
      self.passwd = passwd 
      self.hostname = hostname

      try: 
         self.ssh = paramiko.SSHClient() 
         self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         self.ssh.connect(hostname,username=uname, password=passwd)
      except (paramiko.BadHostKeyException, paramiko.AuthenticationException,paramiko.SSHException) as e:
         print str(e)
         sys.exit(-1)

      chan = self.ssh.invoke_shell() 
      interactive_shell(chan) 

# spawn a shell 
def interactive_shell(chan):
    
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())

        while True:

            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n logout \r\n')
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    

