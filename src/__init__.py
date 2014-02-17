#!/usr/bin/env python

import os
import logging

sys_dir = '.alex'



def was_modified(patch_file_name, file_name):
    return true
    # Has the timestamp or filesize changed, compared to the records in the sig file?


if __name__ == '__main__':
    dirs = ['../test']
    for rootdir in map(os.path.abspath,dirs):
        for subdir, dirs, files in os.walk(rootdir):

            sys_subdir = os.path.join(rootdir, sys_dir, subdir[len(rootdir)+1:])

            try:
                if not os.path.exists(sys_subdir):
                    os.makedirs(sys_subdir)
            except:
                logging.critical("Error accessing or creating system directory '%s'." % sys_subdir)
                break

            # Does a corresponding sig file exist?
            #     If not, this is a new file.
            #     If so, was file modified?
            #         If not, do nothing
            #         If so, generate a patch
            #         Upload patch
            #         Generate new sigs
            #         Overwrite old sig with the new one








