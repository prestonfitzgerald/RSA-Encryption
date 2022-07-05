import os
import csv
try:
	import rsa
except:
	print("RSA module neede -- installing")
	os.system("pip install rsa")
	import rsa

def generate_keys():
	public, private = rsa.newkeys(1024)
	with open("public.pen", 'wb') as f:
		f.write(public.save_pkcs1('PEM'))
	with open("private.pen", 'wb') as f:
		f.write(private.save_pkcs1('PEM'))
	
def load_keys():
	with open("Simonsen_public.pen", 'rb') as f:
		public = rsa.PublicKey.load_pkcs1(f.read())
	with open("Simonsen_private.pen", 'rb') as f:
		private = rsa.PrivateKey.load_pkcs1(f.read())
	return public, private

def encrypt(msg, key):
	return rsa.encrypt(msg.encode('ascii'), key)

def decrypt(msg, key):
	try:
		return rsa.decrypt(msg, key).decode('ascii')
	except:
		return False

def test():
	public, private = load_keys()
	with open("mrsimonsen.dat", 'rb') as f:
		msg = f.read()
	print(decrypt(msg, private))

def create_csv():
	#load Simonsen_private key
	with open("Simonsen_private.pen", 'rb') as f:
		private = rsa.PrivateKey.load_pkcs1(f.read())
	#create a master list of all files in repo with .dat extension
	files = [f for f in os.listdir() if os.path.isfile(f) and '.dat' in f]
	#create csv with header
	header = ("Last name","First (real) name", "period", "github")
	with open('github.csv', 'w', newline='') as f:
		w = csv.writer(f, delimiter=',', quotechar='"')
		w.writerows(header)
	#for each .dat file
	for entry in files:
		#try to open and decode contents
		try:
			with open(entry, 'rb') as f:
				msg = f.read()
			stuff = decrypt(msg, private)
			if not stuff:
				raise Exception
			#split contents at comma
			temp = stuff.split(',')
			#strip leading and trailing spaces from all elements
			parts = []
			for i in temp:
				parts.append(i.strip())
			#github = filename -'.dat'
			parts.append(entry[:-4])
			#append (last, first, period, gh) to csv
			with open('github.csv','a',newline='') as f:
				w = csv.writer(f,delimiter=',',quotechar='"')
				w.writerows(parts)
		#catch unable to decode or open
		except IOError:
			print(f"Unable to open file {entry}.")
		except Exception:
			print(f"Unable to decrypt file {entry}.")
	print("--CSV created--")