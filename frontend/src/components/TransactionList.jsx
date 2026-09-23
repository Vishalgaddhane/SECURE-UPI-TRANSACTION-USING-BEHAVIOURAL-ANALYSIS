import { useEffect, useState } from 'react';
import { getAllTransactions } from '../services/transactionApi';

export default function TransactionList({ refreshTrigger }) {
  const [transactions, setTransactions] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function loadTransactions() {
    setLoading(true);
    setError(null);
    try {
      const data = await getAllTransactions();
      setTransactions(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTransactions();
  }, [refreshTrigger]);

  return (
    <div style={{ maxWidth: '900px', margin: '40px auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>All Transactions</h2>
        <button onClick={loadTransactions} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {transactions.length === 0 && !loading && !error && (
        <p>No transactions yet.</p>
      )}

      {transactions.length > 0 && (
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #ccc', textAlign: 'left' }}>
              <th>ID</th>
              <th>User</th>
              <th>Amount</th>
              <th>Merchant</th>
              <th>Risk Level</th>
              <th>Flagged</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((t) => (
              <tr key={t.id} style={{ borderBottom: '1px solid #eee' }}>
                <td>{t.id}</td>
                <td>{t.userId}</td>
                <td>{t.amount}</td>
                <td>{t.merchant}</td>
                <td>{t.riskLevel}</td>
                <td>{t.isFlagged ? '⚠️ Yes' : 'No'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
