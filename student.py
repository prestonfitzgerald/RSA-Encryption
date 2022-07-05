import os
#import or install dependencies
try:
	import rsa
except:
	print("RSA module needed -- installing")
	os.system("pip install rsa")
	import rsa
	
#prompt for student information
real = ""
valid = False
while not valid:
	try:
		period = int(input("What class period is this?\n"))
		if period not in range(1,9):
			raise Exception
		valid = True
	except ValueError:
		print("That wasn't a number.")
	except Exception:
		print("That wasn't a valid period number.")
first = input("What is your legal first name?\n").title()
val = 'a'
while val not in ('yes','y','n','no',''):
	val = input("Do you have a preferred name(Y/n)?\n").lower()
if val in ('y','yes'):
	real = first
	first = input("What is your preferred first name?\n").title()
last = input("What is your last name?\n").title()
gh = input("What is your GitHub username (capitalization matters)?\n")
#Format string for encoding
stuff = f"{last}, {first}"
if real:
	stuff += f" ({real})"
stuff += f", {period}"
#load Simonsen's public key
print(f"Encoding {stuff} into {gh}.dat")
with open("Simonsen_public.pen", 'rb') as f:
	key = rsa.PublicKey.load_pkcs1(f.read())
crypt = rsa.encrypt(stuff.encode('ascii'), key)
with open(f"{gh}.dat",'wb') as f:
	f.write(crypt)
print("Encoding Complete")