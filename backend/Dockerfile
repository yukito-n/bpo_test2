FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
ENV GOOGLE_CLOUD_PROJECT=local-project
ENV BUCKET_NAME=receipt-images
ENV FIRESTORE_EMULATOR_HOST=firestore:8080
ENV STORAGE_EMULATOR_HOST=storage:4443
CMD ["functions-framework", "--target=app", "--port", "8080"]
