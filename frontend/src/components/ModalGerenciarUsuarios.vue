<template>
  <div class="modal-overlay" v-if="isOpen">
    <div class="order-form" @click.stop>
      <h2>GERENCIAR USUÁRIOS</h2>

      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchTerm" 
          placeholder="Buscar usuário por nome, email ou username"
          @input="filterUsers"
        />
      </div>

      <!-- Carregando indicador -->
      <div v-if="isLoading" class="loading-indicator">
        <p>Carregando usuários...</p>
      </div>

      <!-- Cards dos Usuários -->
      <div class="users-list">
        <div v-if="isDemoMode" class="demo-notice">
          <p>⚠️ Exibindo dados de demonstração. A conexão com o backend falhou.</p>
        </div>
        <div v-if="filteredUsers.length === 0 && !isLoading" class="no-users-notice">
          <p>Nenhum usuário encontrado.</p>
        </div>
        <div v-for="user in filteredUsers" :key="user._id" class="user-card">
          <div class="user-header">
            <span class="user-type" :class="getUserTypeBadgeClass(user.tipo_usuario)">
              {{ getUserTypeLabel(user.tipo_usuario) }}
            </span>
          </div>
          <h3 class="user-name">{{ user.nome }}</h3>
          <div class="user-details">
            <p><strong>Username:</strong> {{ user.username }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
            <p><strong>Setor:</strong> {{ user.setor }}</p>
          </div>
          <div class="user-actions">
            <button class="edit-button" @click="editUser(user)">EDITAR</button>
          </div>
        </div>
      </div>

      <!-- Botão Fechar -->
      <div class="button-row">
        <button class="debug-btn" @click="reloadUsers">RECARREGAR DADOS</button>
        <button class="close-btn" @click="$emit('close')">FECHAR</button>
      </div>
    </div>

    <!-- Modal de Edição de Usuário -->
    <div class="edit-modal-overlay" v-if="isEditModalOpen">
      <div class="edit-modal">
        <div class="modal-header">
          <h3>Editar Usuário</h3>
          <button class="close-btn" @click="closeEditModal">&times;</button>
        </div>
        
        <form @submit.prevent="saveUserChanges">
          <div class="form-group">
            <label for="editName">Nome Completo</label>
            <input 
              id="editName" 
              type="text" 
              v-model="editingUser.nome" 
              required
            />
          </div>

          <div class="form-group">
            <label for="editUsername">Nome de Usuário</label>
            <input 
              id="editUsername" 
              type="text" 
              v-model="editingUser.username" 
              required
            />
          </div>

          <div class="form-group">
            <label for="editEmail">Email</label>
            <input 
              id="editEmail" 
              type="email" 
              v-model="editingUser.email" 
              required
            />
          </div>

          <div class="form-group">
            <label for="editSetor">Setor</label>
            <select id="editSetor" v-model="editingUser.setor" required>
              <option value="Escritório">Escritório</option>
              <option value="Fábrica de Ração">Fábrica de Ração</option>
              <option value="CPO">CPO</option>
              <option value="Granjas">Granjas</option>
              <option value="Abatedouro">Abatedouro</option>
              <option value="Transporte">Transporte</option>
              <option value="Incubatório">Incubatório</option>
              <option value="Favorito">Favorito</option>
            </select>
          </div>

          <div class="form-group">
            <label for="editTipoUsuario">Tipo de Usuário</label>
            <select id="editTipoUsuario" v-model="editingUser.tipo_usuario" required>
              <option value="comum">Comum</option>
              <option value="gestor">Gestor</option>
              <option value="admin">Administrador</option>
            </select>
          </div>

          <div class="form-group">
            <label for="editPassword">Nova Senha (deixe em branco para manter a atual)</label>
            <input 
              id="editPassword" 
              type="password" 
              v-model="editingUser.newPassword" 
            />
          </div>

          <div class="button-group">
            <button type="submit" class="save-btn">Salvar Alterações</button>
            <button type="button" @click="closeEditModal" class="cancel-btn">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';
import authService from '@/api/authService';

export default {
  name: 'ModalGerenciarUsuarios',
  props: {
    isOpen: {
      type: Boolean,
      required: true
    }
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      users: [],
      filteredUsers: [],
      searchTerm: '',
      isEditModalOpen: false,
      editingUser: null,
      originalUserData: null,
      isDemoMode: false,
      isLoading: false,
      hasLoadedData: false
    };
  },
  created() {
    console.log('ModalGerenciarUsuarios criado');
  },
  mounted() {
    console.log('ModalGerenciarUsuarios montado');
  },
  watch: {
    isOpen: {
      immediate: true,
      handler(newVal, oldVal) {
        console.log('Modal de gerenciamento alterado:', oldVal, '->', newVal);
        if (newVal === true) {
          console.log('Modal foi aberto, carregando usuários...');
          // Emitir evento para fechar o menu mobile
          this.$emit('close-menu');
          // Inicializar usuários apenas uma vez quando o modal for aberto
          this.initializeUsers();
        }
      }
    }
  },
  methods: {
    initializeUsers() {
      if (this.isLoading) {
        console.log('Carregamento já em andamento, ignorando inicialização duplicada');
        return;
      }
      // Mostrar dados de demonstração imediatamente ao abrir o modal
      this.addDummyUsers();
      // Tentar carregar dados reais em seguida
      this.fetchUsers();
    },
    
    async fetchUsers() {
      console.log('Iniciando fetchUsers em ModalGerenciarUsuarios');
      this.isLoading = true;
      
      try {
        const user = await authService.validateToken();
        console.log('Resultado da validação do token:', user);
        
        if (!user) {
          console.error('Token inválido ou usuário não autenticado');
          this.$router.push('/login');
          this.toast.error('Sua sessão expirou. Por favor, faça login novamente.');
          return;
        }
        
        // Verificar se o usuário é admin
        const currentUser = authService.getUser();
        console.log('Usuário atual:', currentUser);
        
        if (!currentUser || currentUser.tipo_usuario !== 'admin') {
          console.error('Usuário não é administrador:', currentUser);
          this.toast.error('Acesso restrito a administradores');
          return;
        }
        
        // Usar o token de autenticação diretamente
        const token = authService.getToken();
        console.log('Token obtido:', token ? token.substring(0, 15) + '...' : 'Nenhum token');
        
        if (!token) {
          console.error('Token não encontrado');
          this.toast.error('Token de autenticação não encontrado.');
          return;
        }
        
        console.log('Buscando usuários com token:', token.substring(0, 10) + '...');
        console.log('URL da API:', process.env.VUE_APP_API_URL);
        
        try {
          const response = await axios.get(
            `${process.env.VUE_APP_API_URL}/usuarios`,
            {
              headers: { 
                Authorization: `Bearer ${token}`
              }
            }
          );
          
          console.log('Resposta da API de usuários:', response.data);
          
          if (response.data && Array.isArray(response.data) && response.data.length > 0) {
            // Dados reais recebidos, desliga o modo demonstração
            this.isDemoMode = false;
            this.users = response.data;
            this.filteredUsers = [...this.users];
            console.log('Dados carregados com sucesso:', this.users.length, 'usuários');
            
            // Exibir o toast apenas se ainda não tiver carregado dados antes
            if (!this.hasLoadedData) {
              this.toast.success(`${this.users.length} usuários carregados com sucesso`);
              this.hasLoadedData = true;
            }
          } else {
            console.warn('Resposta da API não contém dados de usuários');
            this.toast.warning('Nenhum usuário encontrado na resposta da API');
          }
        } catch (apiError) {
          console.error('Erro na requisição API:', apiError);
          console.error('Detalhes da resposta:', apiError.response);
          this.toast.error(`Erro ao buscar usuários: ${apiError.response?.status || ''} ${apiError.response?.statusText || apiError.message || ''}`);
        } finally {
          this.isLoading = false;
        }
      } catch (error) {
        console.error('Erro geral ao buscar usuários:', error);
        this.toast.error('Erro ao carregar lista de usuários');
        this.isLoading = false;
      }
    },
    
    // Função para adicionar usuários fictícios (para desenvolvimento)
    addDummyUsers() {
      console.log('Adicionando usuários de demonstração');
      this.isDemoMode = true;
      this.users = [
        { _id: '1', nome: 'Admin Teste', username: 'admin', email: 'admin@example.com', tipo_usuario: 'admin', setor: 'TI' },
        { _id: '2', nome: 'Lucas Araldi', username: 'lucasaraldi', email: 'lucas@example.com', tipo_usuario: 'admin', setor: 'Escritório' },
        { _id: '3', nome: 'Usuário Comum', username: 'usuario', email: 'usuario@example.com', tipo_usuario: 'comum', setor: 'Fábrica de Ração' }
      ];
      this.filteredUsers = [...this.users];
      console.log('Usuários de demonstração adicionados:', this.users.length);
    },
    filterUsers() {
      if (!this.searchTerm) {
        this.filteredUsers = [...this.users];
        return;
      }
      
      const term = this.searchTerm.toLowerCase();
      this.filteredUsers = this.users.filter(user => 
        user.nome.toLowerCase().includes(term) || 
        user.email.toLowerCase().includes(term) ||
        user.username.toLowerCase().includes(term)
      );
    },
    editUser(user) {
      this.originalUserData = { ...user };
      this.editingUser = { 
        ...user,
        newPassword: ''
      };
      this.isEditModalOpen = true;
    },
    closeEditModal() {
      this.isEditModalOpen = false;
      this.editingUser = null;
    },
    async saveUserChanges() {
      try {
        const user = await authService.validateToken();
        if (!user) {
          this.closeEditModal();
          this.$router.push('/login');
          this.toast.error('Sua sessão expirou. Por favor, faça login novamente.');
          return;
        }
        
        const userData = { ...this.editingUser };
        
        if (!userData.newPassword) {
          delete userData.newPassword;
        } else {
          userData.senha = userData.newPassword;
          delete userData.newPassword;
        }
        
        const changes = this.getChanges(this.originalUserData, userData);
        
        if (Object.keys(changes).length > 0) {
          const currentUser = authService.getUser();
          userData.log = {
            changedBy: currentUser.nome,
            changedAt: new Date().toISOString(),
            changes: changes
          };
        }
        
        const token = authService.getToken();
        await axios.put(
          `${process.env.VUE_APP_API_URL}/usuarios/${userData._id}`,
          userData,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        
        this.toast.success('Usuário atualizado com sucesso!');
        this.closeEditModal();
        this.fetchUsers();
      } catch (error) {
        console.error('Erro ao atualizar usuário:', error);
        this.toast.error('Erro ao atualizar usuário');
      }
    },
    getChanges(original, updated) {
      const changes = {};
      
      for (const key in updated) {
        if (['_id', 'log', 'senha', 'newPassword'].includes(key)) continue;
        
        if (original[key] !== updated[key]) {
          changes[key] = {
            from: original[key],
            to: updated[key]
          };
        }
      }
      
      if (updated.senha) {
        changes.senha = {
          from: '[protegido]',
          to: '[nova senha protegida]'
        };
      }
      
      return changes;
    },
    reloadUsers() {
      console.log('Recarregando usuários...');
      this.toast.info('Tentando recarregar dados de usuários...');
      // Resetar a flag para permitir o toast na recarga manual
      this.hasLoadedData = false;
      // Manter o modo de demonstração até que novos dados sejam recebidos
      this.fetchUsers();
    },
    getUserTypeBadgeClass(tipoUsuario) {
      switch(tipoUsuario) {
        case 'admin':
          return 'admin-badge';
        case 'gestor':
          return 'gestor-badge';
        default:
          return 'user-badge';
      }
    },
    
    getUserTypeLabel(tipoUsuario) {
      switch(tipoUsuario) {
        case 'admin':
          return 'ADMIN';
        case 'gestor':
          return 'GESTOR';
        default:
          return 'USUÁRIO';
      }
    },
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.order-form {
  background-color: #1e1e1e;
  padding: 30px;
  border-radius: 15px;
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  overflow-y: auto;
  color: white;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
}

h2 {
  color: white;
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  letter-spacing: 2px;
}

.search-bar {
  margin-bottom: 20px;
}

.search-bar input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #444;
  border-radius: 8px;
  background-color: #333;
  color: white;
  font-size: 16px;
}

.search-bar input:focus {
  outline: none;
  border-color: #66ccff;
}

.users-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.user-card {
  background-color: #2a2a2a;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  overflow: hidden;
  position: relative;
}

.user-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
}

.user-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

.user-type {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 12px;
  font-weight: bold;
}

.admin-badge {
  background-color: #ff9800;
  color: black;
}

.user-badge {
  background-color: #4caf50;
  color: white;
}

.gestor-badge {
  background-color: #9b59b6;
  color: white;
}

.user-name {
  margin: 0 0 15px;
  font-size: 18px;
  color: #66ccff;
}

.user-details {
  margin-bottom: 15px;
}

.user-details p {
  margin: 8px 0;
  font-size: 14px;
}

.user-actions {
  display: flex;
  justify-content: flex-end;
}

.edit-button {
  background-color: #4a6da7;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.edit-button:hover {
  background-color: #3a5d97;
}

.close-btn {
  display: block;
  margin: 20px auto 0;
  padding: 12px 25px;
  background-color: #ff5252;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: #ff3838;
}

.edit-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.edit-modal {
  background-color: #2a2a2a;
  padding: 25px;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  color: white;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  color: #66ccff;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #ccc;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  background-color: #333;
  border: 1px solid #444;
  border-radius: 5px;
  color: white;
  font-size: 16px;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #66ccff;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.save-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.save-btn:hover {
  background-color: #45a049;
}

.cancel-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.cancel-btn:hover {
  background-color: #da190b;
}

.button-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.debug-btn {
  background-color: #4a6da7;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.debug-btn:hover {
  background-color: #3a5d97;
}

@media (max-width: 768px) {
  .users-list {
    grid-template-columns: 1fr;
  }
  
  .edit-modal {
    width: 95%;
    padding: 15px;
  }
}

.demo-notice {
  grid-column: 1 / -1;
  background-color: #ffc107;
  color: #333;
  padding: 10px 15px;
  border-radius: 5px;
  margin-bottom: 15px;
  font-weight: bold;
  text-align: center;
}

.demo-notice p {
  margin: 0;
}

.loading-indicator {
  text-align: center;
  margin-bottom: 20px;
}

.no-users-notice {
  text-align: center;
  margin-bottom: 20px;
}
</style>