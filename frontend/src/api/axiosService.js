// Importação modificada para evitar o erro de 'module is not defined'
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;

// Configurações padrão
const API_URL = process.env.VUE_APP_API_URL || '';

// Cliente axios configurado
const axiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor para adicionar token de autenticação
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Serviço que encapsula as chamadas do axios
const axiosService = {
  get(url, params = {}, headers = {}) {
    return axiosInstance.get(url, { params, headers });
  },
  
  post(url, data = {}, headers = {}) {
    return axiosInstance.post(url, data, { headers });
  },
  
  put(url, data = {}, headers = {}) {
    return axiosInstance.put(url, data, { headers });
  },
  
  delete(url, headers = {}) {
    return axiosInstance.delete(url, { headers });
  },
  
  // Método para fazer download de arquivos (para relatórios)
  downloadFile(url, params = {}, responseType = 'blob', headers = {}) {
    return axiosInstance.get(url, { 
      params, 
      responseType,
      headers: {
        ...headers,
        // Headers específicos para download de arquivos podem ser adicionados aqui
      }
    });
  }
};

export default axiosService; 