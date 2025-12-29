#!/usr/bin/env python3
"""
Test MCP Server - Quick diagnostic tool
"""

import sys
import json
import subprocess

def test_mcp_server():
    """Test the MCP server manually"""
    
    server_path = r"D:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\backend\tools_mcp.py"
    python_path = r"C:\Python313\python.exe"
    
    print("🔍 Testing MCP Server...")
    print(f"Server: {server_path}")
    print(f"Python: {python_path}\n")
    
    # Start the server process
    process = subprocess.Popen(
        [python_path, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Test 1: Initialize
    print("Test 1: Sending 'initialize' request...")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {}
        }
    }
    
    process.stdin.write(json.dumps(init_request) + "\n")
    process.stdin.flush()
    
    # Read response
    response_line = process.stdout.readline()
    print(f"Response: {response_line}")
    
    try:
        response = json.loads(response_line)
        print(f"✅ Valid JSON response")
        print(f"   Protocol: {response.get('result', {}).get('protocolVersion', 'N/A')}")
    except:
        print(f"❌ Invalid JSON response")
    
    # Test 2: List tools
    print("\nTest 2: Sending 'tools/list' request...")
    tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    process.stdin.write(json.dumps(tools_request) + "\n")
    process.stdin.flush()
    
    # Read response
    response_line = process.stdout.readline()
    print(f"Response: {response_line}")
    
    try:
        response = json.loads(response_line)
        tools = response.get('result', {}).get('tools', [])
        print(f"✅ Valid JSON response")
        print(f"   Tool count: {len(tools)}")
        for tool in tools:
            print(f"   - {tool.get('name')}: {tool.get('description')[:50]}...")
    except Exception as e:
        print(f"❌ Invalid JSON response: {e}")
    
    # Check stderr for errors
    print("\nServer stderr output:")
    process.terminate()
    process.wait(timeout=2)
    stderr = process.stderr.read()
    if stderr:
        print(stderr)
    else:
        print("(none)")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    test_mcp_server()
