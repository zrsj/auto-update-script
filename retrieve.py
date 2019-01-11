#!/usr/bin/python3
import psycopg2
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

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
	conn_str = "host='localhost' dbname='northwind' user='postgres' password='admin'"
	idir1 = rootdir + "/app1/sql/query.sql"
	idir2 = rootdir + "/app2/sql/query.sql"
	idir3 = rootdir + "/app3/sql/query.sql"
	odir1 = rootdir + "/app1/data/results.csv"
	odir2 = rootdir + "/app2/data/results.csv"
	odir3 = rootdir + "/app3/data/results.csv"
	try:
		query_exec(conn_str, idir1, odir1)
		query_exec(conn_str, idir2, odir2)
		query_exec(conn_str, idir3, odir3)
	except:
		print("ERROR: execution failure")

def main():
	try:
		script_run(sys.argv[1]);
	except:
		script_run();
	sched = BlockingScheduler()
	sched.add_job(script_run, 'cron', year='*', month='*',  day='*', hour=7, minute=00)
	try:
		sched.start()
	except (KeyboardInterrupt, SystemExit):
		pass

if __name__ == "__main__":
	main()
