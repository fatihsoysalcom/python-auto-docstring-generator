import re
import sys # For checking Python version for asyncio compatibility

def apply_symbiote_improvements(code_content: str) -> str:
    """
    Simulates the Symbiote tool by adding placeholder docstrings
    to Python functions that are missing them.

    This function processes Python code line by line, identifies function
    definitions (including async functions), and inserts a basic docstring
    if one is not already present immediately after the function signature.
    """
    lines = code_content.splitlines()
    improved_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        improved_lines.append(line)

        # Regex to find function definitions (including async functions)
        # It captures the indentation and the full 'def ...:' line
        # Uses named group 'indent' for easier access
        match = re.match(r'^(?P<indent>\s*)(?:async\s+)?def\s+\w+\s*\(.*\):\s*$', line)
        if match:
            indent = match.group('indent')
            
            # Check if the function already has a docstring
            has_docstring = False
            next_line_idx = i + 1
            
            # Skip empty lines and comments to find the first meaningful line after 'def'
            while next_line_idx < len(lines):
                current_check_line = lines[next_line_idx].strip()
                
                # If the line is empty or a comment, skip it
                if not current_check_line or current_check_line.startswith('#'):
                    next_line_idx += 1
                    continue
                
                # If the first meaningful line starts with a triple quote, it's a docstring
                if current_check_line.startswith('"""') or current_check_line.startswith("'''"):
                    has_docstring = True
                break # Found the first meaningful line, stop looking
            
            # If no docstring was found, insert a placeholder
            if not has_docstring:
                # Add a placeholder docstring with proper indentation
                docstring_indent = indent + '    ' # Standard 4 spaces for docstring
                improved_lines.append(f"{docstring_indent}'''")
                improved_lines.append(f"{docstring_indent}This function performs a specific task.")
                improved_lines.append(f"{docstring_indent}Add a more detailed description here.")
                improved_lines.append(f"{docstring_indent}Args: (if any)")
                improved_lines.append(f"{docstring_indent}Returns: (if any)")
                improved_lines.append(f"{docstring_indent}'''")
        i += 1
    return "\n".join(improved_lines)

# --- Example Usage ---

# Original "poor quality" Python code lacking docstrings
original_code = """
import os
import sys
# This is a comment before a function

# A simple function without a docstring
def calculate_product(x, y):
    # This calculates the product of two numbers
    return x * y

# An async function also without a docstring
async def fetch_data(url):
    # Imagine some async network call here
    import asyncio # This import is part of the example code, not the tool
    await asyncio.sleep(0.01) # Simulate I/O
    return {"url": url, "data": "sample"}

class MyProcessor:
    def __init__(self, name):
        '''
        Initializes the processor with a name.
        Args:
            name (str): The name of the processor.
        '''
        self.name = name

    # Method without a docstring
    def process_item(self, item):
        print(f"Processing {self.name}: {item}")
        return item.upper()

# Another function with an existing docstring
def get_version():
    \"\""
    Returns the current version of the application.
    \"\""
    return "1.0.0"

def simple_action():
    pass # No docstring, just a pass
"""

print("--- Original Python Code ---")
print(original_code)
print("\n" + "="*50 + "\n")

# Apply Symbiote-like improvements
improved_code = apply_symbiote_improvements(original_code)

print("--- Python Code Improved with Symbiote ---")
print(improved_code)

# --- Verification ---
# Attempt to execute the improved code to ensure it's still valid Python
print("\n" + "="*50 + "\n")
print("--- Verifying Improved Code Execution ---")

try:
    # Create a dictionary to hold the namespace of the executed code
    exec_globals = {}
    
    # Execute the improved code string. This will define functions and classes.
    exec(improved_code, exec_globals)
    
    # Test a function that was improved
    calc_prod = exec_globals['calculate_product']
    print(f"  - calculate_product(5, 3) = {calc_prod(5, 3)}")
    
    # Test an existing function
    get_ver = exec_globals['get_version']
    print(f"  - get_version() = {get_ver()}")

    # Test a class method
    my_proc_cls = exec_globals['MyProcessor']
    my_proc_instance = my_proc_cls("Demo")
    processed_val = my_proc_instance.process_item("test_data")
    print(f"  - MyProcessor.process_item('test_data') = {processed_val}")

    # Test an async function, if asyncio is available and Python version supports it
    if sys.version_info >= (3, 7): # asyncio.run requires Python 3.7+
        try:
            import asyncio
            async def run_async_test():
                fetch_func = exec_globals['fetch_data']
                result = await fetch_func("http://example.com")
                print(f"  - fetch_data('http://example.com') = {result}")
            
            asyncio.run(run_async_test())
        except ImportError:
            print("  - Note: 'asyncio' module not found for verification of async function.")
        except Exception as e:
            print(f"  - Error during async function verification: {e}")
    else:
        print("  - Note: Python version < 3.7, skipping async function verification.")

    print("\n--- Improved code executed and verified successfully ---")

except Exception as e:
    print(f"\n--- Error running improved code: {e} ---")
    import traceback
    traceback.print_exc()
