import { useState } from 'react';
import TransactionForm from './components/TransactionForm';
import TransactionList from './components/TransactionList';
import AdminDashboard from './pages/AdminDashboard';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [view, setView] = useState('submit');

  function handleTransactionSubmitted() {
    setRefreshTrigger((prev) => prev + 1);
  }

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '20px' }}>
      <h1 style={{ textAlign: 'center' }}>Secure UPI Fraud Detection</h1>

      <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginBottom: '20px' }}>
        <button onClick={() => setView('submit')} disabled={view === 'submit'}>
          Submit Transaction
        </button>
        <button onClick={() => setView('dashboard')} disabled={view === 'dashboard'}>
          Admin Dashboard
        </button>
      </div>

      {view === 'submit' && (
        <>
          <TransactionForm onTransactionSubmitted={handleTransactionSubmitted} />
          <TransactionList refreshTrigger={refreshTrigger} />
        </>
      )}

      {view === 'dashboard' && <AdminDashboard />}
    </div>
  );
}

export default App;
