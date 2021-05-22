#!/usr/bin/env python
import re
import sys

import pytest
from _pytest.unittest import TestCaseFunction
from coverage import Coverage
from coverage.data import add_data_to_hash
from coverage.misc import Hasher

tests = dict()

class FindDuplicateCoverage:

    def __init__(self):
        self.collected = []
        self.name = None
        self.cov = None
        self.hash = None

    def pytest_collection_modifyitems(self, items):
        for item in items:
            if isinstance(item, TestCaseFunction):
                self.collected.append(item.name)

    def pytest_runtest_logstart(self, nodeid, location):
        #print(f"\nStart test {nodeid}")
        try:
            self.name = re.sub(r'^[^/]+/', '', nodeid)
            self.cov = Coverage(branch=True)
            self.hash = Hasher()
            self.cov.start()
        except:
            self.cov = None

    def pytest_runtest_logfinish(self, nodeid, location):
        if self.cov:
            try:
                self.cov.stop()
                #print(f"\nStop test {nodeid}")
                data = self.cov.get_data()
                for f in data.measured_files():
                    # print(f)
                    # print(data.arcs(f))
                    add_data_to_hash(data, f, self.hash)
                text_hash = self.hash.hexdigest()

                #print(text_hash)
                if text_hash in tests:
                    tests[text_hash] += [self.name]
                else:
                    tests[text_hash] = [self.name]

                self.cov.erase()
            except Exception as ex:
                print("Exception %s", str(ex.args()))

            self.name = None
            self.cov = None
            self.hash = None


my_plugin = FindDuplicateCoverage()
# directory = '.'
pytest.main(sys.argv[1:], plugins=[my_plugin])

print("\n\nDuplicates:")
for k, v in tests.items():
    if len(v) > 1:
        for i in sorted(v):
            print(i)
        print('\n')
