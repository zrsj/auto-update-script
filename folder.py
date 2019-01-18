#Author: zrsj
#Date of creation: 17/01/2019
#Description: a class that provides a very abstract definition of a folder
class folder:
	#constructor takes self and directory name as arguments, initialises
	#files to be an empty array and sets its directory name to dirnm
	def __init__(self, dirnm=""):
		self.dirnm = dirnm
		self.files = []
	#function get_dirname is to be used on any folder object to return its
	#directory name as a string
	def get_dirnm(self):
		return self.dirnm
	#function has_files is to be used on any folder object and returns a
	#boolean when called. TRUE if files exist in the files array, else FALSE
	def has_files(self):
		has = True if len(self.files) > 0 else False
		return has
	#function add_file is to be used on any folder object and appends a file
	#name to the folder's files array
	def add_file(self, filenm):
		self.files.append(self.dirnm + filenm)
	#function printfl is to be used on any folder object to print every file
	#name that currently exists in the folder's files array
	def printfl(self):
		for x in self.files:
			print(x)
	#function make_filedirs is to be used on folder objects that have at
	#least one file and returns an array of all files with the directory
	#name of the folder attatched to the front of all files in the array
	def make_filedirs(self, filter=""):
		retarr = []
		for x in self.files:
			if x.endswith(filter):
				retarr.append(self.dirnm + x)
		return retarr
