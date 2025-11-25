import os
import subprocess
import glob
import sys
from typing import List, Optional, Callable
from pathlib import Path

from testcase import TestCase, normalize

class TestCaseWithChecker(TestCase):
    """Test case that uses external checker program for validation"""
    
    def __init__(self, test_file: str, checker_path: str, test_name: str = ""):
        super().__init__(test_file, test_name)
        self.checker_path = checker_path
        self._validate_checker()
    
    def _validate_checker(self) -> None:
        """Validate that checker program exists and is executable"""
        if not os.path.exists(self.checker_path):
            raise FileNotFoundError(f"Checker program not found: {self.checker_path}")
        
        if not os.access(self.checker_path, os.X_OK):
            raise PermissionError(f"Checker program is not executable: {self.checker_path}")
    
    def validate(self) -> bool:
        """Validate user output using external checker program"""
        if self.user_output is None:
            print(f"[ERR] {self.test_name} No program output to validate", file=sys.stderr)
            return False
        
        try:
            # Prepare input for checker: test input + user output
            checker_input = f"{self.test_input}\n#:\n" + '\n'.join(self.user_output)
            
            result = subprocess.run(
                [self.checker_path],
                input=checker_input,
                text=True,
                capture_output=True,
                timeout=5,
                encoding='utf-8'
            )
            if result.returncode == 0:
                print(f"[OK] {self.test_name}")
                return True
            else:
                print(f"[WA] {self.test_name}", file=sys.stderr)
                if result.stderr is not None:
                    print(result.stderr, file=sys.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print(f"[TL] {self.test_name} Checker timeout", file=sys.stderr)
            return False
        except Exception as e:
            print(f"[ERR] {self.test_name} Checker error: {str(e)}", file=sys.stderr)
            return False

