import os
try:
	import rsa
except:
	print("RSA module neede -- installing")
	os.system("pip install rsa")
	import rsa
finally:
	print("complete")

def generate_keys():
	public, private = rsa.newkeys(1024)
	with open("public.pen", 'wb') as f:
		f.write(public.save_pkcs1('PEM'))
	with open("private.pen", 'wb') as f:
		f.write(private.save_pkcs1('PEM'))
	
def load_keys():
	with open("public.pen", 'rb') as f:
		public = rsa.PublicKey.load_pkcs1(f.read())
	with open("private.pen", 'rb') as f:
		private = rsa.PrivateKey.load_pkcs1(f.read())
	return public, private

def encrypt(msg, key):
	return rsa.encrypt(msg.encode('ascii'), key)

def decrypt(msg, key):
	try:
		return rsa.decrypt(msg, key).decode('ascii')
	except:
		return False

def sign_sha1(msg, key):
	return rsa.sign(msg.encode('ascii'), key, 'SHA-1')

def verify_sha1(msg, sign, key):
	try:
		return rsa.verify(msg.encode('ascii'), sign, key) == 'SHA-1'
	except:
		return False

generate_keys()
public, private = load_keys()
message = input("Enter a message: ")
ciphertext = encrypt(message, public)
signature = sign_sha1(message, private)

print(ciphertext)
print("-"*10)
print(signature)
