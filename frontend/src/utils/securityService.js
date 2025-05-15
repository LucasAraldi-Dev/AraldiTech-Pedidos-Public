/**
 * Serviço de Segurança Centralizado
 * 
 * Este módulo fornece funções de segurança reutilizáveis para proteger
 * a aplicação contra vulnerabilidades comuns como CSRF, XSS e injeção.
 */

import axiosService, { axiosInstance } from '../api/axiosService';

const CSRF_TOKEN_KEY = 'csrf_token';

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
 * Obtém o token CSRF atual
 * @returns {string|null} - Token CSRF ou null se não estiver inicializado
 */
export function getCsrfToken() {
  return localStorage.getItem(CSRF_TOKEN_KEY);
}

/**
 * Garantir que temos um token CSRF válido antes de operações protegidas
 * @returns {Promise<string>} Token CSRF
 */
export async function ensureCsrfToken() {
  // Verificar se já existe um token
  const existingToken = getCsrfToken();
  if (existingToken) {
    return existingToken;
  }
  
  // Se não existir, inicializar
  return initCsrfProtection();
}

/**
 * Sanitiza texto para prevenir ataques XSS
 * @param {string} input - Texto a ser sanitizado
 * @returns {string} - Texto sanitizado
 */
export const sanitizeHtml = (input) => {
  if (!input) return '';
  
  return String(input)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
};

/**
 * Valida um objeto inteiro contra regras de validação
 * @param {Object} data - Objeto a ser validado
 * @param {Object} rules - Regras de validação
 * @returns {Object} - Resultado da validação {isValid, errors}
 */
export const validateObject = (data, rules) => {
  const result = {
    isValid: true,
    errors: {}
  };
  
  // Verificar cada campo conforme as regras definidas
  Object.keys(rules).forEach(field => {
    const fieldRules = rules[field];
    const value = data[field];
    
    // Verificar se o campo é obrigatório
    if (fieldRules.required && (value === undefined || value === null || value === '')) {
      result.isValid = false;
      result.errors[field] = 'Este campo é obrigatório';
      return;
    }
    
    // Verificar padrão (regex)
    if (fieldRules.pattern && value) {
      const regex = new RegExp(fieldRules.pattern);
      if (!regex.test(value)) {
        result.isValid = false;
        result.errors[field] = fieldRules.patternMessage || 'Formato inválido';
        return;
      }
    }
    
    // Verificar comprimento mínimo
    if (fieldRules.minLength && value && value.length < fieldRules.minLength) {
      result.isValid = false;
      result.errors[field] = `Deve ter pelo menos ${fieldRules.minLength} caracteres`;
      return;
    }
    
    // Verificar comprimento máximo
    if (fieldRules.maxLength && value && value.length > fieldRules.maxLength) {
      result.isValid = false;
      result.errors[field] = `Deve ter no máximo ${fieldRules.maxLength} caracteres`;
      return;
    }
    
    // Verificar valor mínimo (para números)
    if (fieldRules.min !== undefined && value !== undefined && value < fieldRules.min) {
      result.isValid = false;
      result.errors[field] = `Deve ser maior ou igual a ${fieldRules.min}`;
      return;
    }
    
    // Verificar valor máximo (para números)
    if (fieldRules.max !== undefined && value !== undefined && value > fieldRules.max) {
      result.isValid = false;
      result.errors[field] = `Deve ser menor ou igual a ${fieldRules.max}`;
      return;
    }
    
    // Verificação personalizada
    if (fieldRules.custom && typeof fieldRules.custom === 'function') {
      const customResult = fieldRules.custom(value, data);
      if (customResult !== true) {
        result.isValid = false;
        result.errors[field] = customResult || 'Valor inválido';
        return;
      }
    }
  });
  
  return result;
};

/**
 * Detecta potenciais tentativas de injeção de script
 * @param {string} input - Texto a ser verificado
 * @returns {boolean} - true se parecer uma tentativa de injeção
 */
export const detectScriptInjection = (input) => {
  if (!input || typeof input !== 'string') return false;
  
  // Padrões comuns de injeção de scripts
  const suspiciousPatterns = [
    /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/i,
    /javascript:/i,
    /on\w+\s*=/i,
    /document\.cookie/i,
    /\balert\s*\(/i,
    /\beval\s*\(/i
  ];
  
  return suspiciousPatterns.some(pattern => pattern.test(input));
};

/**
 * Detecta potenciais tentativas de injeção SQL
 * @param {string} input - Texto a ser verificado
 * @returns {boolean} - true se parecer uma tentativa de injeção SQL
 */
export const detectSqlInjection = (input) => {
  if (!input || typeof input !== 'string') return false;
  
  // Padrões comuns de injeção SQL
  const suspiciousPatterns = [
    /\b(union|select|insert|update|delete|drop|alter)\b/i,
    /['"].*?--/i,
    /\bor\s+[\d'"]+=\s*[\d'"]+/i,
    /;\s*\w+/i
  ];
  
  return suspiciousPatterns.some(pattern => pattern.test(input));
};

/**
 * Verifica a força de uma senha
 * @param {string} password - Senha a ser verificada
 * @returns {Object} - Resultado {score, feedback}
 */
export const checkPasswordStrength = (password) => {
  if (!password) {
    return { score: 0, feedback: 'Senha não fornecida' };
  }
  
  let score = 0;
  const feedback = [];
  
  // Verificar comprimento
  if (password.length < 8) {
    feedback.push('A senha deve ter pelo menos 8 caracteres');
  } else {
    score += 1;
  }
  
  // Verificar presença de letras minúsculas
  if (/[a-z]/.test(password)) {
    score += 1;
  } else {
    feedback.push('Inclua pelo menos uma letra minúscula');
  }
  
  // Verificar presença de letras maiúsculas
  if (/[A-Z]/.test(password)) {
    score += 1;
  } else {
    feedback.push('Inclua pelo menos uma letra maiúscula');
  }
  
  // Verificar presença de números
  if (/\d/.test(password)) {
    score += 1;
  } else {
    feedback.push('Inclua pelo menos um número');
  }
  
  // Verificar presença de caracteres especiais
  if (/[^A-Za-z0-9]/.test(password)) {
    score += 1;
  } else {
    feedback.push('Inclua pelo menos um caractere especial');
  }
  
  return {
    score, // 0-5, onde 5 é a mais forte
    feedback: feedback.join('; ') || 'Senha forte'
  };
};

// Interceptor para adicionar CSRF em métodos sensíveis
axiosInstance.interceptors.request.use(config => {
  const method = config.method && config.method.toUpperCase();
  if (["POST", "PUT", "DELETE"].includes(method)) {
    const csrfToken = getCsrfToken();
    if (csrfToken) {
      console.log(`Adicionando token CSRF para ${method} ${config.url}`);
      config.headers['X-CSRF-Token'] = csrfToken;
    } else {
      console.warn(`AVISO: Token CSRF não encontrado para ${method} ${config.url}`);
    }
  }
  return config;
});

export default {
  initCsrfProtection,
  getCsrfToken,
  sanitizeHtml,
  validateObject,
  detectScriptInjection,
  detectSqlInjection,
  checkPasswordStrength
}; 