/**
 * Serviço de Segurança Centralizado
 * 
 * Este módulo fornece funções de segurança reutilizáveis para proteger
 * a aplicação contra vulnerabilidades comuns como CSRF, XSS e injeção.
 */

import axiosService from '@/api/axiosService';

const CSRF_TOKEN_KEY = 'csrf_token';

let csrfToken = null;
// Exportar a constante para uso em outros arquivos
export const CSRF_HEADER_NAME = 'X-CSRF-Token';

/**
 * Inicializa o token CSRF solicitando um novo token do servidor
 * @returns {Promise<string>} - Token CSRF
 */
export async function initCsrfProtection() {
  try {
    const response = await axiosService.get('/security/csrf-token');
    const token = response.data.csrf_token;
    if (token) {
      localStorage.setItem(CSRF_TOKEN_KEY, token);
      return token;
    } else {
      throw new Error('Token CSRF não recebido');
    }
  } catch (error) {
    console.error('Erro ao inicializar proteção CSRF:', error);
    throw new Error('Falha ao inicializar proteção CSRF');
  }
}

/**
 * Obtém o token CSRF atual do armazenamento em memória
 * @returns {string|null} Token CSRF ou null se não existir
 */
export function getCsrfToken() {
  return csrfToken;
}

/**
 * Atualiza o token CSRF chamando a API
 * @param {boolean} [forceRefresh=false] Forçar atualização mesmo se já existir um token
 * @returns {Promise<string|null>} Token CSRF atualizado ou null em caso de erro
 */
export async function ensureCsrfToken(forceRefresh = false) {
  try {
    // Se já temos um token e não estamos forçando atualização, retorna o existente
    if (csrfToken && !forceRefresh) {
      console.log('Usando token CSRF existente');
      return csrfToken;
    }
    
    console.log('Buscando novo token CSRF...');
    
    // Chamar o endpoint para gerar um novo token
    const response = await axiosService.get('/security/csrf-token');
    
    if (response && response.data && response.data.csrf_token) {
      csrfToken = response.data.csrf_token;
      console.log('Token CSRF atualizado com sucesso');
      return csrfToken;
    } else {
      console.error('Resposta inválida do servidor para token CSRF:', response);
      return null;
    }
  } catch (error) {
    console.error('Erro ao obter token CSRF:', error);
    
    // Logs adicionais para diagnóstico
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Dados:', error.response.data);
      console.error('Headers:', error.response.headers);
    } else if (error.request) {
      console.error('Sem resposta do servidor. Requisição:', error.request);
    } else {
      console.error('Erro:', error.message);
    }
    
    return null;
  }
}

/**
 * Sanitiza strings HTML para prevenir ataques XSS
 * @param {string} html String HTML potencialmente perigosa
 * @returns {string} String sanitizada
 */
export function sanitizeHtml(html) {
  if (!html) return '';
  
  // Substituição básica de caracteres especiais
  return String(html)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Verifica a força de uma senha e retorna uma pontuação com feedback
 * @param {string} password A senha a ser verificada
 * @returns {Object} Objeto contendo score (0-4) e feedback para o usuário
 */
export function checkPasswordStrength(password) {
  // Critérios básicos de força de senha
  const criteria = {
    length: password.length >= 8,
    lowercase: /[a-z]/.test(password),
    uppercase: /[A-Z]/.test(password),
    numbers: /[0-9]/.test(password),
    symbols: /[!@#$%^&*(),.?":{}|<>]/.test(password)
  };
  
  // Calcular pontuação com base nos critérios atendidos
  let score = 0;
  let feedback = '';
  
  // Adicionar pontos por cada critério atendido
  if (criteria.length) score++;
  if (criteria.lowercase) score++;
  if (criteria.uppercase) score++;
  if (criteria.numbers) score++;
  if (criteria.symbols) score++;
  
  // Ajustar pontuação para escala 0-4
  score = Math.min(4, Math.floor(score * 0.8));
  
  // Gerar feedback baseado no score
  switch (score) {
    case 0:
      feedback = "Muito fraca. Sua senha é extremamente vulnerável.";
      break;
    case 1:
      feedback = "Fraca. Adicione mais caracteres e varie entre letras, números e símbolos.";
      break;
    case 2:
      feedback = "Razoável. Tente adicionar letras maiúsculas, números ou símbolos.";
      break;
    case 3:
      feedback = "Boa. Sua senha é relativamente segura.";
      break;
    case 4:
      feedback = "Forte. Sua senha atende a todos os critérios de segurança.";
      break;
  }
  
  return { score, feedback };
}

/**
 * Inicializa todas as proteções de segurança necessárias
 * @returns {Promise<boolean>} True se todas as proteções foram inicializadas com sucesso
 */
export async function inicializarProtecoesSeguranca() {
  try {
    // Inicializa a proteção CSRF
    await initCsrfProtection();
    
    // Aqui poderiam ser adicionadas outras inicializações de segurança
    // por exemplo: verificar a versão da API, configurar headers de segurança, etc.
    
    console.log('Todas as proteções de segurança foram inicializadas');
    return true;
  } catch (error) {
    console.error('Falha ao inicializar proteções de segurança:', error);
    return false;
  }
} 