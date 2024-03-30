import win32serviceutil
import win32service
import win32event
import socket
import os

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskService"
    _svc_display_name_ = "Flask Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        import subprocess
        cwd = os.path.dirname(os.path.realpath(__file__))
        subprocess.Popen(["python", "run.py"], cwd=cwd)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
