# Paper Operations Management Tool (MVP)

This project demonstrates a minimal local-first setup for managing data entry and paper operations. It contains a Python backend built with Google Cloud Functions Framework and a React frontend.

## Requirements
- Python 3.9+
- Node.js 16+

## Local Setup
1. Install Python dependencies:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```
2. Install frontend dependencies and start the UI:
    ```bash
    cd ../frontend
    npm install
    npm start
    ```
3. Start the Cloud Functions locally:
    ```bash
    export BUCKET_NAME=receipt-images
    functions-framework --target=create_receipt --debug
    ```
   Launch other function targets similarly or adjust routing with a framework like Flask in future iterations.

Firestore and Cloud Storage can be emulated locally using Docker.
