  <RegisterModal 
    :isModalOpen="isRegisterModalOpen" 
    @close-modal="closeRegisterModal" 
    @go-to-login="switchToLogin" 
    @signup="handleSignup" 
  />

  <!-- Método chamado quando o usuário se cadastra -->
  async handleSignup(userData, callback) {
    try {
      const response = await axios.post(
        `${process.env.VUE_APP_API_URL}/usuarios/`,
        userData
      );
      
      console.log("Usuário cadastrado com sucesso:", response.data);
      
      // Chamar o callback com sucesso se existir
      if (typeof callback === 'function') {
        callback(true);
      }
      
    } catch (error) {
      console.error("Erro ao cadastrar usuário:", error);
      
      // Chamar o callback com erro se existir
      if (typeof callback === 'function') {
        const errorMessage = error.response?.data?.detail || "Erro na conexão com o servidor";
        callback(false, new Error(errorMessage));
      }
      
      // Exibir mensagem de erro
      this.toast.error(error.response?.data?.detail || "Erro ao cadastrar. Verifique os dados e tente novamente.");
    }
  }, 