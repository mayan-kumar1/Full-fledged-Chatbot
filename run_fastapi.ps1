Write-Output "Removing the chroma db folder"
Remove-Item -Path ".\Chroma_db" -Recurse -Force

Write-Output "Running Server"

uv run uvicorn app.api:app --reload --host 127.0.0.1 --port 8000