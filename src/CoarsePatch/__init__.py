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
import sys

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

    removed = removed
    new = new

    a -= removed - new
    b -= removed * blocksize - a

    return (b << 16) | a, a, b



def weakchecksum(data):

    a = b = i = 0
    l = len(data)

    for d in data:
        a += d
        b += (l - i) * d
        i += 1

    return (b << 16) | a, a, b

def read_sigs(file_name):
    print "------------------------"
    sigs = defaultdict(dict)

    with gzip.open(file_name, 'rb') as sig_bytes:

        for weak_checksum_bytes in iter(lambda: sig_bytes.read(struct.calcsize('<qh')), ""):

            weak_checksum,num_sigs = struct.unpack('<qh', weak_checksum_bytes)

            sigs[weak_checksum] = {}
            for i in range(num_sigs):

                sig_hash, position, size = struct.unpack('<32sii', sig_bytes.read(struct.calcsize('<32sii')))
                sigs[weak_checksum][sig_hash] = [position, size]





    return sigs

def write_sigs(sigs, file_name):
    with gzip.open(file_name, 'wb') as sig_bytes:

        # For each weah checksum group
        for weak_checksum in sigs:

            # Write checksum

            sig_bytes.write(struct.pack('<qh', weak_checksum, len(sigs[weak_checksum])))

            # Write length of matches with this weak checksum
            # hash + size + position

            for sig_hash in sigs[weak_checksum]:

                sig_bytes.write(struct.pack('<32sii', sig_hash, sigs[weak_checksum][sig_hash][0], sigs[weak_checksum][sig_hash][1]))



def generate_sigs(file_name, block_size):
    sig_dict = defaultdict(dict)

    with open(file_name, 'rb') as file_bytes:

        position = 0

        for block in iter(lambda: file_bytes.read(block_size), ''):

            c, a,b = weakchecksum(bytes(block))

            sig_dict[c][HASH(block).hexdigest()] = [position, len(block)]
            position += block_size


    return sig_dict

def find_matches(new_file_name, old_sigs, block_size):

    patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')

    new_bytes = []

    with open(new_file_name, 'rb') as file_bytes, gzip.open(patch_file_name, 'wb') as patch_bytes:

        q  = deque(file_bytes.read(block_size))
        c,a,b = weakchecksum(bytes(q))

        for byte in iter(lambda: file_bytes.read(1), ''):


            # Check for matching block
            sig_hash = None
            match = None
            weak_match = None
            weak_match = old_sigs.get(c)
            if weak_match:
                match_hash = HASH(''.join(q)).hexdigest()
                match = weak_match.get(match_hash)
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
                c,a,b = weakchecksum(bytes(q))


            else:

                # roll the window
                old_byte = q.popleft()
                q.append(byte)

                # add old byte to bytes to be written
                new_bytes.append(old_byte)

                # roll the checksum
                c,a,b = rollingchecksum(ord(old_byte), ord(byte), a, b, block_size)

        # write trailing, unmatched data
        if len(new_bytes) > 0 or len(q) > 0:
            new_bytes_str = "".join([''.join(new_bytes), ''.join(q)])
            print >> patch_bytes, struct.pack('<ci%ds' % (len(new_bytes_str)), 'n', len(new_bytes_str), new_bytes_str)


def patch(original_file_name, patch_file_name, out_file_name):

    with open(original_file_name, 'rb') as original_bytes, gzip.open(patch_file_name, 'rb') as patch_bytes, open(out_file_name, 'wb') as out_bytes:

        for data_type_bytes in iter(lambda: patch_bytes.read(struct.calcsize('<c')), ""):

            data_type = struct.unpack('<c', data_type_bytes)[0]

            if data_type == 's':

                position, size = struct.unpack('<ii', patch_bytes.read(struct.calcsize('<ii')))
                original_bytes.seek(position)
                out_bytes.write(original_bytes.read(size))

            elif data_type == 'n':
                length = struct.unpack('<i', patch_bytes.read(struct.calcsize('<i')))[0]
                data = struct.unpack('<%ds' % length, patch_bytes.read(struct.calcsize('<%ds' % length)))[0]
                out_bytes.write(data)

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


def GO():

    block_size = 1 * KB
    pp = pprint.PrettyPrinter(depth=6)

#    old_file_name = '../test/doc_v1.doc'
#    new_file_name = '../test/doc_v2.doc'


    old_file_name = '../test/v1.doc'
    new_file_name = '../test/v2.doc'

    sig_file_name = path.join(path.split(old_file_name)[0],path.split(old_file_name)[1] + '.sig')
    patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')

    sigs = generate_sigs(old_file_name, block_size)
    write_sigs(sigs, sig_file_name)
    print read_sigs(sig_file_name)
    #find_matches(new_file_name, sigs, block_size)

    #old_file_name = '../test/v1.crypt'
    #new_file_name = '../test/v2.crypt'
    #patch_file_name = path.join(path.split(new_file_name)[0],path.split(new_file_name)[1] + '.patch')
    #sigs = generate_sigs(old_file_name, block_size)
    #find_matches(new_file_name, sigs, block_size)

    #patch(old_file_name, patch_file_name, '../test/v2.out.doc')
    #print len(sigs['blocks'])



if __name__=='__main__':
    import cProfile
    #cProfile.run('GO()', sort='time')
    GO()







