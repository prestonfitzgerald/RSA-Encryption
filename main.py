import os, rsa, shelve

class Student():
	def __init__(self, data, github):
		self.period = data[3]
		self.weber = data[4]
		self.github = github
		self.name = f"{data[0]}, {data[1]}"
		if data[2]:
			self.name += f" ({data[2]})"		
	def __str__(self):
		rep = f"{self.name}, {self.github}, P{self.period}, {self.weber}"
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
		return
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
	with shelve.open('students.dat') as f:
		for name in students.keys():
			print(type(students[name]))
			f[name] = students[name]
	print("students.dat created")

def check():
	if os.path.exists('students.dat'):
		with shelve.open('students.dat') as data:
			for e in data:
				print(data[e])
	else:
		print("students.dat does not exist!")

def imports():
	if os.path.exists('students.dat'):
		out = ""
		with shelve.open('students.dat') as data:
			for e in data:
				out += f"{data[e].weber}, "
		with open('import.txt','w') as f:
			f.write(out)
		print("import.txt created")
	else:
		print("students.dat does not exist!")

def main():
	print(
'''
\tMENU
1 - Extract data
2 - Check database
3 - Create canvas import file
4 - Generate Keys
0 - Quit
''')
	op = -1
	while op not in range(5):
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
		imports()
	elif op == 4:
		#generate keys
		generate_keys()

if __name__ == "__main__":
	main()
