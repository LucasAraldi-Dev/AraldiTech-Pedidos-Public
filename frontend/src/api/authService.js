import { isTokenValid } from '@/utils/isTokenValid';
import { ensureCsrfToken } from '@/utils/securityService';
import axiosService from './axiosService';

const authService = {
  // Obtém o token de autenticação
  getToken() {
    return localStorage.getItem('access_token');
  },

  // Obtém o tipo de token
  getTokenType() {
    return localStorage.getItem('token_type');
  },

  // Obtém os dados do usuário logado
  getUser() {
    const userData = localStorage.getItem('user');
    if (userData) {
      return JSON.parse(userData);
    }
    return null;
  },

  // Verifica se o usuário é administrador
  isAdmin() {
    const user = this.getUser();
    return user && user.tipo_usuario === 'admin';
  },

  // Valida o token com o backend
  async validateToken() {
    return await isTokenValid();
  },

  // Obtém headers de autenticação
  getAuthHeaders() {
    const token = this.getToken();
    if (token) {
      return {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      };
    }
    return {};
  },

  // Realiza o login do usuário
  async login(username, senha) {
    try {
      // Limpar completamente a sessão anterior
      this.logout();
      
      // Limpar qualquer token CSRF e obter um novo
      localStorage.removeItem('csrf_token');
      await ensureCsrfToken(true);
      
      const response = await axiosService.post('/token', { username, senha });
      
      // Armazenar token e informações do usuário
      if (response.data && response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('token_type', response.data.token_type);
        localStorage.setItem('tipo_usuario', response.data.tipo_usuario);
        
        // Armazenar dados do usuário
        const userData = {
          nome: response.data.nome,
          tipo_usuario: response.data.tipo_usuario,
          setor: response.data.setor,
          primeiro_login: response.data.primeiro_login
        };
        localStorage.setItem('user', JSON.stringify(userData));
        
        // Renovar token CSRF após login bem-sucedido
        await ensureCsrfToken(true);
        
        return { success: true, user: userData };
      }
      
      return { success: false, error: 'Dados inválidos na resposta' };
    } catch (error) {
      let errorMessage = 'Ocorreu um erro durante o login';
      
      if (error.response) {
        // Erro retornado pelo servidor
        errorMessage = error.response.data?.detail || 'Credenciais inválidas';
      } else if (error.request) {
        // Sem resposta do servidor
        errorMessage = 'Erro de conexão com o servidor';
      }
      
      return { success: false, error: errorMessage };
    }
  },

  // Realiza logout
  async logout() {
    try {
      // Tenta chamar a API de logout apenas se estiver autenticado
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          await axiosService.post('/auth/logout', {}, {
            headers: { Authorization: `Bearer ${token}` }
          });
        } catch (error) {
          // Continuamos com o logout local mesmo se o servidor falhar
        }
      }
    } finally {
      // Limpa os dados locais independentemente do resultado do servidor
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_type');
      localStorage.removeItem('user');
      localStorage.removeItem('tipo_usuario');
    }
  }
};

export default authService;
