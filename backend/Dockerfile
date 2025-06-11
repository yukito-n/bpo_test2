FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
ENV GOOGLE_CLOUD_PROJECT=local-project
ENV BUCKET_NAME=receipt-images
CMD ["functions-framework", "--target=create_receipt", "--port", "8080"]
