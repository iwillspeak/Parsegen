# This file is part of Parsegen and is licensed as follows:
#
# Copyright (c) 2012 Will Speak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

class Struct(object):
	"""Struct
	
	Represents a read-only access to a dictionary through the . operator. Used
	to allow easy access to options and suchlike. Should be both Python 2.7 and
	3.x compatible.
	"""
	
	def __init__(self, *dicts, **kwargs):
		for d in dicts:
			self.__dict__.update(d)
		self.__dict__.update(kwargs)
	
	def __repr__(self):
		return repr(self.__dict__)
	
	def __contains__(self, item):
		return item in self.__dict__

	# Not hashable
	__hash__ = None
	
	def __cmp__(self, other):
		return self.__neq__(other)
	
	def __eq__(self, other):
		try:
			return self.__dict__ == other.__dict__
		except:
			return False
	
	def __neq__(self, other):
		return not self.__eq__(other)

# The following Lazy property decorator is licensed as 'cc-wiki'
# by Mike Boers (http://stackoverflow.com/users/66502/mike-boers)
# from http://stackoverflow.com/a/3013910/1353098 and is reproduced here
# under the terms of the origional license.
def lazyprop(fn):
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop
