// Remover importação não utilizada
import axios from 'axios';
const axiosInstance = axios.create({
  baseURL: 'http://192.168.1.5:8000', // URL exata do backend
  withCredentials: true, // Importante para cookies CSRF
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Contador para monitorar requisições em andamento
 * Útil para mostrar/esconder indicadores de carregamento global
 */
let pendingRequests = 0;

// Interceptor para adicionar token de autenticação e contar requisições ativas
axiosInstance.interceptors.request.use(
  (config) => {
    // Adicionar token de autenticação se disponível
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // Incrementar contador de requisições pendentes
    pendingRequests++;
    document.dispatchEvent(
      new CustomEvent('requestStatusChange', {
        detail: { pending: pendingRequests }
      })
    );
    return config;
  },
  (error) => {
    pendingRequests = Math.max(0, pendingRequests - 1);
    document.dispatchEvent(
      new CustomEvent('requestStatusChange', {
        detail: { pending: pendingRequests }
      })
    );
    return Promise.reject(error);
  }
);

// Interceptor para tratamento de respostas e erros
axiosInstance.interceptors.response.use(
  (response) => {
    // Decrementar contador de requisições pendentes
    pendingRequests = Math.max(0, pendingRequests - 1);
    document.dispatchEvent(
      new CustomEvent('requestStatusChange', {
        detail: { pending: pendingRequests }
      })
    );
    return response;
  },
  (error) => {
    // Decrementar contador de requisições pendentes
    pendingRequests = Math.max(0, pendingRequests - 1);
    document.dispatchEvent(
      new CustomEvent('requestStatusChange', {
        detail: { pending: pendingRequests }
      })
    );
    // Tratamento centralizado de erros
    handleApiError(error);
    return Promise.reject(error);
  }
);

/**
 * Tratamento centralizado de erros da API
 * @param {Error} error - Objeto de erro do Axios
 */
const handleApiError = (error) => {
  // Verificar se é um erro de timeout
  if (error.code === 'ECONNABORTED') {
    console.error('Timeout na requisição:', error.config.url);
  }
  // Obter dados de resposta se disponíveis
  const response = error.response;
  if (response) {
    // Tratar erros específicos por código de status
    switch (response.status) {
      case 401:
        // Erro de autenticação - token expirado ou inválido
        console.warn('Sessão expirada ou token inválido');
        // Se não estiver na página de login, redirecionar
        if (!window.location.pathname.includes('/login')) {
          // Eventos para autenticar novamente o usuário
          document.dispatchEvent(new Event('auth:sessionExpired'));
        }
        break;
      case 403:
        // Erro de permissão
        console.warn('Permissão negada para esta operação');
        document.dispatchEvent(new Event('auth:permissionDenied'));
        break;
      case 404:
        // Recurso não encontrado
        console.warn('Recurso não encontrado:', response.config.url);
        break;
      case 422:
        // Erro de validação
        console.warn('Erro de validação:', response.data);
        break;
      case 429:
        // Rate limiting
        console.warn('Muitas requisições. Tente novamente em alguns instantes.');
        break;
      case 500:
      case 502:
      case 503:
      case 504:
        // Erros de servidor
        console.error('Erro no servidor:', response.status, response.data);
        document.dispatchEvent(new Event('api:serverError'));
        break;
    }
  } else if (error.request) {
    // Requisição enviada mas sem resposta (problemas de rede)
    console.error('Erro de conexão. Verifique sua internet.');
    document.dispatchEvent(new Event('api:connectionError'));
  } else {
    // Erro ao configurar a requisição
    console.error('Erro ao configurar requisição:', error.message);
  }
};

/**
 * Obtém o número atual de requisições pendentes
 * @returns {number} Número de requisições pendentes
 */
const getPendingRequestsCount = () => pendingRequests;

/**
 * Adiciona um listener para mudanças no status de requisições
 * @param {Function} callback - Função a ser chamada quando o status mudar
 */
const addRequestStatusListener = (callback) => {
  document.addEventListener('requestStatusChange', (event) => {
    callback(event.detail.pending);
  });
};

/**
 * Remove um listener de status de requisições
 * @param {Function} callback - Função de callback a ser removida
 */
const removeRequestStatusListener = (callback) => {
  document.removeEventListener('requestStatusChange', callback);
};

// Serviço que encapsula as chamadas do axios
const axiosService = {
  // Métodos HTTP básicos
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
  },
  // Métodos para gerenciamento de requisições
  getPendingRequestsCount,
  addRequestStatusListener,
  removeRequestStatusListener
};

export { axiosInstance };
export default axiosService; 