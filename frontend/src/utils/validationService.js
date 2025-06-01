/**
 * Serviço de Validação Centralizado
 * 
 * Este módulo fornece funções de validação reutilizáveis para formulários
 * e padroniza as mensagens de erro em toda a aplicação.
 */

/**
 * Valida quantidade de produtos
 * @param {number} quantity - Quantidade a ser validada
 * @returns {Object} Objeto com status de validação e mensagem de erro
 */
export const validateQuantity = (quantity) => {
  if (quantity === null || quantity === undefined || isNaN(quantity)) {
    return {
      isValid: false,
      message: "A quantidade deve ser um número válido."
    };
  }
  
  if (quantity <= 0) {
    return {
      isValid: false,
      message: "A quantidade deve ser maior que zero."
    };
  }
  
  return {
    isValid: true,
    message: ""
  };
};

/**
 * Valida valores monetários
 * @param {number} value - Valor monetário a ser validado
 * @param {boolean} required - Se o campo é obrigatório
 * @returns {Object} Objeto com status de validação e mensagem de erro
 */
export const validateMonetaryValue = (value, required = false) => {
  // Se não for obrigatório e estiver vazio, é válido
  if (!required && (value === null || value === undefined || value === "")) {
    return {
      isValid: true,
      message: ""
    };
  }
  
  if (value === null || value === undefined || isNaN(value)) {
    return {
      isValid: false,
      message: "O valor deve ser um número válido."
    };
  }
  
  if (value < 0) {
    return {
      isValid: false,
      message: "O valor não pode ser negativo."
    };
  }
  
  return {
    isValid: true,
    message: ""
  };
};

/**
 * Valida datas
 * @param {string} dateStr - Data em formato string (YYYY-MM-DD)
 * @param {Object} options - Opções adicionais
 * @returns {Object} Objeto com status de validação e mensagem de erro
 */
export const validateDate = (dateStr, options = {}) => {
  const { 
    required = true,
    minDate = null,
    maxDate = null,
    allowPastDates = true
  } = options;
  
  // Se não for obrigatório e estiver vazio, é válido
  if (!required && (!dateStr || dateStr.trim() === "")) {
    return {
      isValid: true,
      message: ""
    };
  }
  
  // Verifica se é uma data válida
  if (!dateStr || !/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
    return {
      isValid: false,
      message: "Formato de data inválido. Use AAAA-MM-DD."
    };
  }
  
  const dateObj = new Date(dateStr);
  if (isNaN(dateObj.getTime())) {
    return {
      isValid: false,
      message: "Data inválida."
    };
  }
  
  // Verificação de data mínima
  if (minDate && dateObj < new Date(minDate)) {
    return {
      isValid: false,
      message: `A data não pode ser anterior a ${formatDate(minDate)}.`
    };
  }
  
  // Verificação de data máxima
  if (maxDate && dateObj > new Date(maxDate)) {
    return {
      isValid: false,
      message: `A data não pode ser posterior a ${formatDate(maxDate)}.`
    };
  }
  
  // Verificação de datas passadas
  if (!allowPastDates) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (dateObj < today) {
      return {
        isValid: false,
        message: "A data não pode estar no passado."
      };
    }
  }
  
  return {
    isValid: true,
    message: ""
  };
};

/**
 * Valida texto com requisitos de tamanho
 * @param {string} text - Texto a ser validado
 * @param {Object} options - Opções de validação
 * @returns {Object} Objeto com status de validação e mensagem de erro
 */
export const validateText = (text, options = {}) => {
  const {
    required = true,
    minLength = 0,
    maxLength = null,
    fieldName = "Texto"
  } = options;
  
  // Se não for obrigatório e estiver vazio, é válido
  if (!required && (!text || text.trim() === "")) {
    return {
      isValid: true,
      message: ""
    };
  }
  
  // Verifica se está vazio quando obrigatório
  if (required && (!text || text.trim() === "")) {
    return {
      isValid: false,
      message: `${fieldName} é obrigatório.`
    };
  }
  
  // Verifica comprimento mínimo
  if (minLength > 0 && text.length < minLength) {
    return {
      isValid: false,
      message: `${fieldName} deve ter pelo menos ${minLength} caracteres.`
    };
  }
  
  // Verifica comprimento máximo
  if (maxLength && text.length > maxLength) {
    return {
      isValid: false,
      message: `${fieldName} deve ter no máximo ${maxLength} caracteres.`
    };
  }
  
  return {
    isValid: true,
    message: ""
  };
};

/**
 * Formata uma data para exibição
 * @param {string|Date} date - Data a ser formatada
 * @returns {string} Data formatada no padrão brasileiro
 */
export const formatDate = (date) => {
  if (!date) return '';
  
  const dateObj = date instanceof Date ? date : new Date(date);
  
  if (isNaN(dateObj.getTime())) {
    return 'Data inválida';
  }
  
  return dateObj.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
};

/**
 * Formata um valor monetário para exibição
 * @param {number} value - Valor a ser formatado
 * @returns {string} Valor formatado como moeda brasileira
 */
export const formatCurrency = (value) => {
  if (value === null || value === undefined || isNaN(value)) {
    return 'R$ 0,00';
  }
  
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
};

export default {
  validateQuantity,
  validateMonetaryValue,
  validateDate,
  validateText,
  formatDate,
  formatCurrency
}; 