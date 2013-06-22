from distutils.core import setup
import parsegen.version
setup(
	# Metadata
	name = 'parsegen',
	version = parsegen.version.VERSION,
	author = 'Will Speak (@willspeak)',
	author_email = 'parsegen@willspeak.me',
	maintainer = 'Will Speak',
	maintainer_email = 'parsegen@willspeak.me',
	url = 'http://github.com/iwillspeak/Parsegen',
	description = 'LL(1) Parser Generator',
	long_description = """
	Parsegen is an automatic parser generator for C. It reads in definitions in
	a dialect of BNF and creates a top-down parser with one-symbol lookahead.

	In theory Parsegen can generate parsers for LL(1) grammars.
	""",
	classifiers = [
		"Programming Language :: Python :: 3",
		"Programming Language :: Python",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	# Things to Distribute
	packages = ['test', 'parsegen', 'parsegen.output'],
	package_data = {'parsegen.output': ['*.mustache']},
	scripts = ['bin/parsegen']
)
