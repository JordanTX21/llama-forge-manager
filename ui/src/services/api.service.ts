import axios from 'axios'

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Backend base URL
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptores para manejo global de errores
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)
