#!/usr/bin/python3
import psycopg2
import sys
import pprint

def main():
	conn_str = "host='localhost' dbname='northwind' user='postgres' password='admin'"
	print("Connecting to database...")
	conn = psycopg2.connect(conn_str)
	cursor = conn.cursor()
	print("Connected!")
	conn.set_session(autocommit=True)
	with open("/home/uniwork/workforce/app1/sql/query.sql") as file:
		for line in file:
			str = file.read()
			cursor.execute(str)
if __name__ == "__main__":
	main() 
