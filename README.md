# Paper Operations Management Tool (MVP)

This project demonstrates a minimal local-first setup for managing data entry and paper operations. It contains a Python backend built with Google Cloud Functions Framework and a React frontend.

## Requirements
- Python 3.9+
- Node.js 16+
- Docker (for Firestore emulator)

## Local Setup

1. **Start the Firestore emulator** (leave this terminal running):
    ```bash
    docker run --rm -it -p 8081:8080 google/cloud-sdk:emulators \
      gcloud beta emulators firestore start --host-port=0.0.0.0:8080
    ```

2. **Install backend dependencies and run the Functions Framework:**
    ```bash
    cd backend
    pip install -r requirements.txt
    export GOOGLE_CLOUD_PROJECT=local-project
    export BUCKET_NAME=receipt-images
    functions-framework --target=create_receipt
    ```
    Other function targets can be launched in separate terminals using the same command with a different `--target` value.

3. **Install frontend dependencies and start the React app:**
    ```bash
    cd ../frontend
    npm install
    REACT_APP_API_BASE=http://localhost:8080 npm start
    ```
    The development server runs at <http://localhost:3000>.

4. **Verify the API** (optional example using `curl`):
    ```bash
    curl http://localhost:8080/receipts
    ```

Receipts created in the UI are stored in the Firestore emulator. Cloud Storage can be emulated locally in a similar manner if needed.
