#!/usr/bin/env python
import os
def file(client,filename,dst):
    cmd = "salt %s cp.get_file salt://%s %s"%(client,filename,dst)
    result = os.popen(cmd).read()
    return result
if __name__=='__main__':
    blue =  file('client','upload/test.txt','/tmp/1.txt')
    print blue
