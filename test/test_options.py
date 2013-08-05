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

# Test helpers
from nose.tools import *
from tempfile import TemporaryFile, NamedTemporaryFile

# Module to test
from parsegen.options import *

def wrapped(function):
    def __return(*args, **kwargs):
        esave = sys.stderr
        osave = sys.stdout

        osave.flush()
        esave.flush()

        T = TemporaryFile
        try:
            with T(mode="w") as sys.stdout, T(mode="w") as sys.stderr:
                function(*args, **kwargs)
        finally:
            sys.stdout = osave
            sys.stderr = esave

    return __return

class TestOptions(object):
    
    def setup(self):
        pass

    def teardown(self):
        pass

    def test_options(self):

        assert_raises(SystemExit, wrapped(lambda : parse([])))

        with NamedTemporaryFile() as f:
            assert parse([f.name])

        with NamedTemporaryFile() as f:
            opts = parse([f.name, 'foo=bar', 'bar=baz'])
            assert opts
            assert opts.options['foo'] == 'bar'
            assert opts.options['bar'] == 'baz'
            assert opts.output_file == sys.stdout
            assert opts.input_file.name == f.name
            opts.input_file.close()
