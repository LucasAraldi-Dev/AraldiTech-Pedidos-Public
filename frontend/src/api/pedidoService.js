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
      console.error('Erro ao buscar pedidos:', error);
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
        console.error('Token de autenticação não encontrado');
        throw {
          statusCode: 401,
          details: 'Você precisa estar autenticado para visualizar pedidos'
        };
      }
      
      console.log(`Iniciando busca do pedido #${id}`);
      
      // Garantir token CSRF atualizado
      const csrfToken = await ensureCsrfToken();
      console.log(`Token CSRF obtido: ${csrfToken ? 'Sim' : 'Não'}`);
      
      // Fazer a requisição usando axiosService
      console.log(`Enviando requisição para /pedidos/${id}`);
      const response = await axiosService.get(`/pedidos/${id}`);
      
      console.log(`Resposta recebida para pedido #${id}:`, response.status);
      
      return response.data;
    } catch (error) {
      console.error(`Erro ao buscar pedido #${id}:`, error);
      
      // Adicionar informações de diagnóstico ao erro
      if (error.response) {
        error.statusCode = error.response.status;
        error.details = error.response.data?.detail || 'Erro desconhecido';
        
        console.error(`Erro HTTP ${error.statusCode}: ${error.details}`);
        if (error.response.headers) {
          console.error('Cabeçalhos da resposta:', error.response.headers);
        }
      } else if (error.request) {
        error.networkError = true;
        console.error('Erro de rede - sem resposta do servidor:', error.request);
      } else {
        console.error('Erro desconhecido:', error.message);
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
      console.error(`Erro ao atualizar pedido #${id}:`, error);
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
      console.error(`Erro ao atualizar pedido #${id} com histórico:`, error);
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
      console.error(`Erro ao buscar histórico do pedido #${id}:`, error);
      throw error;
    }
  },
  
  /**
   * Reseta o serviço de pedidos, limpando tokens e forçando uma nova autenticação.
   * Útil em caso de erros persistentes de CORS ou autenticação.
   */
  async reset() {
    try {
      console.log('Reiniciando serviço de pedidos...');
      
      // Forçar renovação do token CSRF
      await ensureCsrfToken(true);
      
      // Verificar token de autenticação
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.warn('Token de autenticação não encontrado durante reset');
        return false;
      }
      
      // Testar endpoint básico para verificar conectividade
      await axiosService.get('/pedidos');
      
      console.log('Serviço de pedidos reiniciado com sucesso');
      return true;
    } catch (error) {
      console.error('Falha ao reiniciar serviço de pedidos:', error);
      return false;
    }
  }
};

export default pedidoService;
