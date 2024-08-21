import os
import json
import ast
import logging
from pathlib import Path
from typing import List, Dict, Any
import re  # Import for regex usage in JavaScript/TypeScript parsing

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Define a file size limit (in characters)
FILE_SIZE_LIMIT = 10000  # Example limit, set this to your desired size

def analyze_directory_structure(base_path: Path) -> Dict[str, Any]:
    structure = {
        "directories": {},
        "files": {}  # Changed from 'file_content' to 'files'
    }
    
    for root, dirs, files in os.walk(base_path):
        # Save directories with the relative paths
        structure["directories"][root] = {
            "directories": [os.path.join(root, d) for d in dirs],
            "files": [os.path.join(root, f) for f in files]
        }
        for file in files:
            file_path = os.path.join(root, file)
            # Read and store file content with size limit check
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    if len(content) > FILE_SIZE_LIMIT:
                        structure["files"][file_path] = "file too long"
                    else:
                        structure["files"][file_path] = content
            except Exception as e:
                logging.warning(f"Failed to read file {file_path}: {e}")
    
    return structure

def parse_code_files(files: List[Path]) -> Dict[str, Any]:
    code_structure = {}
    
    for file in files:
        try:
            content = file.read_text(encoding='utf-8', errors='replace')
            
            if file.suffix == '.py':
                tree = ast.parse(content, filename=str(file))
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                imports = [ast.unparse(node) for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
                
            elif file.suffix in ['.js', '.ts', ".jsx", ".tsx"]:
                # Simple regex-based parsing for JavaScript/TypeScript
                classes = re.findall(r'class\s+(\w+)', content)
                functions = re.findall(r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>))', content)
                functions = [f[0] or f[1] for f in functions if f[0] or f[1]]  # Flatten the function matches
                imports = re.findall(r'^(import\s+.*?;)$', content, re.MULTILINE)
            
            elif file.suffix == '.java':
                # Simple regex-based parsing for Java
                classes = re.findall(r'class\s+(\w+)', content)
                functions = re.findall(r'(?:public|private|protected|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *\{', content)
                imports = re.findall(r'^(import\s+.*;)$', content, re.MULTILINE)
            
            else:
                continue  # Skip unsupported file types
            
            # Only add to code_structure if there are classes, functions, or imports
            if classes or functions or imports:
                code_structure[str(file)] = {
                    "classes": classes,
                    "functions": functions,
                    "imports": imports
                }
        
        except Exception as e:
            logging.warning(f"Failed to parse file {file}: {e}")
    
    return code_structure

def read_documentation(files: List[Path]) -> Dict[str, str]:
    documentation = {}
    
    for file in files:
        if 'readme' in file.name.lower():
            try:
                with open(file, 'r', encoding='utf-8', errors='replace') as f:
                    documentation[str(file)] = f.read()
            except Exception as e:
                logging.warning(f"Failed to read documentation file {file}: {e}")
    
    return documentation

def save_to_json(data: Dict[str, Any], output_file: str) -> None:
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save results to {output_file}: {e}")

def main(base_path: str, output_file: str):
    base_path = Path(base_path)
    structure = analyze_directory_structure(base_path)
    files = [Path(file) for file in structure["files"]]

    code_info = parse_code_files(files)
    documentation = read_documentation(files)
    
    result = {
        "Directory and File Structure": structure,
        "Classes, Functions, and Imports": code_info,
        "Documentation and Comments": documentation,
    }
    
    # Save result to a JSON file
    save_to_json(result, output_file)
    
    # Pretty-print the result for immediate feedback
    from rich import print
    #print(result)

if __name__ == "__main__":
    base_path = './fullstack'
    output_file = 'codebase_analysis.json'
    main(base_path, output_file)
