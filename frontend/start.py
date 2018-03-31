from subprocess import Popen, PIPE
import os

ip = '127.0.0.1'
port = ':8000'

farmstar_scripts = os.path.join('farmstar','farmstar_scripts','run.py')
farmstar_django = os.path.join('farmstar','manage.py')

##farmstar = call('python '+farmstar_scripts)
##django = call('python '+farmstar_django+' runserver '+ip+port)

bot1 = Popen(["cmd", "python", farmstar_scripts], stdout=PIPE, stderr=PIPE, stdin=PIPE)
