#!/usr/bin/python3
#Author: zrsj
#Date of creation: 09/01/2019
#Description: retrieval script that executes sql at 7am every day
import psycopg2 #postgres driver for executing sql
import sys #currently used for command line arguments
import pytoml as toml #used to read in database config file
import os #used to crawl through directories and retrieve folder names
import threading #anytime_exec daemon runs on a thread
from folder import folder #folder class, see folder.py for details
from apscheduler.schedulers.blocking import BlockingScheduler #scheduler
#function increment_string() takes in a string that resembles an integer,
#converts it to such and then increments it, returning a double digit value
#depending on whether it is less than 9 or not
def increment_string(string):
	val = int(string)
	retval = "0" + str(val + 1) if val < 9 else str(val + 1)
	return retval
#function parse_dbconfig reads in database configuration information from a
#config file using toml
def parse_dbconfig(filenm='config.toml'):
	data = toml.load(open(filenm))
	vals = data['database']
	confvals = [vals['host'], vals['dbname'], vals['user'], vals['password']]
	return(confvals)
#function query_exec connects to the database, initialises a cursor and then
#uses said cursor to execute a query, outputing it to a csv file to a specified
#output directory
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
#function script_run performs bulk of the work. Takes in the root directory as
#an argument and then uses this to crawl directories for folder names. These
#folders are turned into abstract folder objects and stored in arrays
def script_run(rootdir = "./workforce"):
	try:
		conn_vals = parse_dbconfig(rootdir + '/config.toml')
	except:
		conn_vals = parse_dbconfig()
	conn_str = "host='{}' dbname='{}' user='{}' password='{}'".format(conn_vals[0], conn_vals[1], conn_vals[2], conn_vals[3])
	foldernames = next(os.walk(rootdir))[1]
	foldernames.remove(".git")
	foldernames.sort()
	idirs = []
	odirs = []
	for x in foldernames:
		idirs.append(folder(rootdir + "/{0}/sql/".format(x)))
		odirs.append(folder(rootdir + "/{0}/data/".format(x)))
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
	except Exception as e:
		print("FAILURE: {0}".format(str(e)))

class anytime_exec(threading.Thread):
	def run(self):
		print("Will execute at any time upon entering 'n'.")
		print("This daemon will terminate upon entering 'e'.")
		character = input()
		while character != 'e':
			if character == 'n':
				try:
					script_run(sys.argv[1])
					character = input()
				except:
					script_run()
					character = input()
		print("Anytime execution daemon terminated. Scheduler still runs.")

def main():
	thread = anytime_exec(name = "th", daemon=True)
	thread.start()
	sched = BlockingScheduler()
	try:
		sched.add_job(script_run, 'cron', year='*', month='*',  day='*', hour=15, minute=12, args=[sys.argv[1]])
	except:
		sched.add_job(script_run, 'cron', year='*', month='*', day='*', hour=7, minute=0)
	try:
		sched.start()
	except (KeyboardInterrupt, SystemExit):
		pass

if __name__ == "__main__":
	main()
