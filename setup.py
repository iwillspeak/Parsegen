from distutils.core import setup
import parsegen.version
setup(
    name = 'parsegen',
    packages = ['test', 'parsegen'],
	scripts = ['bin/parsegen'],
    version = parsegen.version.VERSION,
    description = 'LL(1) Parser Generator',
    author = 'Will Speak (@willspeak)',
    author_email = 'parsegen@willspeak.me',
    url = 'http://github.com/iwillspeak/Parsegen',
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
