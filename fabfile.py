#!/usr/bin/env python

from fabric.api import *
from fabric.colors import *
import cuisine

print green('Start', bold=True)
env.passwords = {
	'root@198.50.141.68:22': '1P@ssw0rd9',
	'root@198.50.141.69:22': '1P@ssw0rd9',
	'root@198.50.141.70:22': '1P@ssw0rd9',
}
env.roledefs = {
	'web': [ '198.50.141.69', '198.50.141.70' ],
	'db': [ '198.50.141.69', '198.50.141.70' ],
	'devpanel_nodes': [ '198.50.141.68' ]
}
db_daemons_conf = {}
db_shadow_conf = {}


@roles('devpanel_nodes')
def get_devpanel_config():
	print env.host
	with hide('output','running','warnings'):
		with show(): print green('[%s] Retrieving db-daemons.conf' % env.host, bold=True)
		for line in iter(cuisine.file_read('/opt/webenabled/compat/dbmgr/config/db-daemons.conf').splitlines()):
			if line.startswith('#'): continue
			db_daemons_conf[env.host] = line.split(':')
		with show(): print green('[%s] Retrieving db-shadow.conf' % env.host, bold=True)
		for line in iter(cuisine.file_read('/opt/webenabled/compat/dbmgr/config/db-shadow.conf').splitlines()):
			if line.startswith('#'): continue
			db_shadow_conf[env.host] = line.split(':')

		# Test MySQL access
		# args -N removes colum name and -B for batch (no design)
		test_mysql_access = run('mysql -NB -uroot -p1P@ssw0rd9 -e \'SELECT "OK" FROM DUAL\' ; true').endswith('OK')

@roles('web')
def setup_web():
	with hide('output','running','warnings'):
		cuisine.run('hostname -f')
		x = cuisine.command_check('ls -al')

@roles('db')
def setup_db():
	cuisine.run('uname -a')

if __name__ == '__main__':
	execute(get_devpanel_config)
	execute(setup_web)
	execute(setup_db)
