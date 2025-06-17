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
    Set `FIRESTORE_EMULATOR_HOST=localhost:8081` in any terminal that will run the backend.

2. **Install backend dependencies and run the Functions Framework:**
    - **Linux/macOS**
      ```bash
      cd backend
      pip install -r requirements.txt
      export GOOGLE_CLOUD_PROJECT=local-project
      export BUCKET_NAME=receipt-images
      export FIRESTORE_EMULATOR_HOST=localhost:8081
      functions-framework --target=app
      ```

    - **Windows (cmd.exe)**
      ```cmd
      cd backend
      pip install -r requirements.txt
      set GOOGLE_CLOUD_PROJECT=local-project
      set BUCKET_NAME=receipt-images
      set FIRESTORE_EMULATOR_HOST=localhost:8081
      functions-framework --target=app
      ```

    - **Windows PowerShell**
      ```powershell
      cd backend
      pip install -r requirements.txt
      $env:GOOGLE_CLOUD_PROJECT="local-project"
      $env:BUCKET_NAME="receipt-images"
      $env:FIRESTORE_EMULATOR_HOST="localhost:8081"
      functions-framework --target=app
      ```

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

### Troubleshooting

If the React app shows `AxiosError: Network Error`, make sure the backend is
running and that the environment variable `FIRESTORE_EMULATOR_HOST` is set in the
terminal where you launched the functions framework. Without this variable the
backend will exit with a `DefaultCredentialsError` and the API will be
unreachable.

Receipts created in the UI are stored in the Firestore emulator. Cloud Storage can be emulated locally in a similar manner if needed.

## Running with Docker Compose

As an alternative to running services manually, you can launch the backend and Firestore emulator together:

```bash
docker-compose up
```

The backend will be available on `http://localhost:8080` and the emulator on port `8081`. Environment variables like `FIRESTORE_EMULATOR_HOST` are set automatically. Use `docker-compose down` to stop all containers.

Note: Docker Compose v2 ignores the `version` field, so it has been removed from `docker-compose.yml`.

If you see an error such as `Bind for 0.0.0.0:8081 failed: port is already allocated`, another process is already using that port. Stop the other process or change the port mapping in `docker-compose.yml` before running `docker-compose up` again.
