from html5lib import *
from blockchain_utils import *
import os



def append_update(blockchain, proof, update_file, private_mode):
    with open(update_file, "r") as rd_file:
        update_block = rd_file.read()
        if private_mode:
            salt = os.urandom(seed_length).hex()
            update_block = salt + ' ' + HASH_FN(salt + update_block)
        blockchain.append_block(proof, blockchain.tail, update_block)


def parse_chain(chain_folder, chain_head):
    if chain_folder[-1] != '/':
        chain_folder += '/'

    curr_block = chain_folder + chain_head

    with open(curr_block, "r") as ch_file:
        curr_block = ch_file.read()
        next_block = chain_folder + curr_block

    blocks = []

    while os.path.isfile(next_block):
        with open(next_block) as block_file:
            b1 = block_file.readline()
            b2 = block_file.readline()
            next_block = block_file.readline()[:-1]
            b3 = block_file.readline()
            b4 = block_file.readline()
        curr_block = b1 + b2 + next_block + "\n" + b3 + b4
        blocks += [curr_block]
        next_block = chain_folder + next_block
    return blocks

def display(chain_folder, chain_head):
    blocks = parse_chain(chain_folder, chain_head)

    for b in blocks:
        print(b)



display('newchain_1', 'newchain_1')

