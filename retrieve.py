#!/usr/bin/python3
import psycopg2
import sys
import pprint

def query_exec(conn_str, query_direc, data_direc):
	conn = psycopg2.connect(conn_str)
	cursor = conn.cursor()
	conn.set_session(autocommit=True)
	str = ""
	with open(query_direc, "r") as ifile:
		for line in ifile:
			str += line
	outquer = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(str)
	with open(data_direc, "w") as ofile:
		cursor.copy_expert(outquer, ofile)
	conn.close()

def main():
	conn_str = "host='localhost' dbname='northwind' user='postgres' password='admin'"
	idir1 = "/home/uniwork/workforce/app1/sql/query.sql"
	odir1 = "/home/uniwork/workforce/app1/data/results.csv"
	print("Beginning execution...")
	try:
		query_exec(conn_str, idir1, odir1)
	except:
		print("ERROR: execution failure")
	print("Execution succesfully completed. Data CSV files created.")
if __name__ == "__main__":
	main() 
