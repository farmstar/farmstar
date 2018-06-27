import sys
import subprocess
import os
import time
import argparse
import webbrowser

'''
Farmstar start
Launches backend and django frontend
Needs to be run from terminal or run .bat / .sh
'''

#Python executable
python = sys.executable

#Current working directory
cwd = str(os.getcwd())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help='WebUI binding IP (127.0.0.1)')
    parser.add_argument('--port', type=str, default=':8000',
                        help='WebUI binding port (:8000)')
    parser.add_argument('--backend', type=str, default='y',
                        help='Run backend scripts? (y/n)')
    parser.add_argument('--frontend', type=str, default='y',
                        help='Run frontend scripts? (y/n)')
    args = parser.parse_args()
    sys.stdout.write(str(launch(args)))


def launch(args):
    if sys.version_info[0] < 3:
        raise "Must be using Python 3.x"
    
    if args.frontend == 'y':
        binding = args.ip+args.port
        frontend(binding)
        time.sleep(5)
        chrome(binding)
        
    if args.backend == 'y':
        backend()
    

def frontend(binding):
    #Front end webui os command arguments
    frontend_dir = os.path.join(cwd, 'frontend', 'django', 'farmstar', 'manage.py')
    frontend_args = ' runserver '+binding
    frontend_run = python+' '+'"'+frontend_dir+'"'+' '+frontend_args

    if os.name == 'nt':
        frontend_cmd = 'start cmd /K '+frontend_run
        os.system(frontend_cmd)
    elif os.name == 'posix':
        pass


def chrome(binding):
    #Cross platform chrome launcher
    
    if os.name == 'mac':
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    elif os.name == 'nt':
        chrome_path = '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s'
    elif os.name == 'posix':
        chrome_path = '/usr/bin/google-chrome %s'

    webbrowser.get(chrome_path).open(binding)
    

def backend():
    backend_dir = os.path.join(cwd, 'backend','scripts')
    backend_run = python+' '+'"'+backend_dir+'"'+'/fs_run.py'
    backend_cmd = 'start cmd /K '+backend_run
    os.system(backend_cmd)
    

if __name__ == '__main__':
    main()




