import { 
  validateQuantity, 
  validateMonetaryValue, 
  validateDate, 
  validateText,
  formatDate,
  formatCurrency
} from '@/utils/validationService';

describe('ValidationService', () => {
  describe('validateQuantity', () => {
    it('should validate valid quantity', () => {
      expect(validateQuantity(5).isValid).toBe(true);
      expect(validateQuantity(1).isValid).toBe(true);
      expect(validateQuantity(1000).isValid).toBe(true);
    });
    
    it('should reject invalid quantity', () => {
      expect(validateQuantity(0).isValid).toBe(false);
      expect(validateQuantity(-1).isValid).toBe(false);
      expect(validateQuantity(null).isValid).toBe(false);
      expect(validateQuantity(undefined).isValid).toBe(false);
      expect(validateQuantity('abc').isValid).toBe(false);
    });
    
    it('should return appropriate error messages', () => {
      expect(validateQuantity(0).message).toBe('A quantidade deve ser maior que zero.');
      expect(validateQuantity(null).message).toBe('A quantidade deve ser um número válido.');
    });
  });
  
  describe('validateMonetaryValue', () => {
    it('should validate valid monetary values', () => {
      expect(validateMonetaryValue(100).isValid).toBe(true);
      expect(validateMonetaryValue(0).isValid).toBe(true);
      expect(validateMonetaryValue(0.5).isValid).toBe(true);
    });
    
    it('should reject negative values', () => {
      expect(validateMonetaryValue(-1).isValid).toBe(false);
      expect(validateMonetaryValue(-100).isValid).toBe(false);
    });
    
    it('should handle required flag correctly', () => {
      expect(validateMonetaryValue(null, false).isValid).toBe(true);
      expect(validateMonetaryValue(null, true).isValid).toBe(false);
      expect(validateMonetaryValue(undefined, false).isValid).toBe(true);
      expect(validateMonetaryValue(undefined, true).isValid).toBe(false);
    });
  });
  
  describe('validateDate', () => {
    it('should validate valid dates', () => {
      expect(validateDate('2025-01-01').isValid).toBe(true);
      expect(validateDate('2023-12-31').isValid).toBe(true);
    });
    
    it('should reject invalid date formats', () => {
      expect(validateDate('01/01/2025').isValid).toBe(false);
      expect(validateDate('2025-1-1').isValid).toBe(false);
      expect(validateDate('not-a-date').isValid).toBe(false);
    });
    
    it('should handle date range validation', () => {
      const options = {
        minDate: '2025-01-01',
        maxDate: '2025-12-31'
      };
      
      expect(validateDate('2025-06-15', options).isValid).toBe(true);
      expect(validateDate('2024-12-31', options).isValid).toBe(false);
      expect(validateDate('2026-01-01', options).isValid).toBe(false);
    });
    
    it('should enforce future dates when configured', () => {
      const today = new Date();
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      
      const yesterdayStr = yesterday.toISOString().split('T')[0];
      const tomorrowStr = tomorrow.toISOString().split('T')[0];
      
      const options = { allowPastDates: false };
      
      expect(validateDate(tomorrowStr, options).isValid).toBe(true);
      expect(validateDate(yesterdayStr, options).isValid).toBe(false);
    });
  });
  
  describe('validateText', () => {
    it('should validate required text', () => {
      expect(validateText('Some text').isValid).toBe(true);
      expect(validateText('').isValid).toBe(false);
      expect(validateText(null).isValid).toBe(false);
    });
    
    it('should validate optional text', () => {
      const options = { required: false };
      expect(validateText('Some text', options).isValid).toBe(true);
      expect(validateText('', options).isValid).toBe(true);
      expect(validateText(null, options).isValid).toBe(true);
    });
    
    it('should validate text length constraints', () => {
      const options = { minLength: 5, maxLength: 10 };
      
      expect(validateText('12345', options).isValid).toBe(true);
      expect(validateText('1234567890', options).isValid).toBe(true);
      
      expect(validateText('1234', options).isValid).toBe(false);
      expect(validateText('12345678901', options).isValid).toBe(false);
    });
    
    it('should customize field name in error messages', () => {
      const options = { 
        required: true, 
        minLength: 5,
        fieldName: 'Descrição'
      };
      
      expect(validateText('', options).message).toBe('Descrição é obrigatório.');
      expect(validateText('123', options).message).toBe('Descrição deve ter pelo menos 5 caracteres.');
    });
  });
  
  describe('formatDate', () => {
    it('should format valid dates', () => {
      const date = new Date(2025, 0, 15); // 15 de Janeiro de 2025
      expect(formatDate(date)).toBe('15/01/2025');
      
      const dateStr = '2025-01-15';
      expect(formatDate(dateStr)).toBe('15/01/2025');
    });
    
    it('should handle invalid dates', () => {
      expect(formatDate(null)).toBe('');
      expect(formatDate('not-a-date')).toBe('Data inválida');
    });
  });
  
  describe('formatCurrency', () => {
    it('should format monetary values as Brazilian currency', () => {
      expect(formatCurrency(100)).toBe('R$ 100,00');
      expect(formatCurrency(1234.56)).toBe('R$ 1.234,56');
      expect(formatCurrency(0)).toBe('R$ 0,00');
    });
    
    it('should handle invalid values', () => {
      expect(formatCurrency(null)).toBe('R$ 0,00');
      expect(formatCurrency(undefined)).toBe('R$ 0,00');
      expect(formatCurrency('abc')).toBe('R$ 0,00');
    });
  });
}); 