import os
import subprocess
import glob
import sys
from typing import List, Optional, Callable
from pathlib import Path
from abc import ABC, abstractmethod


def normalize(stdout: List[str]) -> List[str]:
    """Normalize output by removing empty lines and stripping whitespace"""
    return list(filter(
        lambda s: (not s.isspace()) and len(s) > 0,
        map(
            lambda s: s.strip('\n').strip(),
            stdout
        )
    ))


class TestCase(ABC):
    """Abstract base class for test cases"""
    
    def __init__(self, test_file: str, test_name: str = ""):
        self.test_file = test_file
        self.test_name = test_name or os.path.basename(test_file)
        self.test_input = ""
        self.user_output: Optional[List[str]] = None
        self._load_test_input()
    
    def _load_test_input(self) -> None:
        """Load test input from file"""
        try:
            with open(self.test_file, 'r', encoding='utf-8') as f:
                self.test_input = f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to load test input from {self.test_file}: {str(e)}")
    
    def run_program(self, program_path: str) -> bool:
        """Run the program with test input and capture output"""
        try:
            if not os.path.exists(program_path):
                print(f"[ERR] {self.test_name} Program not found: {program_path}", file=sys.stderr)
                return False
            
            result = subprocess.run(
                [program_path],
                input=self.test_input,
                text=True,
                capture_output=True,
                timeout=10,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                print(f"[ERR] {self.test_name} Runtime Error ({result.returncode}): {result.stderr}", file=sys.stderr)
                return False
            
            self.user_output = normalize(result.stdout.split('\n'))
            return True
            
        except subprocess.TimeoutExpired:
            print(f"[TL] {self.test_name} Timeout", file=sys.stderr)
            return False
        except Exception as e:
            print(f"[ERR] {self.test_name} Unexpected error: {str(e)}", file=sys.stderr)
            return False
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate program output against expected result"""
        pass
    
    def execute(self, program_path: str) -> bool:
        """Execute full test: run program and validate output"""
        if not self.run_program(program_path):
            return False
        return self.validate()


