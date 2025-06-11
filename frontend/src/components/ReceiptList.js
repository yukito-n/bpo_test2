import React, { useEffect, useState } from 'react';
import { fetchReceipts } from '../api';

export default function ReceiptList({ onSelect }) {
  const [receipts, setReceipts] = useState([]);

  const load = async () => {
    const { data } = await fetchReceipts();
    setReceipts(data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>Receipt ID</th>
          <th>Case ID</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {receipts.map((r) => (
          <tr key={r.receiptId} onClick={() => onSelect && onSelect(r.receiptId)}>
            <td>{r.receiptId}</td>
            <td>{r.caseId}</td>
            <td>{r.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
