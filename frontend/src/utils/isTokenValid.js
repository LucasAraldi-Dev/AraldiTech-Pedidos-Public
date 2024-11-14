import axios from "axios";

export async function isTokenValid() {
  const token = localStorage.getItem("access_token");
  if (!token) return false;
  
  try {
    await axios.get(`${process.env.VUE_APP_API_URL}/auth/validate-token`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return true;
  } catch (error) {
    console.error("Token inválido ou expirado", error);
    return false;
  }
}
