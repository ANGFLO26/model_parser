"""
Merge Utilities for dots.ocr

Provides functions to merge individual page outputs (MD/JSON) into combined documents
and create download packages based on user preferences.
"""

import os
import re
import json
import zipfile
from typing import Optional, List, Dict, Literal
import shutil


def numerical_sort(value: str) -> List:
    """
    Sort files numerically (e.g., page_2 comes before page_10)
    
    Args:
        value: String to sort (typically filename)
        
    Returns:
        List of parts for sorting
    """
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def merge_markdown_files(
    output_dir: str,
    filename_base: Optional[str] = None,
    output_filename: str = "MERGED_DOCUMENT.md"
) -> Optional[str]:
    """
    Merge all page_*.md files in output_dir into a single markdown file
    
    Args:
        output_dir: Directory containing markdown files
        filename_base: Base filename for context (optional, not used in output)
        output_filename: Name of the output merged file
        
    Returns:
        Path to merged file, or None if no files found
    """
    if not os.path.exists(output_dir):
        return None
    
    # Find all markdown files
    md_files = []
    for file in os.listdir(output_dir):
        if file.endswith(".md") and "page_" in file.lower():
            full_path = os.path.join(output_dir, file)
            md_files.append(full_path)
    
    if not md_files:
        return None
    
    # Sort numerically
    md_files.sort(key=lambda x: numerical_sort(os.path.basename(x)))
    
    # Build merged content - simple concatenation
    merged_content = ""
    
    for idx, file_path in enumerate(md_files, 1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                # Remove hyphenation at line breaks
                text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
                
                # Simply append the content
                merged_content += text
                
                # Add spacing between pages (but not after the last page)
                if idx < len(md_files):
                    merged_content += "\n\n"
        except Exception as e:
            print(f"Warning: Failed to read {file_path}: {e}")
            continue
    
    # Save merged file
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(merged_content)
    
    return output_path


def merge_json_files(
    output_dir: str,
    filename_base: Optional[str] = None,
    output_filename: str = "MERGED_LAYOUT.json"
) -> Optional[str]:
    """
    Merge all page_*.json files into a single JSON structure
    
    Args:
        output_dir: Directory containing JSON files
        filename_base: Base filename for context (optional)
        output_filename: Name of the output merged file
        
    Returns:
        Path to merged file, or None if no files found
    """
    if not os.path.exists(output_dir):
        return None
    
    # Find all JSON files
    json_files = []
    for file in os.listdir(output_dir):
        if file.endswith(".json") and "page_" in file.lower():
            full_path = os.path.join(output_dir, file)
            json_files.append(full_path)
    
    if not json_files:
        return None
    
    # Sort numerically
    json_files.sort(key=lambda x: numerical_sort(os.path.basename(x)))
    
    # Build merged structure
    merged_data = {
        "document": filename_base if filename_base else "Merged Document",
        "total_pages": len(json_files),
        "pages": []
    }
    
    for idx, file_path in enumerate(json_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                page_data = json.load(f)
                
                merged_data["pages"].append({
                    "page_number": idx,
                    "elements": page_data if isinstance(page_data, list) else [page_data]
                })
        except Exception as e:
            print(f"Warning: Failed to read {file_path}: {e}")
            merged_data["pages"].append({
                "page_number": idx,
                "error": str(e)
            })
    
    # Save merged file
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)
    
    return output_path


def create_download_package(
    output_dir: str,
    format_choice: Literal["markdown", "json", "both"],
    scope_choice: Literal["individual", "merged", "both"],
    filename_base: Optional[str] = None
) -> Optional[str]:
    """
    Create a ZIP package based on user's format and scope choices
    
    Args:
        output_dir: Directory containing processed results
        format_choice: "markdown" | "json" | "both"
        scope_choice: "individual" | "merged" | "both"
        filename_base: Base name for the original file
        
    Returns:
        Path to created ZIP file, or None on error
    """
    if not os.path.exists(output_dir):
        return None
    
    files_to_zip = []
    
    # Handle Markdown format
    if format_choice in ["markdown", "both"]:
        # Individual MD files
        if scope_choice in ["individual", "both"]:
            for file in os.listdir(output_dir):
                if file.endswith(".md") and "page_" in file.lower():
                    files_to_zip.append(os.path.join(output_dir, file))
        
        # Merged MD file
        if scope_choice in ["merged", "both"]:
            merged_md = merge_markdown_files(
                output_dir,
                filename_base,
                "MERGED_DOCUMENT.md"
            )
            if merged_md and os.path.exists(merged_md):
                files_to_zip.append(merged_md)
    
    # Handle JSON format
    if format_choice in ["json", "both"]:
        # Individual JSON files
        if scope_choice in ["individual", "both"]:
            for file in os.listdir(output_dir):
                if file.endswith(".json") and "page_" in file.lower():
                    files_to_zip.append(os.path.join(output_dir, file))
        
        # Merged JSON file
        if scope_choice in ["merged", "both"]:
            merged_json = merge_json_files(
                output_dir,
                filename_base,
                "MERGED_LAYOUT.json"
            )
            if merged_json and os.path.exists(merged_json):
                files_to_zip.append(merged_json)
    
    if not files_to_zip:
        return None
    
    # Create ZIP file
    zip_filename = f"{filename_base or 'download'}_package.zip"
    zip_path = os.path.join(output_dir, zip_filename)
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files_to_zip:
                # Add file to ZIP with just the filename (not full path)
                zipf.write(file_path, os.path.basename(file_path))
        
        return zip_path
    except Exception as e:
        print(f"Error creating ZIP: {e}")
        return None


def count_files_in_zip(zip_path: str) -> int:
    """
    Count the number of files in a ZIP archive
    
    Args:
        zip_path: Path to ZIP file
        
    Returns:
        Number of files in ZIP
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            return len(zipf.namelist())
    except:
        return 0


def get_zip_size_mb(zip_path: str) -> float:
    """
    Get size of ZIP file in MB
    
    Args:
        zip_path: Path to ZIP file
        
    Returns:
        Size in MB
    """
    try:
        size_bytes = os.path.getsize(zip_path)
        return size_bytes / (1024 * 1024)
    except:
        return 0.0
