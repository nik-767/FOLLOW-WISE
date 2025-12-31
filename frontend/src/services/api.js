import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Request interceptor to add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401 Unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized error (e.g., redirect to login)
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: (email, password) => {
    const params = new URLSearchParams();
    // OAuth2PasswordRequestForm expects `username` and `password` fields
    params.append('username', email);
    params.append('password', password);

    return api.post('/auth/login', params.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  
  register: (userData) => 
    api.post('/auth/register', userData),
  
  getMe: () => 
    api.get('/auth/me'),
};

// Leads API
export const leadsApi = {
  getLeads: (params = {}) => 
    api.get('/leads', { params }),
    
  getLead: (id) => 
    api.get(`/leads/${id}`),
    
  createLead: (leadData) => 
    api.post('/leads', leadData),
    
  updateLead: (id, leadData) => 
    api.patch(`/leads/${id}`, leadData),
    
  deleteLead: (id) => 
    api.delete(`/leads/${id}`),
    
  generateFollowups: (leadId, data) => 
    api.post(`/leads/${leadId}/generate-followups`, data),
    
  getFollowups: (leadId) => 
    api.get(`/leads/${leadId}/followups`),
    
  sendEmail: (leadId, emailData) => 
    api.post(`/leads/${leadId}/send-email`, emailData),
    
  getSentEmails: (leadId, params = {}) => 
    api.get(`/leads/${leadId}/sent-emails`, { params }),
    
  scanInbox: () => 
    api.post('/leads/scan-inbox'),
};

// User API
export const userApi = {
  updateProfile: (userData) => 
    api.patch('/users/me', userData),
    
  changePassword: (currentPassword, newPassword) => 
    api.post('/users/me/change-password', { current_password: currentPassword, new_password: newPassword }),
};

// Add this inside your export object, maybe create a new 'emailsApi' object
export const emailsApi = {
  getAllSentEmails: (params = {}) => 
    api.get('/sent-emails', { params }),
};
export default api;
