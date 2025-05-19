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
      console.log('Iniciando processo de login para:', username);
      
      // Limpar completamente a sessão anterior
      this.logout();
      console.log('Sessão anterior limpa');
      
      // Limpar qualquer token CSRF e obter um novo
      localStorage.removeItem('csrf_token');
      const csrfToken = await ensureCsrfToken(true);
      console.log('Novo token CSRF obtido:', csrfToken ? 'Sim' : 'Não');
      
      console.log('Enviando requisição de login...');
      const response = await axiosService.post('/token', { username, senha });
      console.log('Resposta recebida do servidor');
      
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
        
        console.log('Login bem-sucedido para usuário:', userData.nome, 'com tipo:', userData.tipo_usuario);
        return { success: true, user: userData };
      }
      
      return { success: false, error: 'Dados inválidos na resposta' };
    } catch (error) {
      console.error('Erro no login:', error);
      let errorMessage = 'Ocorreu um erro durante o login';
      
      if (error.response) {
        // Erro retornado pelo servidor
        errorMessage = error.response.data?.detail || 'Credenciais inválidas';
        console.error('Erro do servidor:', error.response.status, error.response.data);
      } else if (error.request) {
        // Sem resposta do servidor
        errorMessage = 'Erro de conexão com o servidor';
        console.error('Sem resposta do servidor:', error.request);
      }
      
      return { success: false, error: errorMessage };
    }
  },

  // Realiza logout
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    localStorage.removeItem('user');
    localStorage.removeItem('tipo_usuario');
  }
};

export default authService;
