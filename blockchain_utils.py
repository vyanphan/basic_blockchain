'''
A very, very naive blockchain.

Only used for demo purposes. 

Not provably secure. Meant to show that it works in the context of this project.
'''



import hashlib
import os
from stat import S_IREAD, S_IRGRP, S_IROTH
import binascii
import time

HASH_FN = hashlib.sha512
HASH_LENGTH = 512


def generate_random_seed(filename, num_bytes):
	''' Generates random seed for blockchain root. '''
	with open(filename, "wb") as file:
		file.write() # random starting hash
		file.write(os.urandom(num_bytes)) # random starting body
	os.chmod(filename, S_IROTH) # file is read-only


def format_update(update_file):
	''' Converts raw update file to a format for the blockchain. '''
	with open(update_file, "rb") as update_file:
		update_body = update_file.read()
	# do whatever formatting here
	return update_body # should be in byte format


class Block():
	'''
	Block information is formatted in this order.

	self.hash	=	hash of current block body and previous block hash
	self.prev	=	hash of previous block	
	self.body	=	body of update for current block

	other data
		self.proof	=	proof of work
		self.time	=	timestamp

	Everything must be string format.
	'''

	def __init__(self, prev, proof, body):
		self.proof = proof # verify_proof(proof, prev, body) == True
		self.prev = prev # must be string
		self.body = body # must be string
		try:
			self.hash =  HASH_FN(str.encode(prev) + str.encode(body)).hexdigest()
		except:
			print("All arguments should be passed as string format.")
		self.time = str(time.time())
		
		with open("records/" + block_hash.hexdigest(), "w+") as block_file:
			block_file.write(self.hash + '\n')
			block_file.write(self.prev + '\n')
			block_file.write(self.body + '\n')
			block_file.write(self.proof + '\n')
			block_file.write(self.time + '\n')

		return self.hash


class Chain():
	def __init__(self, chain_name, seed_length):
		if os.path.isfile(chain_name):
			print("Loading blockchain '" + chain_name + "'.")
			with open(chain_name, "r") as chain_header:
				self.tail = chain_header.readline()
		else:
			print("Blockchain '" + chain_name + "'' does not exist. Initializing new chain.")
			with open(chain_name, 'w+') as chain_header: 
				prev = os.urandom(HASH_LENGTH)
				body = os.urandom(seed_length)
				proof = os.urandom(seed_length)
				root_hash = Block(prev, proof, body)
				chain_header.write(root_hash)
			with open(chain_name, "r") as chain_header:
				self.tail = chain_header.readline()
	
	def verify_proof(prev, proof, body):
		curr_hash = HASH_FN(prev + body)
		# verification = some_function(proof, curr_hash) 
		#	e.g. hash(proof + curr_hash)[:6] == '000000'
		return True


	def append_block(self, proof, body):
		if verify_proof(, proof, body):
			new_block = Block(self.tail.hash, update_body)
			self.tail = new_block




# generate_random_seed('seedfile_test', 762)
blockchain_test = Chain('seedfile_test')
b1 = blockchain_test.tail.hash
print(b1)
blockchain_test.add_block('update1.txt')
print(blockchain_test.tail.prev == b1)
print(blockchain_test.tail.hash)

