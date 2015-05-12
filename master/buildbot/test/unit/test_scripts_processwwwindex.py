# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members


import tempfile

from twisted.trial import unittest

from buildbot.util import json
from buildbot.scripts import processwwwindex


class TestUsersClient(unittest.TestCase):

    def setUp(self):
        # un-do the effects of @in_reactor
        self.patch(processwwwindex, 'processwwwindex', processwwwindex.processwwwindex._orig)

    def test_no_input_file(self):
        d = processwwwindex.processwwwindex({})

        def check(ret):
            self.assertEqual(ret, 1)
        d.addCallback(check)
        return d

    def test_invalid_input_file(self):
        d = processwwwindex.processwwwindex({'index-file': '/some/no/where'})

        def check(ret):
            self.assertEqual(ret, 2)
        d.addCallback(check)
        return d

    def test_output_config(self):
        tmpf = tempfile.NamedTemporaryFile(suffix=".html")
        with open(tmpf.name, 'w') as f:
            f.write('{{ configjson|safe }}')

        d = processwwwindex.processwwwindex({'index-file': tmpf.name})

        def check(ret):
            self.assertEqual(ret, 0)
            with open(tmpf.name) as f:
                config = json.loads(f.read())
                self.assertTrue(isinstance(config, dict))

        d.addCallback(check)
        return d