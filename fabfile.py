#!/usr/bin/env python

from fabric.api import *
from fabric.colors import *
import cuisine
import collections
import json
import re

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
# {'198.50.141.68':
#     ['b_d4t4s1', # app mysql user
#     'mysql',     # database type
#     'any',       # ?
#     '/home/clients/databases/b_d4t4s1/mysql', # app db dir
#     '127.0.0.1', # mysqld IP
#     '4000',      # mysqld port
#     '',
#     '',
#     'ZgUUrFBa2W']} # password

# this is where we're gonna save the info of the devpanel node
devpanel_node = {}


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

@roles('devpanel_nodes')
def prepare_db():
	mysql_opts = '--skip-column-names -NAB -u%s -h%s -P%s' % ('root', db_shadow_conf[env.host][4], db_shadow_conf[env.host][5])

	devpanel_node[env.host] = { 'db': {} }

	with hide('output','running'):
		# Test MySQL access
		if run('mysql %s -e \'SELECT "OK" FROM DUAL\' ; true' % mysql_opts).endswith('OK'):
			# connected to mysql successfully,
			# proceed with dumping users
			mysql_query = "select concat(user,'|',host,'|',password) from mysql.user where user != '' and host != ''"
			mysql_res = run('mysql %s -e "%s"' % (mysql_opts, mysql_query))
			mysql_useraccounts = []
			for line in mysql_res.split('\n'):
				arr = line.strip().split('|')
				mysql_query = "SHOW GRANTS FOR '%s'@'%s'" % (arr[0], arr[1])
				with settings(warn_only=True):
					mysql_res = run('mysql %s -e "%s"' % (mysql_opts, mysql_query))
				if mysql_res.return_code != 0: continue
				mysql_useraccounts.append({ 'user': arr[0], 'properties': {'host': arr[1], 'pass_hash': arr[2], 'grants': mysql_res.strip().split('\r\n') }})
			# push users data to dictionary
			devpanel_node[env.host]['db'].update(users = mysql_useraccounts)
#			print json.dumps(devpanel_node, indent=2)

		else:
			print 'Error accessing database @ %s' % env.host
			raise

@roles('devpanel_nodes')
def dump_schemas():
	mysql_opts = '--skip-column-names -NAB -u%s -h%s -P%s' % ('root', db_shadow_conf[env.host][4], db_shadow_conf[env.host][5])

	with hide('output','running'):
		mysql_query = 'show databases'
		# get list of databases
		mysql_res = run('mysql %s -e "%s"' % (mysql_opts, mysql_query))
		mysql_database = mysql_res.strip().split('\r\n')
		for unused_db in [ 'information_schema', 'performance_schema', 'mysql', 'test' ]:
			mysql_database.remove(unused_db)

		print green('[%s] Schema(s) to dump: %s' % (env.host, mysql_database))
		for schema_to_dump in mysql_database:
			run('mysqldump -u%s -h%s -P%s --databases %s > /tmp/%s.sql' % ('root', db_shadow_conf[env.host][4], db_shadow_conf[env.host][5], schema_to_dump, schema_to_dump))
			print green('[%s] Schema %s dumped to /tmp/%s.sql' % (env.host, schema_to_dump, schema_to_dump))

@roles('devpanel_nodes')
def disable_services():
	with hide('output', 'running'):
		with settings(warn_only=True):
			for service in ['devpanel-taskd', 'devpanel-dbmgr']:
				if cuisine.file_exists('/etc/init/%s.conf' % service):
					run('echo mv /etc/init/%s.conf /etc/init/%s.conf.disabled' % (service, service))
				if cuisine.file_exists('/etc/init.d/%s' % service):
					run('echo update-rc.d %s disabled' % service)



if __name__ == '__main__':
	execute(get_devpanel_config)
	execute(prepare_db)
	execute(dump_schemas)
	execute(disable_services)
#	execute(setup_web)
#	execute(setup_db)



# split grants
#				mysql_user_grant = []
#				for line_grant in mysql_res.strip().split('\r\n'):
#					line_split = re.split("GRANT (.*) ON (.*) TO '[^']+'@'[^']+'(( IDENTIFIED BY [A-Z]+ .*){0,1} WITH (.*)){0,1}", line_grant, flags=re.I)
#					mysql_user_grant.append(line_split)

