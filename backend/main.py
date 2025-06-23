from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import firestore, storage
from google.auth.exceptions import DefaultCredentialsError
import uuid
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

def init_firestore_client():
    if os.environ.get('FIRESTORE_EMULATOR_HOST'):
        project = os.environ.get('GOOGLE_CLOUD_PROJECT', 'local-project')
        return firestore.Client(project=project)
    try:
        return firestore.Client()
    except DefaultCredentialsError as e:
        raise RuntimeError(
            "Firestore credentials not found. Set FIRESTORE_EMULATOR_HOST or configure credentials."
        ) from e

firestore_client = init_firestore_client()

def init_storage_client():
    if os.environ.get('STORAGE_EMULATOR_HOST'):
        project = os.environ.get('GOOGLE_CLOUD_PROJECT', 'local-project')
        return storage.Client(project=project)
    try:
        return storage.Client()
    except DefaultCredentialsError as e:
        raise RuntimeError(
            "Storage credentials not found. Set STORAGE_EMULATOR_HOST or configure credentials."
        ) from e

storage_client = init_storage_client()
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'receipt-images')

@app.route('/receipts', methods=['POST'])
def create_receipt():
    try:
        request_json = request.form if request.form else request.get_json(silent=True)
        if request_json is None:
            return jsonify({'error': 'Invalid request'}), 400
        case_id = request_json.get('caseId')
        receipt_id = request_json.get('receiptId') or str(uuid.uuid4())
        receipt_type = request_json.get('receiptType')
        quantity = request_json.get('quantity')
        received_date = request_json.get('receivedDateTime')
        assigned_to = request_json.get('assignedTo')
        storage_location = request_json.get('storageLocation')
        receipt_image = request.files.get('receiptImageFile') if request.files else None
        data = {
            'caseId': case_id,
            'receiptId': receipt_id,
            'receiptType': receipt_type,
            'quantity': quantity,
            'receivedDateTime': received_date,
            'assignedTo': assigned_to,
            'storageLocation': storage_location,
            'status': 'Received',
            'createdAt': datetime.utcnow().isoformat()
        }
        firestore_client.collection('receipts').document(receipt_id).set(data)
        if receipt_image:
            bucket = storage_client.bucket(BUCKET_NAME)
            blob = bucket.blob(f"{receipt_id}/{receipt_image.filename}")
            blob.upload_from_file(receipt_image.stream, content_type=receipt_image.content_type)
            data['imageUrl'] = blob.public_url
            firestore_client.collection('receipts').document(receipt_id).update({'imageUrl': data['imageUrl']})
        return jsonify({'message': 'Receipt created', 'receiptId': receipt_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/receipts', methods=['GET'])
def list_receipts():
    try:
        case_id = request.args.get('caseId') if request.args else None
        receipts_ref = firestore_client.collection('receipts')
        if case_id:
            query = receipts_ref.where('caseId', '==', case_id)
        else:
            query = receipts_ref
        docs = query.stream()
        receipts = [doc.to_dict() for doc in docs]
        return jsonify(receipts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/receipts/<receipt_id>', methods=['GET'])
def get_receipt(receipt_id):
    if not receipt_id:
        return jsonify({'error': 'Missing receiptId'}), 400
    try:
        doc_ref = firestore_client.collection('receipts').document(receipt_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({'error': 'Receipt not found'}), 404
        return jsonify(doc.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/receipts/<receipt_id>', methods=['PUT'])
def update_receipt(receipt_id):
    if not receipt_id:
        return jsonify({'error': 'Missing receiptId'}), 400
    try:
        request_json = request.get_json(silent=True)
        if not request_json:
            return jsonify({'error': 'Invalid request'}), 400
        update_data = {k: v for k, v in request_json.items() if v is not None}
        firestore_client.collection('receipts').document(receipt_id).update(update_data)
        return jsonify({'message': 'Receipt updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reports/summary', methods=['GET'])
def get_summary_report():
    try:
        receipts_ref = firestore_client.collection('receipts')
        docs = receipts_ref.stream()
        receipts = [d.to_dict() for d in docs]
        total = len(receipts)
        status_count = {}
        assignee_count = {}
        for r in receipts:
            status = r.get('status', 'Unknown')
            status_count[status] = status_count.get(status, 0) + 1
            assignee = r.get('assignedTo') or r.get('currentAssignee')
            if assignee:
                assignee_count[assignee] = assignee_count.get(assignee, 0) + 1
        return jsonify({'totalReceipts': total, 'statusCounts': status_count, 'processedPerAssignee': assignee_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
