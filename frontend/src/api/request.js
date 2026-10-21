import axios from 'axios'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000 
})

service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request interceptor error:', error)
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 200) {
      ElMessage.error(res.message || 'Request failed, please try again')
      return Promise.reject(new Error(res.message || 'API Error'))
    }
    return res
  },
  error => {
    console.error('Response interceptor error:', error)
    if (error.response && error.response.status === 401) {
      ElMessage.error('Session expired, please log in again')
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else {
      ElMessage.error(error.message || `Request failed with status ${error.response?.status}`)
    }
    return Promise.reject(error)
  }
)

export default service