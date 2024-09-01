# Script: manage_rpi_connections.ps1
$filePath = "C:\Users\YourUsername\raspberry_pi_ips.txt"

# Read Raspberry Pi IPs from the file
if (Test-Path $filePath) {
    $ips = Get-Content $filePath | Select-Object -Unique

    foreach ($line in $ips) {
        $splitLine = $line -split ","
        $hostname = $splitLine[0]
        $ip = $splitLine[1]
        $date = $splitLine[2]

        # Here, add any logic to handle the new IPs, e.g., connect via SSH or log them
        Write-Host "Hostname: $hostname, IP: $ip, Last Sync: $date"
    }
} else {
    Write-Host "No Raspberry Pi IP information found."
}
