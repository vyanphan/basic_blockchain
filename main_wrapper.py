from html5lib import *
from blockchain_utils import *
import os

TABLE_LABELS = ['Proof', 'Next Block', 'Update Body', 'Time']

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
        curr_block = (b1, b2, next_block + "\n", b3, b4)
        blocks += [curr_block]
        next_block = chain_folder + next_block
    return blocks

def display(output_file, chain_folder, chain_head):
    blocks = parse_chain(chain_folder, chain_head)

    with open(output_file, 'w+') as out_file:
        out_file.write('<html><head><title>' + chain_folder + '</title>')
        out_file.write('<link rel="stylesheet" href="format.css"></head>')
        out_file.write('<body><h1 align="center">' + chain_folder + '</h1>')

        for b in blocks:
            out_file.write('<table>')
            out_file.write('<tr><th colspan=2>' + b[0] + '</th></tr> <col width="20%"/><col width="80%"/>')
            for i in range(0,4):    
                out_file.write('<tr><td><b>' + TABLE_LABELS[i] + '</b></td><td>' + b[i+1] + '</td>')
            out_file.write('</table>')
            out_file.write('<br>')

        out_file.write('</body></html>')



display('newchain_1.html', 'newchain_1', 'newchain_1')

