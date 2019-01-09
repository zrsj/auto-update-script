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
	cursor.execute("SELECT * from employees")
	rec = cursor.fetchall()
	pprint.pprint(rec)
if __name__ == "__main__":
	main() 
