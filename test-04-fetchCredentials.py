from settings import *
import os, pexpect, sys

if os.path.exists("eucarc"):
    print "We appear to already have credentials - skipping this step"
    sys.exit(0)

#SSH code obtained from http://linux.byexamples.com/archives/346/python-how-to-access-ssh-with-pexpect/

ssh_newkey = 'Are you sure you want to continue connecting'

#Login to the clc and fetch creds for our test account
p=pexpect.spawn('ssh root@' + console_ip +  ' euca_conf --cred-account=test --cred-user=admin --get-credentials=test_cred.zip')

i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==0:
    p.sendline('yes')
    i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==1:
    p.sendline(root_password)
    p.expect(pexpect.EOF)
elif i==2:
    pass

#scp the creds down to the box running the test suite
p=pexpect.spawn('scp root@' + console_ip +  ':test_cred.zip ./')

i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==0:
    p.sendline('yes')
    i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==1:
    p.sendline(root_password)
    p.expect(pexpect.EOF)
elif i==2:
    pass

os.system('unzip test_cred.zip')
