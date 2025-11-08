/**
 * API client for Smart Parking System
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export const api = {
  baseUrl: API_BASE_URL,
  
  async get(endpoint: string) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    return response.json();
  },
  
  async post(endpoint: string, data: any) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    return response.json();
  },
  
  async postFormData(endpoint: string, formData: FormData) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    return response.json();
  },
};

// Auth endpoints
export const authApi = {
  register: (data: { email: string; password: string; full_name: string; phone_number: string }) =>
    api.post('/api/v1/auth/register', data),
  
  login: (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    return fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: 'POST',
      body: formData,
    }).then(res => res.json());
  },
};

// Parking lot endpoints
export const parkingLotApi = {
  getAll: () => api.get('/api/v1/parking-lots/'),
  getById: (id: number) => api.get(`/api/v1/parking-lots/${id}`),
  getNearby: (latitude: number, longitude: number, radius: number = 5) =>
    api.get(`/api/v1/parking-lots/nearby?latitude=${latitude}&longitude=${longitude}&radius_km=${radius}`),
};

// Parking slot endpoints
export const parkingSlotApi = {
  getByLotId: (lotId: number) => api.get(`/api/v1/parking-slots/?parking_lot_id=${lotId}`),
};

// Booking endpoints
export const bookingApi = {
  getAll: (token: string) => fetch(`${API_BASE_URL}/api/v1/bookings/`, {
    headers: { Authorization: `Bearer ${token}` },
  }).then(res => res.json()),
  
  create: (data: any, token: string) => fetch(`${API_BASE_URL}/api/v1/bookings/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  }).then(res => res.json()),
};

// AI endpoints
export const aiApi = {
  detectSlots: (parkingLotId: number, image: File) => {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('parking_lot_id', parkingLotId.toString());
    return api.postFormData(`/api/v1/ai/detect-slots?parking_lot_id=${parkingLotId}`, formData);
  },
  
  getSlotStatus: (parkingLotId: number) =>
    api.get(`/api/v1/ai/parking-lot/${parkingLotId}/slots`),
};

