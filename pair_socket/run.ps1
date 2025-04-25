# Windows PowerShell version of run.sh
# Save this as run.ps1 in the same folder as config.txt
# Usage:  right‑click › “Run with PowerShell”  (or execute `.
un.ps1`)

$FilePath  = "config.txt"
$Endpoint  = "http://192.168.25.1:5000/guideDone"

try {
    # Read the entire JSON file as a single string
    $Body = Get-Content -Path $FilePath -Raw

    # POST the JSON to the SP9 hotspot
    Invoke-RestMethod -Uri $Endpoint -Method Post -Body $Body -ContentType 'application/json'

    Write-Host "✓ Configuration sent successfully."
}
catch {
    Write-Error "✗ Failed to send configuration:`n$_"
}
