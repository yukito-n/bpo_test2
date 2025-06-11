# Frontend for Paper Operations Tool

This directory contains the React Single Page Application used to interact with the backend.

## Running Locally

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server (defaults to `http://localhost:3000`):
   ```bash
   REACT_APP_API_BASE=http://localhost:8080 npm start
   ```

On Windows `cmd.exe` use:
```cmd
set REACT_APP_API_BASE=http://localhost:8080
npm start
```
For PowerShell:
```powershell
$env:REACT_APP_API_BASE='http://localhost:8080'
npm start
```

The `REACT_APP_API_BASE` variable defines where API requests are sent. When running the backend with the Functions Framework the base URL should be `http://localhost:8080`.
