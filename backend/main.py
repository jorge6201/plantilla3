# Esta es una aplicacion basica que utiliza FastAPI para crear una API restful.
from fastapi import FastAPI
from router.router import user # Importamos el router que hemos creado
from fastapi.middleware.cors import CORSMiddleware




# Creamos una instancia de FastAPI
app = FastAPI(debug=True)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción mejor poner ["http://localhost:5500"] o tu dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app = FastAPI(docs_url=None, redoc_url=None)  # Deshabilitamos la documentacion de la API  

# Incluimos el router en la aplicacion
app.include_router(user)


