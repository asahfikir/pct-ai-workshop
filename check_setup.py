#!/usr/bin/env python3
"""
Pre-Workshop Setup Verification Script
=======================================
Run this BEFORE the workshop to catch problems early.

Usage:
    python check_setup.py

What it checks:
1. Python version (3.11+ required)
2. Git installed
3. UV installed
4. Repo cloned (or current directory is the repo)
5. Virtual environment exists
6. Dependencies installed
7. Database created
8. API server can start (brief test)
9. MCP server can start (brief test)

Exit codes:
    0 = All checks passed
    1 = One or more checks failed
"""

import subprocess
import sys
import os
import time
import json
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_check(name, status, detail="", fix=""):
    """Print a check result with color."""
    if status == "PASS":
        symbol = f"{Colors.GREEN}✓{Colors.END}"
        status_text = f"{Colors.GREEN}PASS{Colors.END}"
    elif status == "FAIL":
        symbol = f"{Colors.RED}✗{Colors.END}"
        status_text = f"{Colors.RED}FAIL{Colors.END}"
    elif status == "WARN":
        symbol = f"{Colors.YELLOW}⚠{Colors.END}"
        status_text = f"{Colors.YELLOW}WARN{Colors.END}"
    else:
        symbol = "?"
        status_text = status
    
    print(f"  {symbol} {name:<30} {status_text}")
    if detail:
        print(f"      {detail}")
    if fix:
        print(f"      {Colors.YELLOW}Fix:{Colors.END} {fix}")

def run_command(cmd, timeout=10, capture=True):
    """Run a shell command and return (success, output, error)."""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(
                cmd,
                shell=True,
                timeout=timeout
            )
            return result.returncode == 0, "", ""
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_python():
    """Check Python version."""
    success, stdout, stderr = run_command("python --version")
    if not success:
        # Try python3
        success, stdout, stderr = run_command("python3 --version")
    
    if not success:
        return False, "Python not found", "Install Python 3.11+ from python.org"
    
    version_str = stdout.strip() or stderr.strip()
    # Extract version number
    import re
    match = re.search(r'(\d+)\.(\d+)', version_str)
    if not match:
        return False, f"Could not parse version: {version_str}", "Reinstall Python"
    
    major, minor = int(match.group(1)), int(match.group(2))
    if major < 3 or (major == 3 and minor < 11):
        return False, f"Python {major}.{minor} found (3.11+ required)", "Upgrade Python from python.org"
    
    return True, f"Python {major}.{minor}", ""

def check_git():
    """Check Git is installed."""
    success, stdout, stderr = run_command("git --version")
    if not success:
        return False, "Git not found", "Install Git from git-scm.com"
    
    version = stdout.strip().split('\n')[0]
    return True, version, ""

def check_uv():
    """Check UV is installed."""
    success, stdout, stderr = run_command("uv --version")
    if not success:
        return False, "UV not found", "Install UV: curl -LsSf https://astral.sh/uv/install.sh | sh"
    
    version = stdout.strip().split('\n')[0]
    return True, version, ""

def check_repo():
    """Check we're in the repo folder."""
    required_files = ['api', 'mcp', 'docs', 'requirements.txt']
    missing = [f for f in required_files if not os.path.exists(f)]
    
    if missing:
        return False, f"Missing: {', '.join(missing)}", "Clone the repo: git clone https://github.com/asahfikir/palembang-workshop.git"
    
    return True, "All required files present", ""

def check_venv():
    """Check virtual environment exists."""
    venv_paths = ['.venv', 'venv', 'env']
    found = [p for p in venv_paths if os.path.exists(p)]
    
    if not found:
        return False, "No virtual environment found", "Run: uv venv"
    
    return True, f"Found: {found[0]}", ""

def check_dependencies():
    """Check key dependencies are installed."""
    # Determine Python executable in venv
    if os.path.exists('.venv'):
        if os.name == 'nt':  # Windows
            python_exe = r'.venv\Scripts\python'
        else:
            python_exe = '.venv/bin/python'
    else:
        python_exe = 'python'
    
    required = ['fastapi', 'uvicorn', 'requests', 'pydantic']
    missing = []
    
    for pkg in required:
        success, _, _ = run_command(f'{python_exe} -c "import {pkg}"')
        if not success:
            missing.append(pkg)
    
    if missing:
        return False, f"Missing: {', '.join(missing)}", f"Run: uv pip install -r requirements.txt"
    
    return True, "All dependencies installed", ""

def check_database():
    """Check database file exists."""
    if not os.path.exists('academic.db'):
        return False, "Database not found", "Run: python api/mock_database.py"
    
    # Check it's not empty
    size = os.path.getsize('academic.db')
    if size < 1000:
        return False, f"Database too small ({size} bytes)", "Recreate: python api/mock_database.py"
    
    return True, f"Database exists ({size:,} bytes)", ""

def check_api_server():
    """Check API server can start."""
    import urllib.request
    import urllib.error
    
    # First, check if something is already running on port 8000
    try:
        req = urllib.request.Request('http://localhost:8000/health', method='GET')
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                return True, "API already running on port 8000", ""
    except:
        pass  # Nothing running, which is expected
    
    # Try to start the server briefly
    if os.name == 'nt':
        python_exe = r'.venv\Scripts\python'
    else:
        python_exe = '.venv/bin/python' if os.path.exists('.venv/bin/python') else 'python'
    
    try:
        proc = subprocess.Popen(
            [python_exe, 'api/main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Try to connect
        try:
            req = urllib.request.Request('http://localhost:8000/health', method='GET')
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                proc.terminate()
                return True, "API server starts and responds", ""
        except urllib.error.URLError:
            proc.terminate()
            return False, "API server started but not responding", "Check api/main.py for errors"
        except Exception as e:
            proc.terminate()
            return False, f"Error connecting to API: {e}", "Check if port 8000 is in use"
            
    except Exception as e:
        return False, f"Could not start API: {e}", "Check Python path and dependencies"

def check_mcp_server():
    """Check MCP server can start."""
    import urllib.request
    
    # Check if already running
    try:
        req = urllib.request.Request('http://localhost:8001/tools/list', method='GET')
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                return True, "MCP already running on port 8001", ""
    except:
        pass
    
    if os.name == 'nt':
        python_exe = r'.venv\Scripts\python'
    else:
        python_exe = '.venv/bin/python' if os.path.exists('.venv/bin/python') else 'python'
    
    try:
        proc = subprocess.Popen(
            [python_exe, 'mcp/server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        
        time.sleep(3)
        
        try:
            req = urllib.request.Request('http://localhost:8001/tools/list', method='GET')
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                proc.terminate()
                if 'tools' in data:
                    return True, f"MCP server responds with {len(data['tools'])} tools", ""
                else:
                    return False, "MCP server responded but no tools found", "Check mcp/server.py"
        except Exception as e:
            proc.terminate()
            return False, f"MCP server not responding: {e}", "Check if port 8001 is in use"
            
    except Exception as e:
        return False, f"Could not start MCP: {e}", "Check Python path and dependencies"

def main():
    """Run all checks."""
    print(f"\n{Colors.BOLD}🔍 Pre-Workshop Setup Verification{Colors.END}")
    print(f"{'='*50}\n")
    
    checks = [
        ("Python 3.11+", check_python),
        ("Git", check_git),
        ("UV Package Manager", check_uv),
        ("Repository Files", check_repo),
        ("Virtual Environment", check_venv),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
        ("API Server", check_api_server),
        ("MCP Server", check_mcp_server),
    ]
    
    passed = 0
    failed = 0
    warnings = 0
    
    for name, check_func in checks:
        try:
            success, detail, fix = check_func()
            if success:
                print_check(name, "PASS", detail)
                passed += 1
            else:
                print_check(name, "FAIL", detail, fix)
                failed += 1
        except Exception as e:
            print_check(name, "FAIL", f"Unexpected error: {e}", "Ask the instructor")
            failed += 1
    
    print(f"\n{'='*50}")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ All checks passed! You're ready for the workshop.{Colors.END}")
        print(f"\nNext steps:")
        print(f"  1. Keep this terminal open")
        print(f"  2. During Session 1, run: python api/main.py")
        print(f"  3. During Session 2, run: python mcp/server.py")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ {failed} check(s) failed.{Colors.END}")
        print(f"\n{Colors.YELLOW}Don't worry! Here's what to do:{Colors.END}")
        print(f"  1. Fix the issues above (each has a suggested fix)")
        print(f"  2. Run this script again: python check_setup.py")
        print(f"  3. If still stuck, ask the instructor BEFORE the workshop")
        print(f"\n{Colors.BLUE}Alternative: If you can't fix the issues, you can still participate by:")
        print(f"  - Watching the instructor's demo on the projector")
        print(f"  - Using the browser interface at http://localhost:8000/docs")
        print(f"  - Asking a neighbor to share their screen{Colors.END}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
