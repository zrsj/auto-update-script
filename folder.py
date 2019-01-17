class folder:
	def __init__(self, dirnm=""):
		self.dirnm = dirnm
		self.files = []
	def get_dirnm(self):
		return self.dirnm
	def has_files(self):
		has = True if len(self.files) > 0 else False
		return has
	def add_file(self, filenm):
		self.files.append(self.dirnm + filenm)
	def printfl(self):
		for x in self.files:
			print(x)
	def make_filedirs(self, filter=""):
		retarr = []
		for x in self.files:
			if x.endswith(filter):
				retarr.append(self.dirnm + x)
		return retarr
