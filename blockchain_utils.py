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
		
		with open("records/" + self.hash, "w+") as block_file:
			block_file.write(self.hash + '\n')
			block_file.write(self.prev + '\n')
			block_file.write(self.body + '\n')
			block_file.write(self.proof + '\n')
			block_file.write(self.time + '\n')



class Chain():
	'''
	chain_header stores the tail, aka the hash of the most recently appended block.

	self.name = name of the chain
	self.tail = hash of most recently appended block
	'''

	def __init__(self, chain_name, seed_length):
		self.name = chain_name
		if os.path.isfile(chain_name):
			print("Loading blockchain '" + chain_name + "'.")
			with open(chain_name, "r") as chain_header:
				self.tail = chain_header.readline()
		else:
			print("Blockchain '" + chain_name + "'' does not exist. Initializing new chain.")
			with open(chain_name, 'w+') as chain_header: 
				prev = os.urandom(HASH_LENGTH).hex()
				body = os.urandom(seed_length).hex()
				proof = os.urandom(seed_length).hex()
				
				root_block = Block(prev, proof, body)
				chain_header.write(root_block.hash)
			with open(chain_name, "r") as chain_header:
				self.tail = chain_header.readline()
	
	def verify_proof(self, prev, proof, body):
		curr_hash = HASH_FN(str.encode(prev) + str.encode(body))
		# verification = some_function(proof, curr_hash) 
		#	e.g. hash(proof + curr_hash)[:6] == '000000'
		return True


	def append_block(self, prev, proof, body):
		if self.verify_proof(prev, proof, body):
			new_block = Block(prev, proof, body)
			with open(self.name, 'w') as chain_header:
				chain_header.write(new_block.hash)
				self.tail = new_block.hash 
			print("Successfully appended update " + new_block.hash)




test_chain = Chain('test_chain', 720)
# test_chain.append_block(test_chain.tail, 'blablah', 'hello world')
# test_chain.append_block(test_chain.tail, 'gdi', 'goodbye world')
# test_chain.append_block(test_chain.tail, 'deadbeef', 'i made steak')
test_chain.append_block(test_chain.tail, 'proof 4', 'update 4')
test_chain.append_block(test_chain.tail, 'proof 5', 'update 5')





