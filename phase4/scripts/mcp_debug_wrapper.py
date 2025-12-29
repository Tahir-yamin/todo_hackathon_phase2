#!/usr/bin/env python3
"""
MCP Server Logger - Diagnostic wrapper
Logs all stdin/stdout to files for debugging
"""

import sys
import subprocess
import threading
import time

def log_stream(stream, filename, prefix):
    """Log stream to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"=== {prefix} Stream Log ===\n")
        f.write(f"Started at: {time.ctime()}\n\n")
        for line in stream:
            f.write(f"[{time.time()}] {line}")
            f.flush()

def main():
    server_path = r"D:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\backend\tools_mcp.py"
    python_path = r"C:\Python313\python.exe"
    
    # Start the actual MCP server
    process = subprocess.Popen(
        [python_path, "-u", "-W", "ignore", server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0  # Unbuffered
    )
    
    # Log stderr to file
    stderr_thread = threading.Thread(
        target=log_stream,
        args=(process.stderr, "mcp_stderr.log", "STDERR")
    )
    stderr_thread.daemon = True
    stderr_thread.start()
    
    # Log stdout to file
    stdout_log = open("mcp_stdout.log", 'w', encoding='utf-8')
    stdout_log.write("=== STDOUT Stream Log ===\n")
    stdout_log.write(f"Started at: {time.ctime()}\n\n")
    stdout_log.flush()
    
    # Pass stdin through and log
    stdin_log = open("mcp_stdin.log", 'w', encoding='utf-8')
    stdin_log.write("=== STDIN Stream Log ===\n")
    stdin_log.write(f"Started at: {time.ctime()}\n\n")
    stdin_log.flush()
    
    try:
        # Forward stdin to process
        for line in sys.stdin:
            stdin_log.write(f"[{time.time()}] {line}")
            stdin_log.flush()
            
            process.stdin.write(line)
            process.stdin.flush()
            
            # Read response
            response = process.stdout.readline()
            stdout_log.write(f"[{time.time()}] {response}")
            stdout_log.flush()
            
            # Forward to stdout
            sys.stdout.write(response)
            sys.stdout.flush()
    
    except KeyboardInterrupt:
        pass
    finally:
        stdin_log.close()
        stdout_log.close()
        process.terminate()

if __name__ == "__main__":
    main()
