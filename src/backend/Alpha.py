#!/usr/bin/env python

import re
import os
import logging

class Alpha(object):
	
	
	
	sys_sub_dir = '.rcg_bak'
	
	exclude_patterns = ['.*\.rcg_bak.*',]
	
	def __init__(_cls):
		pass
		
	def id_transform(_self, archive_id):
		return archive_id
		
	def get_node_sys_dir(_self, node_path):
		return os.path.join(node_path, _self.sys_sub_dir)
		
	def touch_sys_dir(_self, node_path):
		sys_dir_path = _self.get_node_sys_dir(node_path)
		
		try:
			if not os.path.exists(sys_dir_path):
				os.makedirs(sys_dir_path)
		except:
			logging.critical("Error accessing or creating system directory '%s'." % sys_dir_path)
	def delete_file(_self, archive):
		print "I definitely have just reported '%s' as deleted. Really." % archive.id
	
	def walk_sigs(_self, node_path):
		
		sys_dir_path = _self.get_node_sys_dir(node_path)
		
		for dir_, dirnames, filenames in os.walk(sys_dir_path):
	
				yield dir_, dirnames, filter(lambda x: re.match('^.*\.sig$', x), filenames)
		
		
	def filtered_walk(_self, path):
		
		# Combine exclusion patterns into a single regex
		regex = "(" + ")|(".join(_self.exclude_patterns) + ")"
		
		for dir_, dirnames, filenames in os.walk(path):
			if not re.match(regex, dir_):
				filtered_dirnames = filter(lambda x: not re.match(regex, x), dirnames)
				filtered_filenames = filter(lambda x: not re.match(regex, x), filenames)
				yield dir_, filtered_dirnames, filtered_filenames
		