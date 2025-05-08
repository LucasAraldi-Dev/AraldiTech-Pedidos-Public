<template>
  <div class="user-management">
    <div class="header">
      <h1>Gerenciamento de Usuários</h1>
      <button class="add-user-btn" @click="openAddUserModal">Adicionar Usuário</button>
    </div>

    <div class="search-bar">
      <input 
        type="text" 
        v-model="searchTerm" 
        placeholder="Buscar usuário por nome, email ou username"
        @input="filterUsers"
      />
    </div>

    <div class="users-table">
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Username</th>
            <th>Email</th>
            <th>Setor</th>
            <th>Tipo</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user._id">
            <td>{{ user.nome }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.setor }}</td>
            <td>{{ user.tipo_usuario }}</td>
            <td>
              <button @click="editUser(user)" class="edit-btn">Editar</button>
              <button @click="deleteUser(user)" class="delete-btn">Excluir</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Adição/Edição de Usuário -->
    <div class="modal-overlay" v-if="isModalOpen">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ isEditing ? 'Editar Usuário' : 'Adicionar Usuário' }}</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        
        <form @submit.prevent="saveUser">
          <div class="form-group">
            <label for="name">Nome Completo</label>
            <input 
              id="name" 
              type="text" 
              v-model="currentUser.nome" 
              required
            />
          </div>

          <div class="form-group">
            <label for="username">Nome de Usuário</label>
            <input 
              id="username" 
              type="text" 
              v-model="currentUser.username" 
              required
            />
          </div>

          <div class="form-group">
            <label for="email">Email</label>
            <input 
              id="email" 
              type="email" 
              v-model="currentUser.email" 
              required
            />
          </div>

          <div class="form-group">
            <label for="setor">Setor</label>
            <select id="setor" v-model="currentUser.setor" required>
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
            <label for="tipoUsuario">Tipo de Usuário</label>
            <select id="tipoUsuario" v-model="currentUser.tipo_usuario" required>
              <option value="comum">Comum</option>
              <option value="admin">Administrador</option>
            </select>
          </div>

          <div class="form-group">
            <label for="password">{{ isEditing ? 'Nova Senha (deixe em branco para manter a atual)' : 'Senha' }}</label>
            <input 
              id="password" 
              type="password" 
              v-model="currentUser.senha" 
              :required="!isEditing"
            />
          </div>

          <div class="button-group">
            <button type="submit" class="save-btn">{{ isEditing ? 'Salvar Alterações' : 'Adicionar Usuário' }}</button>
            <button type="button" @click="closeModal" class="cancel-btn">Cancelar</button>
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
  name: 'UserManagement',
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      users: [],
      filteredUsers: [],
      searchTerm: '',
      isModalOpen: false,
      isEditing: false,
      currentUser: {
        nome: '',
        username: '',
        email: '',
        setor: '',
        tipo_usuario: 'comum',
        senha: ''
      }
    };
  },
  async created() {
    await this.checkAdminAccess();
    this.fetchUsers();
  },
  methods: {
    async checkAdminAccess() {
      try {
        const user = await authService.validateToken();
        if (!user || user.tipo_usuario !== 'admin') {
          this.$router.push('/login');
          this.toast.error('Acesso restrito a administradores');
        }
      } catch (error) {
        console.error('Erro ao verificar acesso:', error);
        this.$router.push('/login');
        this.toast.error('Erro ao verificar permissões');
      }
    },
    async fetchUsers() {
      try {
        const user = await authService.validateToken();
        if (!user) {
          this.$router.push('/login');
          this.toast.error('Sua sessão expirou. Por favor, faça login novamente.');
          return;
        }
        
        const config = {
          withCredentials: true,
          headers: {}
        };
        
        const csrfToken = authService.getToken();
        if (csrfToken) {
          config.headers['X-CSRF-Token'] = csrfToken;
        }
        
        const response = await axios.get(
          `${process.env.VUE_APP_API_URL}/usuarios`,
          config
        );
        
        this.users = response.data;
        this.filteredUsers = [...this.users];
      } catch (error) {
        console.error('Erro ao buscar usuários:', error);
        if (process.env.NODE_ENV === 'development') {
          console.log('Criando usuários fictícios para ambiente de desenvolvimento');
          this.users = [
            { _id: '1', nome: 'Admin Teste', username: 'admin', email: 'admin@example.com', tipo_usuario: 'admin' },
            { _id: '2', nome: 'Usuário Teste', username: 'user', email: 'user@example.com', tipo_usuario: 'comum' }
          ];
          this.filteredUsers = [...this.users];
        } else {
          this.toast.error('Erro ao carregar lista de usuários');
        }
      }
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
    openAddUserModal() {
      this.isEditing = false;
      this.currentUser = {
        nome: '',
        username: '',
        email: '',
        setor: '',
        tipo_usuario: 'comum',
        senha: ''
      };
      this.isModalOpen = true;
    },
    editUser(user) {
      this.isEditing = true;
      this.currentUser = { ...user };
      this.currentUser.senha = '';
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
      this.currentUser = {
        nome: '',
        username: '',
        email: '',
        setor: '',
        tipo_usuario: 'comum',
        senha: ''
      };
    },
    async saveUser() {
      try {
        const user = await authService.validateToken();
        if (!user) {
          this.$router.push('/login');
          this.toast.error('Sua sessão expirou. Por favor, faça login novamente.');
          return;
        }
        
        const userData = { ...this.currentUser };
        
        if (this.isEditing) {
          if (!userData.senha) {
            delete userData.senha;
          }
          
          const changes = this.getChanges(this.users.find(u => u._id === userData._id), userData);
          
          if (Object.keys(changes).length > 0) {
            userData.log = {
              changedBy: user.nome,
              changedAt: new Date().toISOString(),
              changes: changes
            };
          }
          
          await axios.put(
            `${process.env.VUE_APP_API_URL}/usuarios/${userData._id}`,
            userData,
            {
              headers: { Authorization: `Bearer ${authService.getToken()}` }
            }
          );
          
          this.toast.success('Usuário atualizado com sucesso!');
        } else {
          await axios.post(
            `${process.env.VUE_APP_API_URL}/usuarios/`,
            userData,
            {
              headers: { Authorization: `Bearer ${authService.getToken()}` }
            }
          );
          
          this.toast.success('Usuário adicionado com sucesso!');
        }
        
        this.closeModal();
        this.fetchUsers();
      } catch (error) {
        console.error('Erro ao salvar usuário:', error);
        this.toast.error('Erro ao salvar usuário');
      }
    },
    async deleteUser(user) {
      if (!confirm('Tem certeza que deseja excluir este usuário?')) {
        return;
      }
      
      try {
        const currentUser = await authService.validateToken();
        if (!currentUser) {
          this.$router.push('/login');
          this.toast.error('Sua sessão expirou. Por favor, faça login novamente.');
          return;
        }
        
        await axios.delete(
          `${process.env.VUE_APP_API_URL}/usuarios/${user._id}`,
          {
            headers: { Authorization: `Bearer ${authService.getToken()}` }
          }
        );
        
        this.toast.success('Usuário excluído com sucesso!');
        this.fetchUsers();
      } catch (error) {
        console.error('Erro ao excluir usuário:', error);
        this.toast.error('Erro ao excluir usuário');
      }
    },
    getChanges(original, updated) {
      const changes = {};
      
      for (const key in updated) {
        if (['_id', 'log', 'senha'].includes(key)) continue;
        
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
    }
  }
};
</script>

<style scoped>
.user-management {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  margin: 0;
  color: #333;
}

.add-user-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-user-btn:hover {
  background-color: #45a049;
}

.search-bar {
  margin-bottom: 20px;
}

.search-bar input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.users-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
  font-weight: bold;
}

tr:hover {
  background-color: #f9f9f9;
}

.edit-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-right: 8px;
}

.edit-btn:hover {
  background-color: #45a049;
}

.delete-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete-btn:hover {
  background-color: #da190b;
}

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

.modal {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h2 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.close-btn:hover {
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
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
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-btn:hover {
  background-color: #45a049;
}

.cancel-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-btn:hover {
  background-color: #da190b;
}

@media (max-width: 768px) {
  .user-management {
    padding: 15px;
  }
  
  .header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .add-user-btn {
    width: 100%;
  }
  
  table {
    min-width: 800px;
  }
  
  .modal {
    width: 95%;
  }
}
</style>