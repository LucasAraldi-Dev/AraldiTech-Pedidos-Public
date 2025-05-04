"""
Script para iniciar o servidor de desenvolvimento com configurações adequadas para CORS.
Execute com: python backend/run_dev_server.py
"""
import uvicorn

if __name__ == "__main__":
    # Configuração do servidor uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",      # Permite conexões de qualquer IP
        port=8000,           # Porta padrão
        reload=True,         # Reinicia automaticamente ao alterar arquivos
        log_level="info",    # Nível de log
        access_log=True,     # Registra requisições
    ) 