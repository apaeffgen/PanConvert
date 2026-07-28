# Download Inno Setup silently
$url = "https://jrsoftware.org/download.php/is.exe"
$output = "C:\Users\apaeffgen\Downloads\InnoSetup.exe"

Write-Host "Downloading Inno Setup from $url ..."
try {
    Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
    $size = (Get-Item $output).Length / 1MB
    Write-Host "Download complete: $([math]::Round($size, 2)) MB"
} catch {
    Write-Host "Download failed: $_"
    exit 1
}

# Install silently
Write-Host "Installing Inno Setup silently..."
$proc = Start-Process -FilePath $output -ArgumentList "/SILENT" -Wait -PassThru
Write-Host "Install exit code: $($proc.ExitCode)"

# Find iscc.exe
$isccPaths = @(
    "C:\Program Files (x86)\Inno Setup 6\iscc.exe",
    "C:\Program Files\Inno Setup 6\iscc.exe"
)

foreach ($path in $isccPaths) {
    if (Test-Path $path) {
        Write-Host "Found iscc.exe at: $path"
        break
    }
}
