import os
import subprocess
import glob
import sys
from typing import List, Optional, Callable, Dict
from pathlib import Path
from testcase_with_answer import TestCaseWithAnswer
from testcase_with_checker import TestCaseWithChecker

class TestRunner:
    """Main test runner class"""
    
    def __init__(self, problems: List[int]):
        self.problems = problems
        self.test_cases = {i : [] for i in problems}
        self.programs = {i : None for i in problems}
    
    def discover(self) -> None:
        """Discover and create test cases for all solutions"""
        for i in self.problems:
            program_name = f"solution-{i:02d}"
            program_path = Path("./solutions") / program_name
            
            if not program_path.exists():
                print(f"[SKIPPED {i:02d}]")
                continue

            self.programs[i] = program_path
            
            # Try to find tests:
            input_pattern = f"tests/inputs/{i:02d}/*.txt"
            input_files = sorted(glob.glob(input_pattern))
            
            # Create TestCaseWithAnswer for each test
            for input_file in input_files:
                test_name = Path(input_file).stem
                output_file = Path(f"tests/outputs/{i:02d}/{test_name}.txt")
                if output_file.exists():
                    test_case = TestCaseWithAnswer(
                        test_file=str(input_file),
                        answer_file=str(output_file),
                        test_name=f"{i:02d}/{test_name}"
                    )
                    self.test_cases[i].append(test_case)
    
    def add_checker_tests(self, problem : int, checker_path: str) -> None:
        """Add test cases that use external checker"""
        input_pattern = f"tests/inputs/{problem:02d}/*.txt"
        input_files = sorted(glob.glob(input_pattern))
        for test_file in input_files:
            test_case = TestCaseWithChecker(
                test_file=test_file,
                checker_path=checker_path,
                test_name=Path(test_file).stem
            )
            self.test_cases[problem].append(test_case)
    
    def run_all_tests(self) -> Dict[int, bool]:
        """Run all tests"""
        if not self.test_cases:
            print("No tests discovered")
            return False

        summary = {p : True for p in self.problems}

        for problem in self.problems: 
            if self.programs[problem] is None:
                continue
            total_tests = len(self.test_cases[problem])
            passed_tests = 0
            
            if total_tests == 0:
                continue

            print(f"Running {total_tests} tests for problem {problem:02d}...")
            print("=" * 60)
            
            for test_case in self.test_cases[problem]:
                if test_case.execute(str(self.programs[problem])):
                    passed_tests += 1
            
            print("=" * 60)
            print(f"RESULTS: {passed_tests}/{total_tests} tests passed")

            if passed_tests != total_tests:
                summary[problem] = False
            
        return summary

