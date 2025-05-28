// Remover importação não utilizada
import axios from 'axios';
import { getCsrfToken, ensureCsrfToken } from '@/utils/securityService';

const axiosInstance = axios.create({
  baseURL: 'http://192.168.1.5:8000', // URL exata do backend
  withCredentials: true, // Importante para cookies CSRF
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  }
});

/**
 * Contador para monitorar requisições em andamento
 * Útil para mostrar/esconder indicadores de carregamento global
 */
let pendingRequests = 0;

/**
 * Fila de requisições esperando renovação do token CSRF
 */
let csrfPendingRequests = [];
let isRefreshingCsrf = false;

/**
 * Obtém um novo token CSRF e reprocessa as requisições pendentes
 */
const refreshCsrfToken = async () => {
  if (isRefreshingCsrf) return;
  
  isRefreshingCsrf = true;
  try {
    const token = await ensureCsrfToken();
    
    // Se conseguimos um novo token, reprocessamos as requisições pendentes
    if (token) {
      // Processa todas as requisições pendentes
      csrfPendingRequests.forEach(({ resolve, config }) => {
        config.headers['X-CSRF-Token'] = token;
        resolve(axiosInstance(config));
      });
    } else {
      // Se falhou, rejeita todas as requisições pendentes
      csrfPendingRequests.forEach(({ reject }) => {
        reject(new Error('Falha ao renovar token CSRF'));
      });
    }
    
    // Limpa a fila
    csrfPendingRequests = [];
  } catch (error) {
    // Em caso de erro, rejeita todas as requisições pendentes
    csrfPendingRequests.forEach(({ reject }) => {
      reject(error);
    });
    csrfPendingRequests = [];
  } finally {
    isRefreshingCsrf = false;
  }
};

// Interceptor para adicionar token de autenticação e contar requisições ativas
axiosInstance.interceptors.request.use(
  async (config) => {
    // Adicionar token de autenticação se disponível
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Lista de endpoints isentos de CSRF
    const csrfExemptPaths = ['/token', '/security/csrf-token', '/usuarios/'];
    const isExemptPath = csrfExemptPaths.some(path => config.url.includes(path));
    
    console.log(`Requisição ${config.method.toUpperCase()} para ${config.url} - Isento de CSRF: ${isExemptPath}`);
    
    // Adicionar token CSRF para métodos que modificam dados (exceto endpoints isentos)
    if (['post', 'put', 'delete'].includes(config.method.toLowerCase()) && !isExemptPath) {
      const csrfToken = getCsrfToken();
      if (csrfToken) {
        config.headers['X-CSRF-Token'] = csrfToken;
        console.log('Token CSRF adicionado à requisição:', csrfToken.substring(0, 20) + '...');
      } else {
        console.warn('Token CSRF não encontrado. Renovando token...');
        
        // Se estamos em processo de renovação, coloca na fila
        if (isRefreshingCsrf) {
          return new Promise((resolve, reject) => {
            csrfPendingRequests.push({ resolve, reject, config });
          });
        }
        
        // Senão, inicia o processo de renovação
        try {
          const newToken = await ensureCsrfToken();
          if (newToken) {
            config.headers['X-CSRF-Token'] = newToken;
            console.log('Novo token CSRF obtido e adicionado:', newToken.substring(0, 20) + '...');
          } else {
            console.error('Não foi possível obter um token CSRF válido.');
          }
        } catch (error) {
          console.error('Erro ao renovar token CSRF:', error);
        }
      }
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
  async (error) => {
    // Decrementar contador de requisições pendentes
    pendingRequests = Math.max(0, pendingRequests - 1);
    document.dispatchEvent(
      new CustomEvent('requestStatusChange', {
        detail: { pending: pendingRequests }
      })
    );
    
    // Se o erro for de CSRF (403), tentamos renovar o token e reenviar a requisição
    if (error.response && error.response.status === 403 && 
        error.response.data && error.response.data.detail && 
        (error.response.data.detail.includes('CSRF token') || 
         error.response.data.detail.includes('csrf'))) {
      
      // Se não estamos já tentando renovar o token
      if (!isRefreshingCsrf) {
        try {
          // Renovar token CSRF
          await refreshCsrfToken();
          
          // Reenviar a requisição com o novo token
          const csrfToken = getCsrfToken();
          if (csrfToken) {
            error.config.headers['X-CSRF-Token'] = csrfToken;
            return axiosInstance(error.config);
          }
        } catch (refreshError) {
          console.error('Erro ao renovar token CSRF após falha 403:', refreshError);
        }
      } else {
        // Se já estamos renovando, coloca na fila
        return new Promise((resolve, reject) => {
          csrfPendingRequests.push({ 
            resolve, 
            reject, 
            config: error.config 
          });
        });
      }
    }
    
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
  get(url, config = {}) {
    return axiosInstance.get(url, config);
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