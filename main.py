import os
import rsa

class Student():
	def __init__(self, last, first, pref, period, github):
		self.last = last
		self.first = first
		self.pref = pref
		self.period = period
		self.github = github

def generate_keys():
	print("WARNING\n\tExisting messages will be unextractable with new keys.")
			if input("").lower() in ('y','yes'):
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
		print('Could not locate 'private.pen' file")

	#create a list of files that have the extension .txt
	#for each encoded .txt file
	decoded = rsa.decrypt(msg, private).decode('ascii')
	data = decoded.split(',')

def main():
	print(
'''
\tMENU
1 - Extract usernames
2 - Generate Keys
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
		#generate keys
		generate_keys()

if __name__ == "__main__":
	main()