#!/usr/bin/env python3
import sys
from testrunner import TestRunner

runner = TestRunner([1,2,3,4,5])
runner.discover()
runner.add_checker_tests(3, 'tests/outputs/03/checker.py')
res = runner.run_all_tests()

if not all(res.values()):
    sys.exit(1)
sys.exit(0)

