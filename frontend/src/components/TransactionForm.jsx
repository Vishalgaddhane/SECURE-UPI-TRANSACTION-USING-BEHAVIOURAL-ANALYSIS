import { useState } from 'react';
import { submitTransaction } from '../services/transactionApi';

export default function TransactionForm({ onTransactionSubmitted }) {
  const [formData, setFormData] = useState({
    userId: '',
    amount: '',
    merchant: '',
    transactionType: 'send',
    location: '',
    deviceInfo: 'Web',
  });
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const payload = {
        ...formData,
        amount: parseFloat(formData.amount),
      };
      const response = await submitTransaction(payload);
      setResult(response);
      if (onTransactionSubmitted) {
        onTransactionSubmitted();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto' }}>
      <h2>Submit a Transaction</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <input
          name="userId"
          placeholder="User ID (e.g. user_5)"
          value={formData.userId}
          onChange={handleChange}
          required
        />
        <input
          name="amount"
          type="number"
          step="0.01"
          placeholder="Amount"
          value={formData.amount}
          onChange={handleChange}
          required
        />
        <input
          name="merchant"
          placeholder="Merchant (e.g. Amazon)"
          value={formData.merchant}
          onChange={handleChange}
          required
        />
        <select name="transactionType" value={formData.transactionType} onChange={handleChange}>
          <option value="send">Send</option>
          <option value="receive">Receive</option>
        </select>
        <input
          name="location"
          placeholder="Location (e.g. Mumbai)"
          value={formData.location}
          onChange={handleChange}
          required
        />
        <select name="deviceInfo" value={formData.deviceInfo} onChange={handleChange}>
          <option value="Web">Web</option>
          <option value="Android">Android</option>
          <option value="iOS">iOS</option>
        </select>
        <button type="submit" disabled={loading}>
          {loading ? 'Checking...' : 'Submit Transaction'}
        </button>
      </form>

      {error && (
        <p style={{ color: 'red', marginTop: '15px' }}>Error: {error}</p>
      )}

      {result && (
        <div style={{ marginTop: '20px', padding: '15px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <h3>Result</h3>
          <p><strong>Risk Level:</strong> {result.riskLevel}</p>
          <p><strong>Fraud Probability:</strong> {(result.fraudProbability * 100).toFixed(2)}%</p>
          <p><strong>Flagged:</strong> {result.isFlagged ? 'Yes' : 'No'}</p>
          <p><strong>Explanation:</strong> {result.explanation}</p>
        </div>
      )}
    </div>
  );
}
