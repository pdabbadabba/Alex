#!/usr/bin/env python

import struct
from base64 import b64encode
import itertools
import zlib
from collections import deque, defaultdict
from os import path
import gzip
from hashlib import md5 as HASH
import pprint

KB = 1024
MB = 1000*KB

if not(hasattr(__builtins__, "bytes")) or str is bytes:
    # Python 2.x compatibility
    def bytes(var, *args):
        try:
            return ''.join(map(chr, var))
        except TypeError:
            return map(ord, var)

def rollingchecksum(removed, new, a, b, blocksize=4096):

    removed = ord(removed)
    new = ord(new)

    a -= removed - new
    b -= removed * blocksize - a
    return (b << 16) | a, a, b


def weakchecksum(data):

    data = bytes(data)

    a = b = 0
    l = len(data)
    for i in range(l):
        a += data[i]
        b += (l - i)*data[i]

    return (b << 16) | a, a, b

def generate_sigs(file_name, block_size):
    sig_dict = defaultdict(dict)

    with open(file_name, 'rb') as file_bytes:

        position = 0

        for block in iter(lambda: file_bytes.read(block_size), ''):

            c, a,b = weakchecksum(block)

            sig_dict[c][HASH(block).hexdigest()] = [position, len(block)]
            position += block_size


    return sig_dict

def find_matches(new_file_name, old_sigs, block_size):

    patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')

    new_bytes = []

    with open(new_file_name, 'rb') as file_bytes, gzip.open(patch_file_name, 'wb') as patch_bytes:

        q  = deque(file_bytes.read(block_size))
        c,a,b = weakchecksum(q)

        for byte in iter(lambda: file_bytes.read(1), ''):


            # Check for matching block
            sig_hash = None
            match = None
            weak_match = None
            weak_match = old_sigs.get(c)
            if weak_match:

                match = weak_match.get(HASH(''.join(q)).hexdigest())
                #print weak_match[HASH(''.join(q)).hexdigest()]
                #print weak_match[HASH(''.join(q)).hexdigest()]

            # If there is a match...
            if match:

                # If we had accumulated new data, write it out
                if len(new_bytes) > 0:
                    new_bytes_str = "".join(new_bytes)
                    print >> patch_bytes, struct.pack('<ci%ds' % (len(new_bytes_str)), 'n', (len(new_bytes_str)), new_bytes_str)
                    new_bytes = []

                print >> patch_bytes, struct.pack('<cii', 's', match[0], match[1])

                # refill the queue
                q=deque(byte + file_bytes.read(block_size-1))
                c,a,b = weakchecksum(q)


            else:

                # roll the window
                old_byte = q.popleft()
                q.append(byte)

                # add old byte to bytes to be written
                new_bytes.append(old_byte)

                # roll the checksum
                c,a,b = rollingchecksum(old_byte, byte, a, b, block_size)

        # write trailing, unmatched data
        if len(new_bytes) > 0 or len(q) > 0:
            new_bytes_str = "".join([''.join(new_bytes), ''.join(q)])
            print >> patch_bytes, struct.pack('<ci%ds' % (len(new_bytes_str)), 'n', len(new_bytes_str), new_bytes_str)


def patch(old_file_name, sigs, patch_file_name):

    patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')
    out_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.out')

    #with open(old_file_name, 'rb') as old_bytes, gzip.open(patch_file_name, 'rb') as patch_bytes, open(out_file_name, 'wb') as out_bytes:
    with gzip.open(patch_file_name, 'rb') as patch_bytes:

        for data_type_bytes in iter(lambda: patch_bytes.read(struct.calcsize('<c')), ""):

            print '---'

            data_type = struct.unpack('<c', data_type_bytes)[0]
            print data_type

            if data_type == 's':
                position, size = struct.unpack('<ii', patch_bytes.read(struct.calcsize('<ii')))
                print position
                print size
            elif data_type == 'n':
                length = struct.unpack('<i', patch_bytes.read(struct.calcsize('<i')))[0]
                data = struct.unpack('<%ds' % length, patch_bytes.read(struct.calcsize('<%ds' % length)))[0]
                print data


            patch_bytes.read(struct.calcsize('<c'))

        # If signature
        # ... lookup signature's position in old
        # ... seek to that position
        # ... read one block
        # ... write block to out_bytes
        # Else
        # ... read line
        # ... strip newline
        # ... write line to out_bytes



if __name__=='__main__':

    block_size = 1 * KB
    pp = pprint.PrettyPrinter(depth=6)

#    old_file_name = '../test/doc_v1.doc'
#    new_file_name = '../test/doc_v2.doc'

    old_file_name = '../test/doc_v1.doc'
    new_file_name = '../test/doc_v2.doc'
    patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')
    sigs = generate_sigs(old_file_name, block_size)
    find_matches(new_file_name, sigs, block_size)

    old_file_name = '../test/doc_v1.doc'
    new_file_name = '../test/doc_v2.doc'
    patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')
    sigs = generate_sigs(old_file_name, block_size)
    find_matches(new_file_name, sigs, block_size)

    old_file_name = '../test/v1.html'
    new_file_name = '../test/v2.html'
    patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')
    sigs = generate_sigs(old_file_name, block_size)
    find_matches(new_file_name, sigs, block_size)

    old_file_name = '../test/v1.crypt'
    new_file_name = '../test/v2.crypt'
    patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')
    sigs = generate_sigs(old_file_name, block_size)
    find_matches(new_file_name, sigs, block_size)

    #patch(old_file_name, sigs, patch_file_name)
    #print len(sigs['blocks'])










