import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

const unwrap = (request) => request.then((response) => response.data);

export const hospitalAPI = {
  list: (params) => unwrap(api.get('/hospitals', { params })),
  search: (params) => unwrap(api.get('/hospitals/search', { params })),
  detail: (id) => unwrap(api.get(`/hospitals/${id}`)),
  availability: (id, params) => unwrap(api.get(`/hospitals/${id}/availability`, { params })),
};

export const doctorAPI = {
  list: (params) => unwrap(api.get('/doctors', { params })),
  detail: (id) => unwrap(api.get(`/doctors/${id}`)),
};

export const roomAPI = {
  list: (params) => unwrap(api.get('/rooms', { params })),
};

export const bookingAPI = {
  create: (data) => unwrap(api.post('/bookings', data)),
  detail: (id) => unwrap(api.get(`/bookings/${id}`)),
  cancel: (id) => unwrap(api.patch(`/bookings/${id}/cancel`)),
};

export default api;
