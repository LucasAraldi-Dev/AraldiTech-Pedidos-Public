/**
 * Serviço de Cache
 * 
 * Este módulo fornece funcionalidades para cache de dados,
 * reduzindo requisições desnecessárias ao servidor e melhorando
 * o tempo de resposta da aplicação.
 */

/**
 * Armazenamento em memória para cache
 * @private
 */
const memoryCache = new Map();

/**
 * Configuração padrão do cache
 * @private
 */
const defaultConfig = {
  ttl: 5 * 60 * 1000, // 5 minutos em milissegundos
  maxItems: 100, // Número máximo de itens em cache
};

/**
 * Configuração atual do cache
 * @private
 */
let cacheConfig = { ...defaultConfig };

/**
 * Configura o serviço de cache
 * @param {Object} config - Configurações de cache
 * @param {number} config.ttl - Tempo de vida dos itens em milissegundos
 * @param {number} config.maxItems - Número máximo de itens em cache
 */
export const configureCache = (config = {}) => {
  cacheConfig = { ...defaultConfig, ...config };
};

/**
 * Gera uma chave de cache baseada nos parâmetros
 * @param {string} baseKey - Chave base (geralmente a URL)
 * @param {Object} params - Parâmetros adicionais
 * @returns {string} - Chave de cache
 * @private
 */
const generateCacheKey = (baseKey, params = {}) => {
  if (!params || Object.keys(params).length === 0) {
    return baseKey;
  }
  
  // Ordenar as chaves para garantir consistência
  const sortedParams = Object.keys(params).sort().reduce((obj, key) => {
    obj[key] = params[key];
    return obj;
  }, {});
  
  return `${baseKey}?${JSON.stringify(sortedParams)}`;
};

/**
 * Adiciona um item ao cache
 * @param {string} key - Chave de cache
 * @param {any} data - Dados a serem armazenados
 * @param {Object} options - Opções de cache
 * @param {number} options.ttl - Tempo de vida em milissegundos
 */
export const cacheSet = (key, data, options = {}) => {
  // Limitar o número de itens no cache
  if (memoryCache.size >= cacheConfig.maxItems && !memoryCache.has(key)) {
    // Se o cache estiver cheio, remove o item mais antigo
    const oldestKey = memoryCache.keys().next().value;
    memoryCache.delete(oldestKey);
  }
  
  const ttl = options.ttl || cacheConfig.ttl;
  const expiry = Date.now() + ttl;
  
  memoryCache.set(key, {
    data,
    expiry,
  });
  
  // Agendar remoção automática quando o TTL expirar
  setTimeout(() => {
    const item = memoryCache.get(key);
    if (item && item.expiry === expiry) {
      memoryCache.delete(key);
    }
  }, ttl);
};

/**
 * Obtém um item do cache
 * @param {string} key - Chave de cache
 * @returns {any|null} - Dados armazenados ou null se não encontrado ou expirado
 */
export const cacheGet = (key) => {
  const item = memoryCache.get(key);
  
  if (!item) {
    return null;
  }
  
  // Verificar se o item expirou
  if (item.expiry < Date.now()) {
    memoryCache.delete(key);
    return null;
  }
  
  return item.data;
};

/**
 * Remove um item específico do cache
 * @param {string} key - Chave de cache
 */
export const cacheDelete = (key) => {
  memoryCache.delete(key);
};

/**
 * Remove todos os itens que correspondem a um prefixo de chave
 * @param {string} keyPrefix - Prefixo da chave
 */
export const cacheDeleteByPrefix = (keyPrefix) => {
  for (const key of memoryCache.keys()) {
    if (key.startsWith(keyPrefix)) {
      memoryCache.delete(key);
    }
  }
};

/**
 * Limpa todo o cache
 */
export const cacheClear = () => {
  memoryCache.clear();
};

/**
 * Wrapper para Axios que implementa cache
 * @param {Function} axiosMethod - Método do Axios (get, post, etc)
 * @param {string} url - URL da requisição
 * @param {Object} config - Configuração do Axios
 * @param {Object} cacheOptions - Opções de cache
 * @param {boolean} cacheOptions.enabled - Se o cache está habilitado
 * @param {number} cacheOptions.ttl - Tempo de vida do cache
 * @returns {Promise<any>} - Resposta da requisição
 */
export const cachedRequest = async (
  axiosMethod,
  url,
  config = {},
  cacheOptions = { enabled: true }
) => {
  // Se o cache estiver desabilitado, apenas executa a requisição
  if (!cacheOptions.enabled) {
    return axiosMethod(url, config);
  }
  
  // Gerar a chave de cache
  const cacheKey = generateCacheKey(url, config.params || {});
  
  // Verificar se os dados estão em cache
  const cachedData = cacheGet(cacheKey);
  if (cachedData) {
    return Promise.resolve({ data: cachedData, cached: true });
  }
  
  // Se não estiver em cache, fazer a requisição
  const response = await axiosMethod(url, config);
  
  // Armazenar a resposta no cache
  cacheSet(cacheKey, response.data, {
    ttl: cacheOptions.ttl || cacheConfig.ttl,
  });
  
  return response;
};

/**
 * Estatísticas do cache
 * @returns {Object} - Estatísticas do cache
 */
export const cacheStats = () => {
  const now = Date.now();
  let validItems = 0;
  let expiredItems = 0;
  
  memoryCache.forEach((item) => {
    if (item.expiry >= now) {
      validItems++;
    } else {
      expiredItems++;
    }
  });
  
  return {
    totalItems: memoryCache.size,
    validItems,
    expiredItems,
    maxItems: cacheConfig.maxItems,
    defaultTTL: cacheConfig.ttl,
  };
};

export default {
  configureCache,
  cacheSet,
  cacheGet,
  cacheDelete,
  cacheDeleteByPrefix,
  cacheClear,
  cachedRequest,
  cacheStats,
}; 