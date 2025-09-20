from fastapi import APIRouter, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT , HTTP_404_NOT_FOUND
from schema.user_schema import UserSchema, UserResponse, UserLoginSchema
#from config.db import conn  
from config.db import engine 
from model.users import users  # Importamos el modelo de usuarios
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from typing import List, Dict
from pydantic import BaseModel
from typing import Optional
from schema.user_schema import UserUpdateSchema

user = APIRouter()

@user.get("/")
def root():
    return {"hola": "ya estamos dentro del router"}


    
    
@user.put("/api/user/{id}", response_model=UserResponse)
async def update_user(id: int, user: UserSchema):
    """
    PUT = Actualiza todos los campos del usuario
    """
    # Aquí iría tu lógica de actualización en BD
    return {**user.dict(), "id": id}

# PATCH USUARIO
# Esta ruta actualiza algunos datos en la base de datos
@user.patch("/api/user/{id}", response_model=UserResponse)
def patch_user(user_id: int, data_user: UserUpdateSchema):
    with engine.connect() as conn:
        # Verificar si existe
        existing = conn.execute(users.select().where(users.c.id == user_id)).fetchone()
        if not existing:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )

        # Solo actualizamos lo que venga en el body
        update_data = data_user.model_dump(exclude_unset=True)

        if "password" in update_data:
            from werkzeug.security import generate_password_hash
            update_data["password"] = generate_password_hash(update_data["password"], "pbkdf2:sha256:30", 30)

        conn.execute(
            users.update()
            .where(users.c.id == user_id)
            .values(**update_data)
        )
        conn.commit()

        # Retornar el usuario actualizado
        updated = conn.execute(users.select().where(users.c.id == user_id)).fetchone()
        return dict(updated._mapping)




# C REAR USUARIO
# Esta ruta crea un nuevo usuario en la base de datos
@user.post("/api/user", response_model=UserResponse, status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:  # Usamos el contexto para manejar la conexión
        new_user = data_user.model_dump()
        new_user["password"] = generate_password_hash(data_user.password, "pbkdf2:sha256:30", 30)

        result = conn.execute(users.insert().values(new_user))
        conn.commit()  # ← esto es obligatorio
        new_id = result.lastrowid
        new_user["id"] = new_id
    return new_user  # Devolver el usuario creado


# Esta ruta permite a un usuario iniciar sesión
# Verifica las credenciales y devuelve los datos del usuario si son correctas
@user.post("/api/user/login", response_model=UserResponse, status_code=HTTP_200_OK)
def login_user(data_user: UserLoginSchema):    
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.email == data_user.email)).fetchone()

        if result is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        if not check_password_hash(result.password, data_user.password):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Contraseña incorrecta"
            )

        # Si llega aquí, credenciales son correctas
        return {
            "id": result.id,
            "name": result.name,
            "email": result.email,
            "rol": result.rol
        }
                    
            
      
        
        
        

# R EAD ONE USUARIO
# Esta ruta obtiene un usuario por su ID
@user.get("/api/user/{user_id}", response_model=UserResponse, status_code=HTTP_200_OK)
def get_user(user_id: int):
    with engine.connect() as conn:
        row = conn.execute(users.select().where(users.c.id == user_id)).fetchone()

        if row is None:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )

        return dict(row._mapping)  # Esto extrae directamente el resultado como dict





# R EAD ALL USERS
# Esta ruta obtiene todos los usuarios de la base de datos
@user.get("/api/users", response_model=list[UserResponse])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select())
        columns = result.keys()
        rows = result.fetchall()

        users_list = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            row_dict.pop("password", None)
            users_list.append(row_dict)

    return users_list



# U PDATE ONE USER
# Esta ruta actualiza un usuario por su ID  
@user.put("/api/user/{user_id}", response_model=UserResponse, status_code=HTTP_200_OK)
def update_user(user_id: int, data_user: UserSchema):
    with engine.connect() as conn:  # Usamos el contexto para manejar la conexión
        new_user = data_user.model_dump()
        new_user["password"] = generate_password_hash(data_user.password, "pbkdf2:sha256:30", 30)
        
        conn.execute(
            users.update()
            .where(users.c.id == user_id)
            .values(new_user)
        )
        conn.commit()
    return new_user
    


# D ELETE ONE USER
# Esta ruta elimina un usuario por su ID
@user.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    with engine.connect() as conn:  # Usamos el contexto para manejar la conexión
        cursor = conn.execute(users.select().where(users.c.id == user_id))
        rows = cursor.fetchall()

        
        if not rows:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        
        # Si existe, proceder a eliminar
        conn.execute(
            users.delete()
            .where(users.c.id == user_id)
        )
        conn.commit()

