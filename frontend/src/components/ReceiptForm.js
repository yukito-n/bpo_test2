import React, { useState } from 'react';
import { createReceipt } from '../api';

export default function ReceiptForm({ onCreated }) {
  const [form, setForm] = useState({});
  const [file, setFile] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleFile = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();
    Object.entries(form).forEach(([k, v]) => data.append(k, v));
    if (file) data.append('receiptImageFile', file);
    try {
      await createReceipt(data);
      setForm({});
      setFile(null);
      if (onCreated) onCreated();
    } catch (err) {
      alert('Error creating receipt');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="caseId" placeholder="Case ID" onChange={handleChange} />
      <input name="receiptType" placeholder="Type" onChange={handleChange} />
      <input name="quantity" placeholder="Quantity" onChange={handleChange} />
      <input name="receivedDateTime" placeholder="Received Date" onChange={handleChange} />
      <input name="assignedTo" placeholder="Assigned To" onChange={handleChange} />
      <input name="storageLocation" placeholder="Storage Location" onChange={handleChange} />
      <input type="file" onChange={handleFile} />
      <button type="submit">Save</button>
    </form>
  );
}
