/**
 * Utilitários para teste de upload de arquivos
 */

/**
 * Cria um arquivo de teste para simular upload
 * @param {string} content - Conteúdo do arquivo
 * @param {string} filename - Nome do arquivo
 * @param {string} mimeType - Tipo MIME do arquivo
 * @returns {File} Arquivo de teste
 */
export function createTestFile(content = 'Test file content', filename = 'test.txt', mimeType = 'text/plain') {
  const blob = new Blob([content], { type: mimeType });
  return new File([blob], filename, { type: mimeType });
}

/**
 * Cria uma imagem de teste em base64
 * @returns {string} Imagem PNG em base64
 */
export function createTestImageBase64() {
  // PNG de 1x1 pixel transparente
  return 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==';
}

/**
 * Converte arquivo para base64
 * @param {File} file - Arquivo a ser convertido
 * @returns {Promise<string>} Base64 do arquivo
 */
export function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result;
      if (result.includes(',')) {
        resolve(result.split(',')[1]);
      } else {
        resolve(result);
      }
    };
    reader.onerror = error => reject(error);
    reader.readAsDataURL(file);
  });
}

/**
 * Valida se uma string é um base64 válido
 * @param {string} str - String a ser validada
 * @returns {boolean} True se for base64 válido
 */
export function isValidBase64(str) {
  if (!str || typeof str !== 'string') return false;
  
  try {
    // Verifica se é base64 válido
    return btoa(atob(str)) === str;
  } catch (err) {
    return false;
  }
}

/**
 * Detecta o tipo de arquivo baseado no início do base64
 * @param {string} base64 - String base64
 * @returns {string} Tipo MIME detectado
 */
export function detectMimeTypeFromBase64(base64) {
  if (!base64) return 'application/octet-stream';
  
  const firstChars = base64.substring(0, 10);
  
  if (firstChars.startsWith('/9j/')) {
    return 'image/jpeg';
  } else if (firstChars.startsWith('iVBORw0KGgo')) {
    return 'image/png';
  } else if (firstChars.startsWith('R0lGOD')) {
    return 'image/gif';
  } else if (firstChars.startsWith('JVBERi0')) {
    return 'application/pdf';
  }
  
  return 'application/octet-stream';
}

/**
 * Cria uma URL de dados a partir de base64
 * @param {string} base64 - String base64
 * @param {string} mimeType - Tipo MIME (opcional, será detectado se não fornecido)
 * @returns {string} URL de dados
 */
export function createDataUrl(base64, mimeType = null) {
  if (!base64) return '';
  
  const detectedMimeType = mimeType || detectMimeTypeFromBase64(base64);
  return `data:${detectedMimeType};base64,${base64}`;
} 