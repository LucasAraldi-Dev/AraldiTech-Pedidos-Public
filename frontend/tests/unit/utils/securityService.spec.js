import {
  sanitizeHtml,
  detectScriptInjection,
  detectSqlInjection,
  checkPasswordStrength,
  validateObject
} from '@/utils/securityService';

// Mocking axios
jest.mock('@/api/axiosService', () => ({
  get: jest.fn().mockResolvedValue({ data: { token: 'test-csrf-token' } }),
  setupCsrfInterceptor: jest.fn()
}));

describe('SecurityService', () => {
  describe('sanitizeHtml', () => {
    it('should sanitize HTML tags', () => {
      const input = '<script>alert("XSS")</script>';
      const expected = '&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;';
      expect(sanitizeHtml(input)).toBe(expected);
    });
    
    it('should handle special characters', () => {
      const input = '& < > " \'';
      const expected = '&amp; &lt; &gt; &quot; &#39;';
      expect(sanitizeHtml(input)).toBe(expected);
    });
    
    it('should handle empty and null input', () => {
      expect(sanitizeHtml('')).toBe('');
      expect(sanitizeHtml(null)).toBe('');
      expect(sanitizeHtml(undefined)).toBe('');
    });
  });
  
  describe('detectScriptInjection', () => {
    it('should detect script tags', () => {
      expect(detectScriptInjection('<script>alert(1)</script>')).toBe(true);
      expect(detectScriptInjection('Normal text with <script> tag')).toBe(true);
      expect(detectScriptInjection('Normal text with </script> closing tag')).toBe(true);
    });
    
    it('should detect javascript: protocol', () => {
      expect(detectScriptInjection('javascript:alert(1)')).toBe(true);
      expect(detectScriptInjection('Click href="javascript:alert(1)"')).toBe(true);
    });
    
    it('should detect event handlers', () => {
      expect(detectScriptInjection('onload=alert(1)')).toBe(true);
      expect(detectScriptInjection('<img onmouseover="alert(1)">')).toBe(true);
      expect(detectScriptInjection('onclick = doSomething()')).toBe(true);
    });
    
    it('should detect other suspicious patterns', () => {
      expect(detectScriptInjection('document.cookie')).toBe(true);
      expect(detectScriptInjection('eval("alert(1)")')).toBe(true);
      expect(detectScriptInjection('alert(document.domain)')).toBe(true);
    });
    
    it('should not flag safe content', () => {
      expect(detectScriptInjection('Normal text content')).toBe(false);
      expect(detectScriptInjection('Using <div> tags is fine')).toBe(false);
      expect(detectScriptInjection('This is > than that and < than the other')).toBe(false);
    });
  });
  
  describe('detectSqlInjection', () => {
    it('should detect SQL keywords', () => {
      expect(detectSqlInjection('SELECT * FROM users')).toBe(true);
      expect(detectSqlInjection('product WHERE 1=1')).toBe(true);
      expect(detectSqlInjection('input"; DROP TABLE users;')).toBe(true);
    });
    
    it('should detect SQL logical operators', () => {
      expect(detectSqlInjection('username OR 1=1')).toBe(true);
      expect(detectSqlInjection('admin" OR "1"="1')).toBe(true);
    });
    
    it('should not flag regular content', () => {
      expect(detectSqlInjection('Normal text')).toBe(false);
      expect(detectSqlInjection('Product name')).toBe(false);
      expect(detectSqlInjection('Price: 25.99')).toBe(false);
    });
  });
  
  describe('checkPasswordStrength', () => {
    it('should calculate score correctly', () => {
      // Should score 0 - no criteria met
      expect(checkPasswordStrength('').score).toBe(0);
      
      // Should score 1 - length only
      expect(checkPasswordStrength('12345678').score).toBe(1);
      
      // Should score 2 - length + lowercase
      expect(checkPasswordStrength('abcdefgh').score).toBe(2);
      
      // Should score 3 - length + lowercase + uppercase
      expect(checkPasswordStrength('abcdEFGH').score).toBe(3);
      
      // Should score 4 - length + lowercase + uppercase + number
      expect(checkPasswordStrength('abcdEFG1').score).toBe(4);
      
      // Should score 5 - all criteria met
      expect(checkPasswordStrength('abcdEFG1!')).toBe(5);
    });
    
    it('should provide appropriate feedback', () => {
      const shortPassword = checkPasswordStrength('abc');
      expect(shortPassword.feedback).toContain('pelo menos 8 caracteres');
      
      const noUppercase = checkPasswordStrength('abcdefgh1!');
      expect(noUppercase.feedback).toContain('letra maiúscula');
      
      const strongPassword = checkPasswordStrength('Abcdef1!');
      expect(strongPassword.feedback).toBe('Senha forte');
    });
  });
  
  describe('validateObject', () => {
    it('should validate required fields', () => {
      const data = { name: 'Test', age: '' };
      const rules = {
        name: { required: true },
        age: { required: true }
      };
      
      const result = validateObject(data, rules);
      expect(result.isValid).toBe(false);
      expect(result.errors.age).toBeTruthy();
    });
    
    it('should validate patterns', () => {
      const data = { email: 'not-an-email' };
      const rules = {
        email: { 
          pattern: '^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$',
          patternMessage: 'Email inválido'
        }
      };
      
      const result = validateObject(data, rules);
      expect(result.isValid).toBe(false);
      expect(result.errors.email).toBe('Email inválido');
    });
    
    it('should validate min and max values', () => {
      const data = { age: 15, score: 110 };
      const rules = {
        age: { min: 18 },
        score: { max: 100 }
      };
      
      const result = validateObject(data, rules);
      expect(result.isValid).toBe(false);
      expect(result.errors.age).toContain('maior ou igual a 18');
      expect(result.errors.score).toContain('menor ou igual a 100');
    });
    
    it('should validate string lengths', () => {
      const data = { shortText: 'AB', longText: 'ABCDEFGHIJK' };
      const rules = {
        shortText: { minLength: 3 },
        longText: { maxLength: 10 }
      };
      
      const result = validateObject(data, rules);
      expect(result.isValid).toBe(false);
      expect(result.errors.shortText).toContain('pelo menos 3 caracteres');
      expect(result.errors.longText).toContain('no máximo 10 caracteres');
    });
    
    it('should support custom validation', () => {
      const data = { password: 'pass', confirmPassword: 'password' };
      const rules = {
        password: { required: true },
        confirmPassword: { 
          required: true,
          custom: (value, data) => value === data.password || 'Senhas não coincidem'
        }
      };
      
      const result = validateObject(data, rules);
      expect(result.isValid).toBe(false);
      expect(result.errors.confirmPassword).toBe('Senhas não coincidem');
    });
  });
}); 