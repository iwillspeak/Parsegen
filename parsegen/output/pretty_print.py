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

from parsegen.output import register_context
from parsegen.output.callback import CallbackOutputContext

class PrettyPrintContext(CallbackOutputContext):
	"""Pretty Print Context
	
	Prints out a human readable representation of the computed grammar.
	"""
	
	def __init__(self, *args):
		CallbackOutputContext.__init__(self, *args)
		self.register_callback(self._output_symbol, CallbackOutputContext.MAIN)
	
	def _output_symbol(self, symbol, file):
		kind = "NULLABLE" if symbol.is_nullable() else "COMPULSORY"
		file.write("%s SYMBOL %s {\n" % (kind, symbol.name))
		for exp in symbol.expansions:
			predictions = self.predictions_for_expansion(exp)
			file.write("  {%s}\n" % ", ".join([s for s in predictions]))
			file.write("  ~> %s\n" % ", ".join(exp))
		file.write("}\n\n")

register_context("pretty_print", PrettyPrintContext)