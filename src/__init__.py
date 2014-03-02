#!/usr/bin/env python

import os
import logging
from archive import Archive
from backend import Alpha as AlphaBackend
from functools import partial

sys_dir = '.alex'
sig_ext = ".sig"


def was_modified(patch_file_name, file_name):
    return true
    # Has the timestamp or filesize changed, compared to the records in the sig file?



def process_node(sys, (node_name, node_path)):

	sys.touch_sys_dir(node_path)
	detect_deletions(sys, node_name, node_path)
	#map(partial(process_dir, sys, node_name, node_path), sys.filtered_walk(node_path))

def detect_deletions(sys, node_name, node_path):
	
	map(partial(detect_deletions_in_dir, sys, node_name, node_path), sys.walk_sigs(node_path))

def detect_deletions_in_dir(sys, node_name, node_path, (dir, subdirs, files)):
	map(partial(detect_deleted_file, sys, node_name, node_path, dir), files)

def detect_deleted_file(sys, node_name, node_path, dir, filename):

	archive = Archive.from_sig_path(os.path.join(dir, filename), node_name, node_path, sys)
	if not archive.original_present:
		sys.delete_file(archive)
	
def process_dir(sys, node_name, node_path, (dir, subdirs, files)):
	
	map(partial(process_file, sys, node_name, node_path, dir), files)
	
def process_file(sys, node_name, node_path, dir, file):	
	a = Archive(os.path.join(dir, file), node_name, node_path, sys)

	
if __name__ == '__main__':
	
	
	
	nodes = {'test': '/Users/Paul/Documents/Projects/Alex/test/'}
	sys = AlphaBackend.Alpha()
	
	
	map(partial(process_node, sys), nodes.iteritems())
	
	#for node_name, node_path in nodes.items():
	#
	#


	#	for sub_dir, dirs, files in sys.filtered_walk(node_path):
	#		for file in files:
	#			a = Archive(os.path.join(sub_dir, file), node_name, node_path, sys)
	#			print a.id
	#			print a.sys_path
				
	
	pass



def __something__():

	
	for rootdir in map(os.path.abspath,dirs):

        
        # Look for deleted files (i.e., sig files with no matching working files)
		for subdir, dirs, files in os.walk(os.path.join(rootdir, sys_dir)):
			working_subdir = os.path.join(rootdir, subdir[len(os.path.join(rootdir, sys_dir))+1:])
			for sig_file in files:
				working_file = sig_file[:-len(sig_ext)]
				if (
                    sig_file.endswith(sig_ext)
                    and not os.path.exists(os.path.join(working_subdir, working_file))
                    ):
					print "%s was deleted!?" % working_file
        
		l = lambda(x,y,z): not x.startswith(os.path.join(rootdir, sys_dir))
        
        # TODO: filter sys_dir
		for subdir, dirs, files in filter(l, os.walk(rootdir)):
            
			sys_subdir = os.path.join(rootdir, sys_dir, subdir[len(rootdir)+1:])
            
			try:
				if not os.path.exists(sys_subdir):
					os.makedirs(sys_subdir)
			except:
				logging.critical("Error accessing or creating system directory '%s'." % sys_subdir)
				break
            
			for sig_file in files:
				sig_file_path = os.path.join(sys_subdir, sig_file)
                
				if  os.path.exists(sig_file_path):
					pass
				else:
					pass
                # Does a corresponding sig file exist?
                #     If not, this is a new file.
                #     If so, was file modified?
                #         If not, do nothing
                #         If so, generate a patch
                #         Upload patch
                #         Generate new sigs
                #         Overwrite old sig with the new one








