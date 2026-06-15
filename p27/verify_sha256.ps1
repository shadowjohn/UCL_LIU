param(
  [string]$ManifestPath = (Join-Path $PSScriptRoot "SHA256SUMS.txt"),
  [string]$BasePath = $PSScriptRoot
)

$ErrorActionPreference = "Stop"
$hadFailure = $false
$checkedCount = 0

function Report-Failure {
  param([Parameter(Mandatory = $true)][string]$Message)
  Write-Host "[ERROR] $Message"
  $script:hadFailure = $true
}

function Resolve-BasePath {
  param([Parameter(Mandatory = $true)][string]$Path)
  if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
    throw "Base path does not exist: $Path"
  }
  return [System.IO.Path]::GetFullPath((Resolve-Path -LiteralPath $Path).ProviderPath).TrimEnd("\")
}

if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
  Write-Host "[ERROR] SHA256 manifest not found: $ManifestPath"
  exit 1
}

$baseFullPath = Resolve-BasePath -Path $BasePath
$basePrefix = $baseFullPath + "\"
$manifestLines = @(Get-Content -LiteralPath $ManifestPath)

for ($i = 0; $i -lt $manifestLines.Count; $i++) {
  $lineNumber = $i + 1
  $line = $manifestLines[$i].Trim()

  if ($line -eq "" -or $line.StartsWith("#")) {
    continue
  }

  $match = [regex]::Match($line, "^(?<hash>[A-Fa-f0-9]{64})\s+\*?(?<path>.+?)\s*$")
  if (-not $match.Success) {
    Report-Failure "Invalid manifest line $lineNumber`: $line"
    continue
  }

  $expectedHash = $match.Groups["hash"].Value.ToLowerInvariant()
  $relativePath = $match.Groups["path"].Value.Replace("/", "\")

  if ([System.IO.Path]::IsPathRooted($relativePath)) {
    Report-Failure "Manifest line $lineNumber uses an absolute path: $relativePath"
    continue
  }

  $fullPath = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($baseFullPath, $relativePath))
  if (-not $fullPath.StartsWith($basePrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    Report-Failure "Manifest line $lineNumber escapes the base path: $relativePath"
    continue
  }

  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    Report-Failure "Missing file listed in manifest line $lineNumber`: $relativePath"
    continue
  }

  $actualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $fullPath).Hash.ToLowerInvariant()
  if ($actualHash -ne $expectedHash) {
    Report-Failure "SHA256 mismatch for $relativePath. Expected $expectedHash, got $actualHash."
    continue
  }

  $checkedCount++
  Write-Host "[OK] $relativePath"
}

if ($hadFailure) {
  Write-Host "[ERROR] SHA256 verification failed."
  exit 1
}

Write-Host "[OK] Verified $checkedCount files from $ManifestPath."
exit 0
