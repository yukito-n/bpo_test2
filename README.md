# Paper Operations Management Tool (MVP)

This project demonstrates a minimal local-first setup for managing data entry and paper operations. It contains a Python backend built with Google Cloud Functions Framework and a React frontend.

## Requirements
- Python 3.9+
- Node.js 16+
- Docker (for Firestore emulator)

## Docker Usage

1. Install Docker Desktop or the Docker Engine for your OS.
   Verify installation with `docker --version`.
2. Pull the emulator image (optional, as `docker run` will pull automatically):
   ```bash
   docker pull google/cloud-sdk:emulators
   ```
3. Start the Firestore emulator container (leave this terminal running):
   - **Linux/macOS**
     ```bash
     docker run --rm -it -p 8081:8080 google/cloud-sdk:emulators \
       gcloud beta emulators firestore start --host-port=0.0.0.0:8080
     ```
   - **Windows (cmd.exe)**
     ```cmd
     docker run --rm -it -p 8081:8080 google/cloud-sdk:emulators ^
       gcloud beta emulators firestore start --host-port=0.0.0.0:8080
     ```
     Make sure there is **no trailing space** after the caret (`^`).
   The `--rm` flag cleans up the container when you stop it with `Ctrl+C`.
   You can confirm it is running using `docker ps`.

## Local Setup

1. **Start the Firestore emulator** (leave this terminal running):
    - **Linux/macOS**
      ```bash
      docker run --rm -it -p 8081:8080 google/cloud-sdk:emulators \
        gcloud beta emulators firestore start --host-port=0.0.0.0:8080
      ```
    - **Windows (cmd.exe)**
      ```cmd
      docker run --rm -it -p 8081:8080 google/cloud-sdk:emulators ^
        gcloud beta emulators firestore start --host-port=0.0.0.0:8080
      ```
      Again ensure no spaces follow the caret.

2. **Install backend dependencies and run the Functions Framework:**
    ```bash
    cd backend
    pip install -r requirements.txt
    export GOOGLE_CLOUD_PROJECT=local-project
    export BUCKET_NAME=receipt-images
    functions-framework --target=create_receipt
    ```

On Windows `cmd.exe`, use `set` to define environment variables:
```cmd
set GOOGLE_CLOUD_PROJECT=local-project
set BUCKET_NAME=receipt-images
functions-framework --target=create_receipt
```
For PowerShell:
```powershell
$env:GOOGLE_CLOUD_PROJECT="local-project"
$env:BUCKET_NAME="receipt-images"
functions-framework --target=create_receipt
```
    Other function targets can be launched in separate terminals using the same command with a different `--target` value.

3. **Install frontend dependencies and start the React app:**
    ```bash
    cd ../frontend
    npm install
    REACT_APP_API_BASE=http://localhost:8080 npm start
    ```

On Windows `cmd.exe` run:
```cmd
set REACT_APP_API_BASE=http://localhost:8080
npm start
```
For PowerShell:
```powershell
$env:REACT_APP_API_BASE='http://localhost:8080'
npm start
```
    The development server runs at <http://localhost:3000>.

4. **Verify the API** (optional example using `curl`):
    ```bash
    curl http://localhost:8080/receipts
    ```

Receipts created in the UI are stored in the Firestore emulator. Cloud Storage can be emulated locally in a similar manner if needed.

## Running with Docker Compose

As an alternative to running services manually, you can launch the backend and Firestore emulator together:

```bash
docker-compose up
```

The backend will be available on `http://localhost:8080` and the emulator on port `8081`. Use `docker-compose down` to stop all containers.
