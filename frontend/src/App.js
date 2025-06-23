import React, { useState } from 'react';
import ReceiptForm from './components/ReceiptForm';
import ReceiptList from './components/ReceiptList';
import SummaryDashboard from './components/SummaryDashboard';

function App() {
  const [selected, setSelected] = useState(null);
  const [refresh, setRefresh] = useState(false);

  const handleCreated = () => setRefresh(!refresh);

  return (
    <div className="App">
      <h1>Paper Operations Tool</h1>
      <ReceiptForm onCreated={handleCreated} />
      <ReceiptList key={refresh} onSelect={setSelected} />
      <SummaryDashboard />
    </div>
  );
}

export default App;
