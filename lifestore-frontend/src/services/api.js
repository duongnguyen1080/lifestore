import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5001', 
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
    response => response,
    error => {
      console.error('API Error:', error);
      if (error.response && error.response.status === 401) {
        // Handle unauthorized access
      }
      return Promise.reject(error);
    }
  );

export default {
  getQuote(question) {
    return apiClient.post('/api/quote', { question });
  },
};