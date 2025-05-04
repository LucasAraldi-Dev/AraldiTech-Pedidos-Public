import { isTokenValid } from '@/utils/isTokenValid';

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

  // Realiza logout
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    localStorage.removeItem('user');
    localStorage.removeItem('tipo_usuario');
  }
};

export default authService;
