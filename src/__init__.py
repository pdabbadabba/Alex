#!/usr/bin/env python

import os
import logging
from CoarsePatch import read_sigs

sys_dir_name = '.alex'
sig_suffix = ".sig"
patch_suffix = ".patch"



def was_modified(patch_file_name, file_name):
    return true
    # Has the timestamp or filesize changed, compared to the records in the sig file?


if __name__ == '__main__':
    dirs = ['../test']
    for rootdir in map(os.path.abspath,dirs):

        sys_dir = os.path.join(rootdir, sys_dir_name)

        for subdir, dirs, files in filter(lambda x: not x[0].startswith(os.path.abspath(sys_dir)), os.walk(rootdir)):

            sys_subdir = os.path.join(rootdir, sys_dir_name, subdir[len(rootdir)+1:])

            try:
                if not os.path.exists(sys_subdir):
                    os.makedirs(sys_subdir)
            except:
                logging.critical("Error accessing or creating system directory '%s'." % sys_subdir)
                break

            for file_name in files:

                sig_file_name = os.path.join(sys_subdir, file_name)

                if not os.path.exists(sig_file_name):
                    pass
                    # TODO: actually upload the file, etc.

                else:
                    pass
                    sigs = read_sig_attributes(sig_file_name)




                # Does a corresponding sig file exist?
                #
                #     If not, this is a new file.
                #         Create new file backup
                #
                #     If so, was the file modified?
                #         If not, do nothing
                #         If so, generate a patch
                #         Upload patch
                # Generate new sigs
                # Write new sig to disk








