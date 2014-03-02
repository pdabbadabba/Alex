#!/usr/bin/env python

import os
import logging
from archive import Archive
from backend import Alpha as AlphaBackend
from functools import partial
import FileScan
	
if __name__ == '__main__':
	
	nodes = {'test': '/Users/Paul/Documents/Projects/Alex/test/'}
	sys = AlphaBackend.Alpha()
	print nodes
	FileScan.process_node(sys, nodes)
	











