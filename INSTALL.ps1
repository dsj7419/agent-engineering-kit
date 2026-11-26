# Preview by default. Specify -Apply only after reviewing the proposed changes.
param(
    [Parameter(Mandatory=$true)][string]$Target,
    [switch]$Apply,
    [switch]$WithTools
)
$ErrorActionPreference = 'Stop'
$python = $null
foreach ($candidate in @(Get-Command python -All -CommandType Application -ErrorAction SilentlyContinue)) {
    # Store execution aliases can open an interactive installer instead of Python.
    if ($candidate.Source -match '\\Microsoft\\WindowsApps\\python\.exe$') { continue }
    try {
        & $candidate.Source -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' *> $null
        if ($LASTEXITCODE -eq 0) {
            $python = $candidate.Source
            break
        }
    } catch {
        # An unusable PATH entry must not hide a later working interpreter.
        continue
    }
}
if ($null -eq $python) {
    throw 'Python 3.9+ is required. Add a working Python installation to PATH; Windows Store execution aliases are skipped.'
}
$arguments = @((Join-Path $PSScriptRoot 'tools/release/install_kit.py'), '--target', $Target)
if ($Apply) { $arguments += '--apply' }
if ($WithTools) { $arguments += '--with-tools' }
& $python @arguments
exit $LASTEXITCODE
