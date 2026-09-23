import { useEffect, useState } from 'react';
import { getAllTransactions, getFlaggedTransactions, getTransactionsByRiskLevel, getStats } from '../services/transactionApi';

const FILTERS = ['All', 'Flagged', 'Low', 'Medium', 'High'];

const CARD_STYLE = {
  flex: 1,
  padding: '16px',
  borderRadius: '8px',
  textAlign: 'center',
  border: '1px solid #e5e7eb',
};

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [activeFilter, setActiveFilter] = useState('All');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function loadStats() {
    try {
      const data = await getStats();
      setStats(data);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadTransactions(filter) {
    setLoading(true);
    setError(null);
    try {
      let data;
      if (filter === 'All') {
        data = await getAllTransactions();
      } else if (filter === 'Flagged') {
        data = await getFlaggedTransactions();
      } else {
        data = await getTransactionsByRiskLevel(filter);
      }
      setTransactions(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleFilterClick(filter) {
    setActiveFilter(filter);
    loadTransactions(filter);
  }

  useEffect(() => {
    loadStats();
    loadTransactions('All');
  }, []);

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '20px' }}>
      <h1 style={{ textAlign: 'center' }}>Fraud Monitoring Dashboard</h1>

      {stats && (
        <div style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
          <div style={{ ...CARD_STYLE, background: '#f3f4f6' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{stats.total}</div>
            <div>Total</div>
          </div>
          <div style={{ ...CARD_STYLE, background: '#dcfce7' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{stats.lowCount}</div>
            <div>Low Risk</div>
          </div>
          <div style={{ ...CARD_STYLE, background: '#fef3c7' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{stats.mediumCount}</div>
            <div>Medium Risk</div>
          </div>
          <div style={{ ...CARD_STYLE, background: '#fee2e2' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{stats.highCount}</div>
            <div>High Risk</div>
          </div>
          <div style={{ ...CARD_STYLE, background: '#fee2e2' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{stats.flaggedCount}</div>
            <div>Flagged</div>
          </div>
        </div>
      )}

      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        {FILTERS.map((filter) => (
          <button
            key={filter}
            onClick={() => handleFilterClick(filter)}
            style={{
              padding: '8px 16px',
              borderRadius: '6px',
              border: activeFilter === filter ? '2px solid #333' : '1px solid #ccc',
              background: activeFilter === filter ? '#333' : 'white',
              color: activeFilter === filter ? 'white' : 'black',
              cursor: 'pointer',
            }}
          >
            {filter}
          </button>
        ))}
      </div>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {loading && <p>Loading...</p>}

      {!loading && transactions.length === 0 && !error && (
        <p>No transactions match this filter.</p>
      )}

      {!loading && transactions.length > 0 && (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #ccc', textAlign: 'left' }}>
              <th>ID</th>
              <th>User</th>
              <th>Amount</th>
              <th>Merchant</th>
              <th>Risk Level</th>
              <th>Action</th>
              <th>Time</th>
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
                <td>{t.securityAction}</td>
                <td>{t.transactionTime}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
