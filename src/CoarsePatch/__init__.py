#!/usr/bin/env python

import struct
from base64 import b64encode
import itertools
import zlib
from collections import deque
from os import path
import gzip

KB = 1024
MB = 1000*KB

def rollingchecksum(removed, new, a, b, blocksize=4096):
    """
    Generates a new weak checksum when supplied with the internal state
    of the checksum calculation for the previous window, the removed
    byte, and the added byte.
    """
    a -= removed - new
    b -= removed * blocksize - a
    return (b << 16) | a, a, b


def weakchecksum(data):
    """
    Generates a weak checksum from an iterable set of bytes.
    """
    a = b = 0
    l = len(data)
    for i in range(l):
        a += data[i]
        b += (l - i)*data[i]

    return (b << 16) | a, a, b

def generate_sigs(file_name, block_size):
    sig_list = []
    sig = ''

    with open(file_name, 'rb') as file_bytes:
        position = 0
        for block in iter(lambda: file_bytes.read(block_size), ''):
            block_sig = zlib.adler32(block)
            sig_list.append([block_sig, len(block), block[:5], block[-5:], position])
            position += block_size

    data = {'blocks': sig_list, 'signature': zlib.adler32(str(sig_list))}
    return data

def find_matches(new_file_name, old_sigs, block_size):

    patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')

    new_bytes = ""

    with open(new_file_name, 'rb') as file_bytes, gzip.open(patch_file_name, 'wb') as patch_bytes:

        q  = file_bytes.read(block_size)

        for byte in iter(lambda: file_bytes.read(1), ''):

            match = False

            for sig, size, start, end, position in old_sigs:

                if ((start == q[:5]) and (end == q[-5:])) and zlib.adler32(q) == sig:

                    if len(new_bytes) > 0:
                        print >> patch_bytes, struct.pack('<ci%ds' % (len(new_bytes)), 'n', (len(new_bytes)), new_bytes)
                        new_bytes = ""

                    print >> patch_bytes, struct.pack('<cii', 's', position, block_size)
                    q = byte + file_bytes.read(block_size-1)
                    match = True

            if not match:
                new_bytes += q[:1]
                q = q[1:]
                q += byte

        new_bytes += q
        print >> patch_bytes, struct.pack('<ci%ds' % (len(new_bytes)), 'n', len(new_bytes), new_bytes)


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

    block_size = 1*KB

#    old_file_name = '../test/doc_v1.doc'
#    new_file_name = '../test/doc_v2.doc'

    old_file_name = '../test/txt_v1.txt'
    new_file_name = '../test/txt_v2.txt'
    patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')



    sigs = generate_sigs(old_file_name, block_size)
    find_matches(new_file_name, sigs['blocks'], block_size)

    patch(old_file_name, sigs, patch_file_name)
    print len(sigs['blocks'])










