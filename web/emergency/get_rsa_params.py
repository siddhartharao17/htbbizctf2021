# import library
from Crypto.PublicKey import RSA

fp = open("publickey.crt", "r")     # Open file in read-only mode
key = RSA.importKey(fp.read())
fp.close()

print("n:", key.n)      # print n and e values
print("e:", key.e)
