# Recursively scans folders to list locations containing non-data files (e.g., binaries, caches) while excluding common data types like documents, media, and code files.
param(
    [string]$RootPath = ".",
    [string[]]$DataExtensions = @(".docx", ".doc", ".txt", ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".py", ".csv", ".json", ".yaml", ".yml", ".xlsx", ".drawio", ".mp4", ".mp3", ".mkv", ".mov", ".wav", ".m4a", ".webm", ".xls", ".bat", ".sh", ".zip", ".rar", ".7z", ".tar", ".gz")
)

Write-Host "Scanning for non-data files under: $RootPath`n"

# Normalize to lowercase for comparison
$dataExts = $DataExtensions | ForEach-Object { $_.ToLower() }

# Recursively find all files
Get-ChildItem -Path $RootPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        $ext = $_.Extension.ToLower()
        -not ($dataExts -contains $ext)
    } |
    Select-Object -ExpandProperty DirectoryName |
    Sort-Object -Unique |
    ForEach-Object { Write-Output $_ }

Write-Host "`nScan complete."
