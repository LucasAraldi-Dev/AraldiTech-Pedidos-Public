import axios from "axios";

export async function isTokenValid() {
  const token = localStorage.getItem("access_token");
  if (!token) return null; // Retorne `null` para tokens ausentes.
  
  try {
    const response = await axios.get(`${process.env.VUE_APP_API_URL}/auth/validate-token`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data.user || null; // Retorna o usuário, caso o backend forneça.
  } catch (error) {
    console.error("Token inválido ou expirado", error);
    return null;
  }
}