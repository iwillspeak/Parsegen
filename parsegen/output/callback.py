
from parsegen.output import OutputContext

class CallbackOutputContext(OutputContext):
	"""Callback Output Context
	
	Output context that uses callbacks to write things to a stream. This is
	intended for implementing output contexts where the logic for the context
	is better expressed in python.
	"""
	
	PRE, MAIN, POST = range(3)
	
	def __init__(self, *args):
		OutputContext.__init__(self, *args)
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