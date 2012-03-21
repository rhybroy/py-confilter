#encoding:utf-8
#!/usr/bin/python 
#Author:troycheng
#Email:frostmourn716@gmail.com

import os
import atexit
import time
from confilter import *
from signal import SIGTERM

class Daemon:
    '''
    A generic daemon class

    Usage: subclass the Daemon class and override the _run() method
    '''

    def __init__(self, pidfile, stdin="/dev/null", stdout="/dev/null",\
            stderr="/dev/null"):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def _daemonize(self):
        '''
        do the UNIX double-fork magic
        '''

        # Perform the first hook
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError,e:
            sys.stderr.write("fork #1 failed. %d (%s)\n" % (e.errno,\
                e.strerror))
            sys.exit(1)

        # Decouple from parent environment
        os.setsid()
        os.chdir('/')
        os.umask(0)

        # Perform second fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit()
        except OSError,e:
            sys.stderr.write("fork #2 failed. %d (%s)\n" %(e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)

        # Redirect stdin, stdout, stderr
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # Bind exit handler
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write('%s\n' % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        # check the pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # start the Daemon
        self._daemonize()
        self._run()

    def stop(self):
        # get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return

        # try killing the daemon Process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, e:
            e = str(e)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print err 
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def _run(self):
        '''
        You should override this method when you subclass Daemon. it will be
        called after the Process has been daemonized by start() or restart()
        '''

class ConfilterDaemon(Daemon):

    def __init__(self, stdin="/dev/null", stdout="/dev/null",\
            stderr="/dev/null"):
        pidfile = CUR_PATH + "../.confilter_service.pid"
        Daemon.__init__(self, pidfile, stdin, stdout, stderr)

    def _run(self):
        runConfilter()

if __name__ == "__main__":
    daemon = ConfilterDaemon()
    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            log.info("Confilter Service start.")
            print "Confilter Service start"
            daemon.start()
        elif "stop" == sys.argv[1]:
            log.info("Confilter Service stop.")
            print "Confilter Service stop"
            daemon.stop()
        elif "restart" == sys.argv[1]:
            log.info("Confilter Service restart.")
            print "Confilter Service restart"
            daemon.restart()
        else:
            print "Unknown command, valid param: start/stop/restart"
            sys.exit(2)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)


