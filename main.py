import os
import rsa
import shelve

class Student():
	def __init__(self, data, github):
		self.last = data[0]
		self.first = data[1]
		self.pref = data[2]
		self.period = data[3]
		self.github = github
	def __str__(self):
		rep = f"{self.last}, "
		if self.pref:
			rep += f"{self.pref} ({self.first}), "
		else:
			rep += f"{self.first}, "
		rep += f"{self.github}, P{self.period}"
		return rep

def generate_keys():
	print("WARNING\n\tExisting messages will be unextractable with new keys.")
	if input("Continue?(Y/n)\n").lower() in ('y','yes'):
		public, private = rsa.newkeys(1024)
		with open("public.pen", 'wb') as f:
			f.write(public.save_pkcs1('PEM'))
		with open("private.pen", 'wb') as f:
			f.write(private.save_pkcs1('PEM'))
		print("New public and private keys have been generated.")

def extract():
	if os.path.exists("private.pen"):
		with open("private.pen", 'rb') as f:
			private = rsa.PrivateKey.load_pkcs1(f.read())
	else:
		print("Could not locate 'private.pen' file")
	students = {}
	os.chdir('students')
	#create a list of files that have the extension .txt
	files = [f for f in os.listdir() if os.path.isfile(f) and ".dat" in f]
	for f in files:
		with open(f,'rb') as t:
			msg = t.read()
		decoded = rsa.decrypt(msg, private).decode('ascii')
		data = decoded.split(',')
		github = f.replace('.dat','')
		students[github] = Student(data, github)
	os.chdir('..')
	f = shelve.open('students.dat')
	for name in students.keys():
		print(type(students[name]))
		f[name] = students[name]
	f.close()

def check():
	data = shelve.open('students.dat')
	for e in data:
		print(data[e])
	data.close()

def main():
	print(
'''
\tMENU
1 - Extract data
2 - Check database
3 - Generate Keys
0 - Quit
''')
	op = -1
	while op not in range(3):
		try:
			op = int(input("What's your choice?\n"))
		except ValueError:
			print("That wasn't a number.")
	if op == 1:
		#extract username
		extract()
	elif op == 2:
		check()
	elif op == 3:
		#generate keys
		generate_keys()

if __name__ == "__main__":
	main()
