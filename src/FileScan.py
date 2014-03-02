#!/usr/bin/env python

import os
import logging
from archive import Archive
from backend import Alpha as AlphaBackend
from functools import partial

def process_node(sys, nodes):

	map(lambda x: sys.touch_sys_dir(x[0]), nodes)
	map(partial(detect_deletions, sys), nodes.iteritems())
	map(partial(detect_modifications, sys), nodes.iteritems())

def detect_deletions(sys, (node_name, node_path)):
	map(partial(detect_deletions_in_dir, sys, node_name, node_path), sys.walk_sigs(node_path))

def detect_deletions_in_dir(sys, node_name, node_path, (dir, subdirs, files)):
	map(partial(detect_deleted_file, sys, node_name, node_path, dir), files)

def detect_deleted_file(sys, node_name, node_path, dir, filename):
	
	archive = Archive.from_sig_path(os.path.join(dir, filename), node_name, node_path, sys)
	
	if not archive.original_present:
		sys.delete_file(archive)
	else:
		pass

def detect_modifications(sys, (node_name, node_path)):
	map(partial(detect_modifications_in_dir, sys, node_name, node_path), sys.filtered_walk(node_path))

def detect_modifications_in_dir(sys, node_name, node_path, (dir, subdirs, files)):
	map (partial(detect_modified_file, sys, node_name, node_path, dir), files)
	
def detect_modified_file(sys, node_name, node_path, dir, filename):
	archive = Archive(os.path.join(dir, filename), node_name, node_path, sys)
	print archive.sig_file_path
	print archive.sig_present
	
	
		