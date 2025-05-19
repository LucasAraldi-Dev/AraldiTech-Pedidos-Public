from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from . import schemas, database, auth
from .auth import get_current_user
from passlib.context import CryptContext
import logging
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import re
from .utils import registrar_atividade

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para converter ObjectId para string
def parse_obj_id(doc):
    if '_id' in doc:
        doc['_id'] = str(doc['_id']) 
    return doc

# Rota para criar um novo usuário
@router.post("/usuarios/", response_model=dict)
async def create_user(user: schemas.UsuarioCreate, db=Depends(database.get_db)):
    try:
        # Criptografar a senha
        user_dict = user.dict()
        user_dict["senha"] = pwd_context.hash(user_dict["senha"])
        
        # Verificar se já existe usuário com mesmo username ou email
        existing_user = await db["users"].find_one({"$or": [
            {"username": user_dict["username"]},
            {"email": user_dict["email"]}
        ]})
        
        if existing_user:
            if existing_user["username"] == user_dict["username"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nome de usuário já está em uso"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="E-mail já está em uso"
                )
        
        # Definir tipo de usuário como comum por padrão
        user_dict["tipo_usuario"] = "comum"
        
        # Processar informações do aceite dos termos
        if "termsAcceptance" in user_dict and user_dict["termsAcceptance"]:
            # Armazenar data de aceitação dos termos explicitamente
            if "timestamp" in user_dict["termsAcceptance"]:
                try:
                    # Converter o timestamp ISO para objeto datetime
                    user_dict["termsAcceptanceDate"] = datetime.fromisoformat(
                        user_dict["termsAcceptance"]["timestamp"].replace("Z", "+00:00")
                    )
                except ValueError:
                    # Se não for possível converter, usar a data atual
                    user_dict["termsAcceptanceDate"] = datetime.now()
            else:
                user_dict["termsAcceptanceDate"] = datetime.now()
                
            # Adicionar IP do usuário se não estiver presente
            if "ip" not in user_dict["termsAcceptance"]:
                # Nota: Em uma implementação real, você obteria o IP do cliente
                user_dict["termsAcceptance"]["ip"] = "not_captured"
        else:
            # Se não houver informações de aceite de termos, não criar o usuário
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="É necessário aceitar os Termos de Serviço para criar uma conta"
            )
        
        # Inserir no banco de dados
        result = await db["users"].insert_one(user_dict)
        
        # Obter o usuário recém-criado
        new_user = await db["users"].find_one({"_id": result.inserted_id})
        
        # Log de criação de usuário
        logging.info(f"Usuário criado com sucesso: {user_dict['username']} - Termos aceitos em: {user_dict.get('termsAcceptanceDate')}")
        
        # Registrar atividade de criação de usuário
        try:
            await registrar_atividade(
                db=db,
                tipo="registro",
                descricao=f"Novo usuário registrado: {user_dict['nome']} ({user_dict['username']}) - Setor: {user_dict['setor']}",
                usuario_nome=user_dict['nome']
            )
        except Exception as e:
            logging.error(f"Erro ao registrar atividade de criação de usuário: {e}")
        
        return parse_obj_id(new_user)
    except HTTPException as e:
        # Repassar exceções HTTP
        raise e
    except Exception as e:
        logging.error(f"Erro ao criar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

# Rota para listar todos os usuários (apenas para admins)
@router.get("/usuarios", response_model=List[dict])
async def list_users(db=Depends(database.get_db), current_user=Depends(get_current_user)):
    # Verificar se o usuário atual é admin
    if current_user.get("tipo_usuario") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para administradores"
        )
    
    # Buscar todos os usuários
    users = await db["users"].find().to_list(length=100)
    return [parse_obj_id(user) for user in users]

# Rota para atualizar um usuário (apenas para admins)
@router.put("/usuarios/{user_id}", response_model=dict)
async def update_user(user_id: str, user_data: dict, db=Depends(database.get_db), current_user=Depends(get_current_user)):
    # Verificar se o usuário atual é admin
    if current_user.get("tipo_usuario") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para administradores"
        )
    
    # Verificar se o usuário existe
    try:
        existing_user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Preparar dados para atualização
        update_data = {k: v for k, v in user_data.items() if k not in ["_id", "log", "senha"]}
            
        # Verificar se o tipo de usuário foi alterado
        tipo_usuario_alterado = False
        if "tipo_usuario" in update_data and existing_user.get("tipo_usuario") != update_data["tipo_usuario"]:
            tipo_usuario_alterado = True
            logging.info(f"Tipo de usuário de {existing_user['username']} alterado de {existing_user.get('tipo_usuario')} para {update_data['tipo_usuario']}")
        
        # Adicionar campo para indicar que o usuário precisa fazer login novamente 
        # se o tipo de usuário foi alterado
        if tipo_usuario_alterado:
            update_data["sessao_expirada"] = True
            
        # Registrar log de alterações
        if "log" in user_data:
            # Se já existir um histórico de logs, adicionar o novo log
            if "logs" in existing_user:
                update_data["logs"] = existing_user["logs"] + [user_data["log"]]
            else:
                update_data["logs"] = [user_data["log"]]
        
        # Adicionar informações sobre a alteração
        if tipo_usuario_alterado:
            if "logs" not in update_data:
                update_data["logs"] = existing_user.get("logs", [])
            
            update_data["logs"].append({
                "changedBy": current_user.get("nome", "Admin"),
                "changedAt": datetime.now().isoformat(),
                "changes": {
                    "tipo_usuario": {
                        "from": existing_user.get("tipo_usuario"),
                        "to": update_data["tipo_usuario"]
                    }
                }
            })
        
        # Atualizar o usuário
        await db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        # Retornar o usuário atualizado
        updated_user = await db["users"].find_one({"_id": ObjectId(user_id)})
        result = parse_obj_id(updated_user)
        
        # Adicionar informações para o frontend
        result["info"] = {
            "tipo_usuario_alterado": tipo_usuario_alterado
        }
        
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Erro ao atualizar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar usuário: {str(e)}"
        )

# Rota para obter logs de alterações de um usuário (apenas para admins)
@router.get("/usuarios/{user_id}/logs", response_model=List[dict])
async def get_user_logs(user_id: str, db=Depends(database.get_db), current_user=Depends(get_current_user)):
    # Verificar se o usuário atual é admin
    if current_user.get("tipo_usuario") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para administradores"
        )
    
    # Verificar se o usuário existe
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Retornar logs se existirem
    return user.get("logs", [])