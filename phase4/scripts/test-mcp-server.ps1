# Test MCP Server - Verification Script

Write-Host "🔍 MCP Server Verification Script" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Gray

# Step 1: Check Python
Write-Host "`n[1/4] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ $pythonVersion" -ForegroundColor Green
    
    # Get Python path
    $pythonPath = (Get-Command python).Source
    Write-Host "   Path: $pythonPath" -ForegroundColor Gray
}
catch {
    Write-Host "   ❌ Python not found!" -ForegroundColor Red
    exit 1
}

# Step 2: Check MCP server file exists
Write-Host "`n[2/4] Checking MCP server file..." -ForegroundColor Yellow
$mcpServerPath = "D:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\backend\tools_mcp.py"

if (Test-Path $mcpServerPath) {
    Write-Host "   ✅ File exists" -ForegroundColor Green
    Write-Host "   Path: $mcpServerPath" -ForegroundColor Gray
}
else {
    Write-Host "   ❌ File not found at: $mcpServerPath" -ForegroundColor Red
    exit 1
}

# Step 3: Test server startup (briefly)
Write-Host "`n[3/4] Testing server startup..." -ForegroundColor Yellow
Write-Host "   (This will start the server for 2 seconds)" -ForegroundColor Gray

try {
    # Start the process
    $process = Start-Process -FilePath "python" `
        -ArgumentList $mcpServerPath `
        -RedirectStandardOutput "mcp_test_stdout.txt" `
        -RedirectStandardError "mcp_test_stderr.txt" `
        -PassThru `
        -NoNewWindow
    
    # Wait 2 seconds
    Start-Sleep -Seconds 2
    
    # Check if still running
    if (-not $process.HasExited) {
        Write-Host "   ✅ Server started and is running" -ForegroundColor Green
        
        # Stop it
        $process.Kill()
        $process.WaitForExit()
        
        # Check stderr for startup messages
        if (Test-Path "mcp_test_stderr.txt") {
            $stderr = Get-Content "mcp_test_stderr.txt" -Raw
            if ($stderr -match "Evolution Tool Hub MCP Server starting") {
                Write-Host "   ✅ Server initialization message found" -ForegroundColor Green
            }
        }
    }
    else {
        Write-Host "   ❌ Server exited immediately (EOF error)" -ForegroundColor Red
        
        # Show errors
        if (Test-Path "mcp_test_stderr.txt") {
            $stderr = Get-Content "mcp_test_stderr.txt" -Raw
            Write-Host "`n   Error output:" -ForegroundColor Red
            Write-Host "   $stderr" -ForegroundColor Yellow
        }
        
        exit 1
    }
}
catch {
    Write-Host "   ❌ Failed to start server: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    # Cleanup test files
    Remove-Item "mcp_test_stdout.txt" -ErrorAction SilentlyContinue
    Remove-Item "mcp_test_stderr.txt" -ErrorAction SilentlyContinue
}

# Step 4: Generate MCP config
Write-Host "`n[4/4] Generating MCP configuration..." -ForegroundColor Yellow

$mcpConfig = @{
    mcpServers = @{
        EvolutionToolHub = @{
            command = $pythonPath
            args    = @($mcpServerPath)
            env     = @{}
        }
    }
} | ConvertTo-Json -Depth 10

Write-Host "   ✅ Configuration generated" -ForegroundColor Green

# Save config to a file
$configPath = "mcp_config_suggested.json"
$mcpConfig | Out-File -FilePath $configPath -Encoding UTF8

Write-Host "`n" + ("=" * 50) -ForegroundColor Cyan
Write-Host "✅ ALL CHECKS PASSED!" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Cyan

Write-Host "`n📋 Next Steps:" -ForegroundColor White
Write-Host "`n1. Open Antigravity Settings → MCP Servers" -ForegroundColor Gray
Write-Host "2. Add or edit 'EvolutionToolHub' server" -ForegroundColor Gray
Write-Host "3. Use this configuration:" -ForegroundColor Gray
Write-Host ""
Write-Host $mcpConfig -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Or copy from: $configPath" -ForegroundColor Gray
Write-Host "5. Enable 'Allow Agent Non-Workspace File Access'" -ForegroundColor Gray
Write-Host "6. Restart Antigravity" -ForegroundColor Gray
Write-Host "7. Look for green dot (●) in MCP Servers" -ForegroundColor Gray

Write-Host "`n💡 Test Command:" -ForegroundColor White
Write-Host '   "Show me the cluster status"' -ForegroundColor Cyan
Write-Host ""
