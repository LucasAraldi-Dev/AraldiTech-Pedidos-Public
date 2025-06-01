/**
 * Serviço de API para gerenciamento de Pedidos
 * Utiliza axiosService para garantir os cabeçalhos de autenticação e CSRF
 */

import axiosService from './axiosService';
import { ensureCsrfToken } from '@/utils/securityService';

/**
 * Serviço para operações relacionadas a Pedidos
 */
const pedidoService = {
  /**
   * Busca todos os pedidos disponíveis para o usuário atual
   */
  async buscarTodos() {
    try {
      // Garantir token CSRF atualizado
      await ensureCsrfToken();
      
      // Fazer a requisição usando axiosService
      const response = await axiosService.get('/pedidos');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Busca um pedido específico pelo ID
   * @param {number} id - ID do pedido
   */
  async buscarPorId(id) {
    try {
      if (!id) {
        throw new Error('ID do pedido é obrigatório');
      }
      
      // Verificar se o token de autenticação está disponível
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw {
          statusCode: 401,
          details: 'Você precisa estar autenticado para visualizar pedidos'
        };
      }
      
      // Garantir token CSRF atualizado
      await ensureCsrfToken();
      
      // Fazer a requisição usando axiosService
      const response = await axiosService.get(`/pedidos/${id}`);
      
      return response.data;
    } catch (error) {
      // Adicionar informações de diagnóstico ao erro
      if (error.response) {
        error.statusCode = error.response.status;
        error.details = error.response.data?.detail || 'Erro desconhecido';
      } else if (error.request) {
        error.networkError = true;
      }
      
      throw error;
    }
  },
  
  /**
   * Atualiza um pedido existente
   * @param {number} id - ID do pedido
   * @param {Object} dados - Dados atualizados do pedido
   */
  async atualizar(id, dados) {
    try {
      if (!id) {
        throw new Error('ID do pedido é obrigatório');
      }
      
      // Garantir token CSRF atualizado
      await ensureCsrfToken();
      
      // Fazer a requisição usando axiosService
      const response = await axiosService.put(`/pedidos/${id}`, dados);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Atualiza um pedido e registra no histórico
   * @param {number} id - ID do pedido
   * @param {Object} dados - Dados atualizados do pedido
   */
  async atualizarComHistorico(id, dados) {
    try {
      if (!id) {
        throw new Error('ID do pedido é obrigatório');
      }
      
      // Garantir token CSRF atualizado
      await ensureCsrfToken();
      
      // Fazer a requisição usando axiosService
      const response = await axiosService.put(`/pedidos/${id}/com-historico`, dados);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Obtém o histórico de um pedido
   * @param {number} id - ID do pedido
   */
  async obterHistorico(id) {
    try {
      if (!id) {
        throw new Error('ID do pedido é obrigatório');
      }
      
      // Garantir token CSRF atualizado
      await ensureCsrfToken();
      
      // Fazer a requisição usando axiosService
      const response = await axiosService.get(`/pedidos/${id}/historico`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Reseta o serviço de pedidos, limpando tokens e forçando uma nova autenticação.
   * Útil em caso de erros persistentes de CORS ou autenticação.
   */
  async reset() {
    try {
      // Forçar renovação do token CSRF
      await ensureCsrfToken(true);
      
      // Verificar token de autenticação
      const token = localStorage.getItem('access_token');
      if (!token) {
        return false;
      }
      
      // Testar endpoint básico para verificar conectividade
      await axiosService.get('/pedidos');
      
      return true;
    } catch (error) {
      return false;
    }
  }
};

export default pedidoService;
