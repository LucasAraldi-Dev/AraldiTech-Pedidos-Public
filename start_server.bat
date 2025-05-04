@echo off
echo Iniciando servidor AraldiTech-Pedidos...
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause 