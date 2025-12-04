import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export function parseSchedule(text) {
  return api.post('/api/schedule/parse', { text }).then(res => res.data);
}