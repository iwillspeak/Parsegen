# This file is part of Parsegen and is licensed as follows:
#
# Copyright (c) 2013 Will Speak
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

from parsegen.output import OutputFormatter

class CallbackOutputFormatter(OutputFormatter):
	"""Callback Output Formatter
	
	Output formatter that uses callbacks to write things to a stream. This is
	intended for implementing output formatters where the logic for the formatter
	is better expressed in python.
	"""
	
	PRE, MAIN, POST = range(3)
	
	def __init__(self, *args):
		OutputFormatter.__init__(self, *args)
		self.callbacks = {
			self.PRE : [],
			self.MAIN : [],
			self.POST : []
		}
		
	def write(self, file):
		"""Write
		
		Calls the methods that have been registered for each stage to write the
		output to the file.
		"""
		
		for callback in self.callbacks[self.PRE]:
			callback(file)
		
		for callback in self.callbacks[self.MAIN]:
			for symbol in self.grammar.expansions.values():
				callback(symbol, file)
		
		for callback in self.callbacks[self.POST]:
			callback(file)
	
	def register_callback(self, callback, stage=MAIN):
		
		if not stage in [self.MAIN, self.PRE, self.POST]:
			raise ArgumentError("unknown callback stage '%s'" % stage)
		
		self.callbacks[stage].append(callback)
