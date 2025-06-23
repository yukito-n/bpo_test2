import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8080';

export const createReceipt = (data) => {
  return axios.post(`${API_BASE}/receipts`, data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

export const fetchReceipts = (params) => {
  return axios.get(`${API_BASE}/receipts`, { params });
};

export const fetchReceipt = (id) => {
  return axios.get(`${API_BASE}/receipts/${id}`);
};

export const updateReceipt = (id, data) => {
  return axios.put(`${API_BASE}/receipts/${id}`, data);
};

export const fetchSummary = () => {
  return axios.get(`${API_BASE}/reports/summary`);
};
