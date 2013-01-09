#!/usr/bin/env python
""" This module show how to call opensees from python and do the redirection"""

import shlex, subprocess
import time
import sys,os
import signal
folder = os.path.dirname(os.path.realpath(__file__))

def terminate_process(pid):
    # all this shit is because we are stuck with Python 2.5 and \ we cannot use Popen.terminate()
    if sys.platform == 'win32':
        import ctypes
        PROCESS_TERMINATE = 1
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
        ctypes.windll.kernel32.TerminateProcess(handle, -1)
        ctypes.windll.kernel32.CloseHandle(handle)
    else:
        os.kill(pid, signal.SIGKILL)

def run_OpenSees_abs(sourcefile,version='2.1.0'):
    # define subprocess
    if version == '2.1.0':
        OP=subprocess.Popen(os.path.join(folder,'openSees.exe'),
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
    elif version == '2.4.0':
        OP=subprocess.Popen(os.path.join(folder,'OpenSees_2_4.exe'),
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)        
    
    # link the pipe 
    flag = OP.stdout
    pipe = OP.stdin
    
    # write the opensees file
    pipe.write('source '+ sourcefile + '\n')
    print flag.readline()
    
    pipe.write('quit\n')
    #terminate_process(OP.pid)
    #ret_code = OP.wait()
    #logfile.flush()
    return 1



def run_OpenSees(sourcefile):
    # define subprocess
    OP=subprocess.Popen(os.path.join(folder,'openSees.exe'),
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
    
    # link the pipe 
    flag = OP.stdout
    pipe = OP.stdin
    
    # write the opensees file
    pipe.write('source '+ 'source'+ r'/'+ sourcefile + '\n')
    print flag.readline()
    
    #retcode = OP.wait()

    return 1

def run_OpenSees_interact(sourcefile,loopfun,logfile=None):
    """
    Interactive analysis with initial inputs and looping function
    """

    # create the subprocess by calling opensees ar the default location
    # and also redirect the standard out and error
    OP=subprocess.Popen(os.path.join(folder,'openSees.exe'),
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
    
    # link the pipe 
    flag = OP.stdout
    pipe = OP.stdin
    
    # write the opensees file
    pipe.write('source '+ 'source'+ r'/'+ sourcefile + '\n')
    
    #
    time.sleep(1)
    print flag.readline()  ## this is to read the end of analysis and make the stops
    
    if logfile != None:
        logfile.write(sourcefile)
    
    # start to loop within OpenSees
    nloop = 0
    while 1:
        nloop += 1
        updates = loopfun(nloop)             ## Call external functions
        if updates == None:
            str1 = 'stop looping at loop number:"' +str(nloop)

            pipe.write('quit\n')
            
            if logfile != None:
                logfile.write(str1)
                
            logfile.flush()
            break
        else:
            print 'now looping:"' +str(nloop)

            pipe.write(updates)
            if logfile != None:
                logfile.write(updates)
            
            #self.pipe.write('analyze '+ str(step) + '\n')
            #self.pipe.write("puts 'Analyze_Done'\n")
            if logfile != None:
                logfile.write('analyze '+ str(step) + '\n')
                logfile.write("puts 'Analyze_Done'\n")
                
                logfile.flush()
            
            print flag.readline()  ## this is to read the end of analysis and make the stops
            