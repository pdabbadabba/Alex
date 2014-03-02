#!/usr/bin/env python

import os


class Archive(object):
	
	sig_suffix = '.sig'
	
	@classmethod
	def from_sig_path(_cls, sig_file_path, node_name, node_path, sys):
		node_path = os.path.abspath(node_path)
		sig_file_path = os.path.abspath(sig_file_path)
		sys_root = os.path.join(node_path, sys.sys_sub_dir)
		file_path = os.path.join(node_path, sig_file_path[len(sys_root):].lstrip('/')).rstrip('.sig')
		return _cls(file_path, node_name, node_path, sys)
		 
	def __init__(_self, path, node_name, node_path, sys):
			_self.path = os.path.abspath(path)
			_self.node_path = os.path.abspath(node_path)
			_self.node_name = node_name
			_self.sys = sys
	
	@property
	def original_present(_self):
		return os.path.exists(_self.path)
	@property
	def sig_present(_self):
		return os.path.exists(_self.sig_file_path)
				
	@property
	def id(_self):
		return _self.sys.id_transform("%s@%s" % (_self.node_name, _self.node_relative_path))	
			
	@property
	def node_relative_path(_self):

		node_abspath = os.path.abspath(_self.node_path)

		assert _self.path.startswith(node_abspath)

		# The node-relative path is the portion of the absolute path to the 
		# archive that follows the absolute path to the node
		return _self.path[len(node_abspath):].lstrip('/')
		
		
	@property	
	def sys_path(_self):
		return os.path.join(_self.node_path, _self.sys.sys_sub_dir, _self.node_relative_path)
		
	@property
	def sig_file_path(_self):
		return _self.sys_path + _self.sig_suffix
		