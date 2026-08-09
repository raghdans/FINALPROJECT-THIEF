$ErrorActionPreference = "Stop"
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Create the environment first: py -3.12 -m venv .venv; .\.venv\Scripts\python.exe -m pip install -e ."
}
& $python -m police_thief peer --role thief @args
