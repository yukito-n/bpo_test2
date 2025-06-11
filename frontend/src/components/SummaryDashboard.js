import React, { useEffect, useState } from 'react';
import { fetchSummary } from '../api';

export default function SummaryDashboard() {
  const [summary, setSummary] = useState(null);

  const load = async () => {
    const { data } = await fetchSummary();
    setSummary(data);
  };

  useEffect(() => {
    load();
  }, []);

  if (!summary) return <div>Loading...</div>;

  return (
    <div>
      <h3>Summary</h3>
      <p>Total Receipts: {summary.totalReceipts}</p>
      <h4>Status Counts</h4>
      <ul>
        {Object.entries(summary.statusCounts).map(([k, v]) => (
          <li key={k}>{k}: {v}</li>
        ))}
      </ul>
      <h4>Processed per Assignee</h4>
      <ul>
        {Object.entries(summary.processedPerAssignee).map(([k, v]) => (
          <li key={k}>{k}: {v}</li>
        ))}
      </ul>
    </div>
  );
}
