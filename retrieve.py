#!/usr/bin/python3
import psycopg2
import sys
import pytoml as toml
import os
from folder import folder
from apscheduler.schedulers.blocking import BlockingScheduler

def increment_string(string):
	val = int(string)
	retval = "0" + str(val + 1) if val < 9 else str(val + 1)
	return retval

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
	foldernames = next(os.walk(rootdir))[1]
	foldernames.remove(".git")
	foldernames.sort()
	idirs = []
	odirs = []
	for x in foldernames:
		#idirs.append(rootdir + "/{0}/sql/query.sql".format(x))
		if x.startswith("app"):
			ifolder = folder(rootdir + "/{0}/sql/".format(x))
			ofolder = folder(rootdir + "/{0}/data/".format(x))
			idirs.append(ifolder)
			odirs.append(ofolder)
		#odirs.append(rootdir + "/{0}/data/".format(x))
	for x, y in zip(idirs, odirs):
		f = []
		fln = "00"
		try:
			f = next(os.walk(x.dirnm))[2]
		except StopIteration:
			pass
		for z in f:
			if z.endswith(".sql"):
				x.add_file(z)
				y.add_file("data{0}.csv".format(fln))
				fln = increment_string(fln)
	try:
		for x, y in zip(idirs, odirs):
				for z, w in zip(x.files, y.files):
					query_exec(conn_str, z, w)
					print("Completed successfully!")
	except FileNotFoundError as e:
		print("NOTE: {0}".format(str(e)))
		print("If a query should exist within this dir, filepath must match")
	#except Exception as e:
	#	print("FAILURE: {0}".format(str(e)))

def main():
	script_run(sys.argv[1])
	sched = BlockingScheduler()
	try:
		sched.add_job(script_run, 'cron', year='*', month='*',  day='*', hour=9, minute=3, args=[sys.argv[1]])
	except:
		sched.add_job(script_run, 'cron', year='*', month='*', day='*', hour=7, minute=00)
	try:
		sched.start()
	except (KeyboardInterrupt, SystemExit):
		pass

if __name__ == "__main__":
	main()
