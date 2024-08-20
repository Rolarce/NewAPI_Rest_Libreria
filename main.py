from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Modelo para un libro
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    anio_publicacion: Optional[int] = None
    isbn: Optional[str] = None

# Base de datos simulada
libros_db = []

# Ruta de prueba
@app.get("/")
def raiz():
    return {"mensaje": "Bienvenido a la API_REST de Libros"}


@app.post("/libros/", response_model=Libro)
def crear_libro(libro: Libro):
    # Verifica si el libro ya existe
    for l in libros_db:
        if l.id == libro.id:
            raise HTTPException(status_code=400, detail="El libro ya existe")
    libros_db.append(libro)
    return libro


#Define una ruta para obtener todos los libros.
@app.get("/libros/", response_model=List[Libro])
def leer_libros():
    return libros_db

#obtener un libro específico por su ID.
@app.get("/libros/{libro_id}", response_model=Libro)
def leer_libro(libro_id: int):
    for libro in libros_db:
        if libro.id == libro_id:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

#Define una ruta para actualizar un libro existente.
@app.put("/libros/{libro_id}", response_model=Libro)
def actualizar_libro(libro_id: int, libro_actualizado: Libro):
    for index, libro in enumerate(libros_db):
        if libro.id == libro_id:
            libros_db[index] = libro_actualizado
            return libro_actualizado
    raise HTTPException(status_code=404, detail="Libro no encontrado")

#Define una ruta para eliminar un libro
@app.delete("/libros/{libro_id}", response_model=dict)
def eliminar_libro(libro_id: int):
    for index, libro in enumerate(libros_db):
        if libro.id == libro_id:
            libros_db.pop(index)
            return {"detalle": "Libro eliminado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")




    