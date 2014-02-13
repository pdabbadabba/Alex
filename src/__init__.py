#!/usr/bin/env python

import hashlib
import os
import shelve

db_filename = '.alex_db'

KB = 1024
MB = 1000*KB
block_size = 1 * MB
upload_buffer = 5 * MB

bk_dirs = ['../test/']

def mkdir(directory):
    path = os.path.join(dir_prefix)
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == '__main__':

    # Check for db

    for bk_dir in bk_dirs:

        db = shelve.open(os.path.join(bk_dir, db_filename), 'c')
        print db
        for root, dirs, files in os.walk(bk_dir):
            for this_filename in files:
                this_file = os.path.join(root, this_filename)

                # Write block digests to db
                with open(this_file, 'rb') as file_bytes:
                    digest_list = []
                    digest = ''
                    for chunk in iter(lambda: file_bytes.read(block_size), ''):
                        chunk_digest = hashlib.sha1(chunk).hexdigest()
                        digest_list.append([chunk_digest, len(chunk)])
                        digest = hashlib.sha1(digest + chunk_digest).hexdigest()

                    db[str(this_file)] = {
                                          'stage':
                                          {'blocks': digest_list,
                                           'signature': digest}
                                          }
#                    db[str(this_file)]['stage'] = {}
                    #db[str(this_file)]['stage']['blocks'] = digest_list
                    #db[str(this_file)]['stage']['signature'] = digest


        db.close()



        #for root, dirs, files in os.walk(bk_dir):
        #    for f in files:


   #             staging_dir = os.path.join(root, staging_dir)
   #
   #             if not os.path.exists(staging_dir)
   #                 os.makedirs(staging_dir)
   #
   #
   #             this_file = os.path.join(root, f)
   #             staging_file = os.path.join(root, staging_dir, f)
   #             print staging_file
   #             print os.path.abspath(staging_file)


                #print os.path.join(staging_path, this_file)
        #        with open(this_file, 'rb') as f_bytes:
        #            with open()
        #            for chunk in iter(lambda: f.read(block_size), ''):
        #            chunk_digest = hashlib.sha1(chunk).hexdigest()
        #            digest = hashlib.sha1(digest + chunk_digest).hexdigest()
        ##            print chunk_digest
        #
        #
        #        print '-----------------------'
        #        print digest




