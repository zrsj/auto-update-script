#!/usr/bin/python3
import psycopg2
import sys
import pytoml as toml
import os
from apscheduler.schedulers.blocking import BlockingScheduler

def parse_dbconfig(filenm='config.toml'):
	data = toml.load(open('config.toml'))
	vals = data['database']
	confvals = [vals['host'], vals['dbname'], vals['user'], vals['password']]
	return(confvals)

def query_exec(conn_str, query_direc, data_direc):
	conn = psycopg2.connect(conn_str)
	cursor = conn.cursor()
	conn.set_session(autocommit=True)
	str = ""
	with cursor as cursor:
		str = open(query_direc).read()
		outquer = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(str)
		with open(data_direc, "w") as ofile:
			cursor.copy_expert(outquer, ofile)
	conn.close()

def script_run(rootdir = "./workforce"):
	conn_vals = parse_dbconfig()
	conn_str = "host='{}' dbname='{}' user='{}' password='{}'".format(conn_vals[0], conn_vals[1], conn_vals[2], conn_vals[3])
	folders = next(os.walk(rootdir))[1]
	folders.remove(".git")
	idirs = []
	odirs = []
	for x in folders:
		idirs.append(rootdir + "/{0}/sql/query.sql".format(x))
		odirs.append(rootdir + "/{0}/data/data.csv".format(x))
	try:
		for x in range(len(folders)):
			query_exec(conn_str, idirs[x], odirs[x])
	except:
		print("ERROR: execution failure")
	print("Executed successfully")

def main():
	sched = BlockingScheduler()
	try:
		sched.add_job(script_run, 'cron', year='*', month='*',  day='*', hour=15, minute=16, args=[sys.argv[1]])
	except:
		sched.add_job(script_run, 'cron', year='*', month='*', day='*', hour=7, minute=00)
	try:
		sched.start()
	except (KeyboardInterrupt, SystemExit):
		pass

if __name__ == "__main__":
	main()
