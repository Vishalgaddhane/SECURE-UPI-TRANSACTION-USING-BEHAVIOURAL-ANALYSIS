const API_BASE_URL = 'http://localhost:8080/api/v1/transactions';

export async function submitTransaction(transaction) {
  const response = await fetch(API_BASE_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(transaction),
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.message || 'Failed to submit transaction');
  }

  return response.json();
}

export async function getAllTransactions() {
  const response = await fetch(API_BASE_URL);
  if (!response.ok) {
    throw new Error('Failed to fetch transactions');
  }
  return response.json();
}

export async function getFlaggedTransactions() {
  const response = await fetch(`${API_BASE_URL}/flagged`);
  if (!response.ok) {
    throw new Error('Failed to fetch flagged transactions');
  }
  return response.json();
}

export async function getTransactionsByRiskLevel(level) {
  const response = await fetch(`${API_BASE_URL}/risk/${level}`);
  if (!response.ok) {
    throw new Error('Failed to fetch transactions by risk level');
  }
  return response.json();
}

export async function getStats() {
  const response = await fetch(`${API_BASE_URL}/stats`);
  if (!response.ok) {
    throw new Error('Failed to fetch stats');
  }
  return response.json();
}