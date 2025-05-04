import axios from "axios";

export async function isTokenValid() {
  const token = localStorage.getItem("access_token");
  console.log("Validando token:", token?.substring(0, 10) + "...");
  
  if (!token) {
    console.log("Nenhum token encontrado");
    return null; // Retorne `null` para tokens ausentes.
  }
  
  // URL base primária e fallback
  const baseUrls = [
    process.env.VUE_APP_API_URL,
    "http://localhost:8000",
    "http://192.168.1.5:8000"
  ];
  
  // Tenta cada URL base até obter sucesso
  for (const baseUrl of baseUrls) {
    if (!baseUrl) continue;
    
    try {
      console.log(`Chamando API para validar token em ${baseUrl}...`);
      const response = await axios.get(`${baseUrl}/auth/validate-token`, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        withCredentials: false
      });
      
      console.log("Resposta da validação:", response.data);
      return response.data.user || null; // Retorna o usuário, caso o backend forneça.
    } catch (error) {
      console.error(`Erro validando token em ${baseUrl}:`, error.message);
      // Continue tentando com a próxima URL
    }
  }
  
  console.error("Falha em todas as tentativas de validação do token");
  return null;
}