import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:8000' });

export function setAuthToken(token){
  if (token) {
    localStorage.setItem('token', token);
    API.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    localStorage.removeItem('token');
    delete API.defaults.headers.common['Authorization'];
  }
}

export function getToken(){ return localStorage.getItem('token'); }

// Initialize interceptor
const token = getToken();
if (token) setAuthToken(token);

export default API;
