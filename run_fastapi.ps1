$Path = ".\Chroma_db"

if (Test-Path -Path $Path) {
    Write-Output "Removing the chroma db folder..."
    Remove-Item -Path $Path -Recurse -Force
    Write-Output "Folder deleted successfully."
}  
Write-Output "Running Server"

uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000