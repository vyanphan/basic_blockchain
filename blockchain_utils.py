import hashlib
import os
from stat import S_IREAD, S_IRGRP, S_IROTH


def generate_random_seed(filename, num_bytes):
	''' Generates random seed for blockchain root. '''
	with open(filename, "wb") as file:
		file.write(os.urandom(512)) # random starting hash
		file.write(os.urandom(num_bytes)) # random starting body
	os.chmod(filename, S_IROTH) # file is read-only


def format_update(update_file):
	''' Converts raw update file to a format for the blockchain. '''
	with open(update_file, "rb") as update_file:
		update_body = update_file.read()
	# do whatever formatting here
	return update_body # should be in byte format


class Block():
	def __init__(self, prev, body):
		self.prev = prev # must be bytestring
		self.body = body # must be bytestring
		try:
			self.hash = hashlib.sha512(prev + body).digest()
		except:
			print("Previous block hash and block body must be formatted as bytes.")


class Chain():
	def __init__(self, seed_filename):
		with open(seed_filename, "rb") as seed_file:
			prev = seed_file.read(512)
			body = seed_file.read()
		self.root = Block(prev, body)
		self.tail = self.root

	def add_block(self, update_filename):
		update_body = format_update(update_filename)
		new_block = Block(self.tail.hash, update_body)
		self.tail = new_block





# generate_random_seed('seedfile_test', 762)
blockchain_test = Chain('seedfile_test')
b1 = blockchain_test.tail.hash
print(b1)
blockchain_test.add_block('update1.txt')
print(blockchain_test.tail.prev == b1)
print(blockchain_test.tail.hash)

