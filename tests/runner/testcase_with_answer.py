import os
import subprocess
import glob
import sys
from typing import List, Optional, Callable
from pathlib import Path

from testcase import TestCase, normalize

class TestCaseWithAnswer(TestCase):
    """Test case with expected answer file"""
    
    def __init__(self, test_file: str, answer_file: str, test_name: str = ""):
        super().__init__(test_file, test_name)
        self.answer_file = answer_file
        self.expected_output: Optional[List[str]] = None
        self._load_expected_output()
    
    def _load_expected_output(self) -> None:
        """Load expected output from answer file"""
        try:
            with open(self.answer_file, 'r', encoding='utf-8') as f:
                self.expected_output = normalize(f.read().split('\n'))
        except Exception as e:
            raise RuntimeError(f"Failed to load expected output from {self.answer_file}: {str(e)}")
    
    def validate(self) -> bool:
        """Validate user output against expected output"""
        if self.user_output is None:
            print(f"[ERR] {self.test_name} No program output to validate", file=sys.stderr)
            return False
        
        if self.expected_output is None:
            print(f"[ERR] {self.test_name} No expected output loaded", file=sys.stderr)
            return False
        
        if len(self.expected_output) != len(self.user_output):
            print(f"[WA] {self.test_name} Line count mismatch. Expected: {len(self.expected_output)}, Got: {len(self.user_output)}", file=sys.stderr)
            return False
        
        for i, (expected_line, user_line) in enumerate(zip(self.expected_output, self.user_output)):
            if expected_line != user_line:
                print(f"[WA] {self.test_name} Line {i+1} mismatch", file=sys.stderr)
                print(f"  Expected: {expected_line}", file=sys.stderr)
                print(f"  Got: {user_line}", file=sys.stderr)
                return False
        
        print(f"[OK] {self.test_name}")
        return True

