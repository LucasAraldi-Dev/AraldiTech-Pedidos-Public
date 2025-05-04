import authService from '@/api/authService';
import { useToast } from 'vue-toastification';

/**
 * Serviço para gerenciar autenticação em modais
 */
const modalAuthService = {
  /**
   * Verifica se o usuário está autenticado antes de abrir um modal
   * @param {Function} openModalCallback - Função de callback para abrir o modal se autenticado
   * @param {Object} options - Opções adicionais
   * @param {boolean} options.requiresAdmin - Se o modal requer privilégios de administrador
   * @param {string} options.errorMessage - Mensagem de erro personalizada
   * @returns {Promise<boolean>} - Verdadeiro se a autenticação for bem-sucedida
   */
  async verifyAuthBeforeOpenModal(openModalCallback, options = {}) {
    const toast = useToast();
    const { requiresAdmin = false, errorMessage } = options;
    
    // Verifica se há uma sessão de login ativa no sessionStorage
    const isLoggedInFromSession = sessionStorage.getItem('isLoggedIn') === 'true';
    const userFromSession = sessionStorage.getItem('user') ? JSON.parse(sessionStorage.getItem('user')) : null;
    const csrfTokenFromSession = sessionStorage.getItem('csrfToken');
    
    // Se tiver sessão ativa e não precisar de privilégios de admin (ou tiver os privilégios)
    if (isLoggedInFromSession && (!requiresAdmin || (userFromSession && userFromSession.tipo_usuario === 'admin'))) {
      // Recupera dados de usuário e token CSRF da sessão para authService
      if (userFromSession && !authService.userData) {
        authService.userData = userFromSession;
      }
      
      // Recuperar o token CSRF se necessário
      if (csrfTokenFromSession && !authService.csrfToken) {
        authService.csrfToken = csrfTokenFromSession;
      }
      
      // Se todas as verificações passarem, chama o callback para abrir o modal
      if (typeof openModalCallback === 'function') {
        openModalCallback();
      }
      
      return true;
    }
    
    // Verifica se o usuário está autenticado no authService
    if (!authService.isAuthenticated()) {
      toast.error(errorMessage || 'Você precisa estar logado para acessar esta funcionalidade');
      return false;
    }
    
    // Verifica se o token é válido
    try {
      const user = await authService.validateToken();
      if (!user) {
        toast.error('Sua sessão expirou. Por favor, faça login novamente.');
        sessionStorage.removeItem('isLoggedIn');
        sessionStorage.removeItem('user');
        sessionStorage.removeItem('csrfToken');
        return false;
      }
      
      // Garante que temos os dados mais recentes no sessionStorage
      sessionStorage.setItem('isLoggedIn', 'true');
      sessionStorage.setItem('user', JSON.stringify(user));
      
      // Salvar token CSRF na sessão se disponível
      if (authService.csrfToken) {
        sessionStorage.setItem('csrfToken', authService.csrfToken);
      }
      
      // Verifica se o usuário tem permissões de administrador, se necessário
      if (requiresAdmin && !authService.isAdmin()) {
        toast.error(errorMessage || 'Acesso restrito a administradores');
        return false;
      }
      
      // Se todas as verificações passarem, chama o callback para abrir o modal
      if (typeof openModalCallback === 'function') {
        openModalCallback();
      }
      
      return true;
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error);
      toast.error('Erro ao verificar autenticação. Por favor, faça login novamente.');
      return false;
    }
  }
};

export default modalAuthService;