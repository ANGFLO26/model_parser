#!/usr/bin/env python3
"""
Test script to verify numerical sorting logic for merge_utils
"""

import re
from typing import List

def numerical_sort(value: str) -> List:
    """
    Sort files numerically (e.g., page_2 comes before page_10)
    """
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

# Test cases
test_files = [
    "page_10.md",
    "page_2.md",
    "page_1.md",
    "page_15.md",
    "page_3.md",
    "page_20.md",
    "page_11.md",
    "page_5.md"
]

print("Original order:")
for f in test_files:
    print(f"  {f}")

print("\nSorted with numerical_sort:")
sorted_files = sorted(test_files, key=numerical_sort)
for f in sorted_files:
    print(f"  {f}")

print("\nExpected order:")
expected = [
    "page_1.md",
    "page_2.md", 
    "page_3.md",
    "page_5.md",
    "page_10.md",
    "page_11.md",
    "page_15.md",
    "page_20.md"
]
for f in expected:
    print(f"  {f}")

print("\n" + "="*50)
if sorted_files == expected:
    print("✅ PASS: Sorting is CORRECT!")
else:
    print("❌ FAIL: Sorting is INCORRECT!")
    print("\nDifferences:")
    for i, (got, exp) in enumerate(zip(sorted_files, expected)):
        if got != exp:
            print(f"  Position {i}: got '{got}', expected '{exp}'")
