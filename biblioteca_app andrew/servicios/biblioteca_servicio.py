from __future__ import annotations

from pathlib import Path

from modelos.libro import Libro
from modelos.usuario import Usuario


class BibliotecaServicio:
    """Centraliza la logica del catalogo, usuarios, prestamos y carga de libros."""

    def __init__(self) -> None:
        # ISBN -> Libro disponible.
        self.__libros_disponibles: dict[str, Libro] = {}
        # Guarda todos los libros del sistema.
        self.__catalogo_general: dict[str, Libro] = {}
        self.__usuarios: dict[str, Usuario] = {}
        # Set para IDs unicos de usuarios.
        self.__ids_usuarios: set[str] = set()
        # ISBN -> ID del usuario que tiene el libro.
        self.__prestamos: dict[str, str] = {}
        self.__ruta_libros: Path | None = None

    def cargar_libros_desde_archivo(self, ruta_archivo: str) -> None:
        # Carga los libros desde el archivo de texto.
        ruta = Path(ruta_archivo)
        self.__ruta_libros = ruta

        if not ruta.exists():
            ruta.touch()
            return

        self.__libros_disponibles.clear()
        self.__catalogo_general.clear()

        for linea in ruta.read_text(encoding="utf-8").splitlines():
            if not linea.strip():
                continue

            datos = [dato.strip() for dato in linea.split("|")]
            if len(datos) != 4:
                continue

            titulo, autor, categoria, isbn = datos
            libro = Libro(titulo, autor, categoria, isbn)
            self.__catalogo_general[libro.isbn] = libro
            if libro.isbn not in self.__prestamos:
                self.__libros_disponibles[libro.isbn] = libro

    def agregar_libro(self, libro: Libro) -> str:
        if libro.isbn in self.__catalogo_general:
            raise ValueError("Ya existe un libro registrado con ese ISBN.")

        self.__catalogo_general[libro.isbn] = libro
        self.__libros_disponibles[libro.isbn] = libro
        self.__guardar_libros_en_archivo()
        return "Libro anadido correctamente."

    def quitar_libro(self, isbn: str) -> str:
        isbn = isbn.strip()
        if isbn in self.__prestamos:
            raise ValueError("No se puede quitar un libro que esta prestado.")
        if isbn not in self.__libros_disponibles:
            raise ValueError("No existe un libro disponible con ese ISBN.")

        del self.__libros_disponibles[isbn]
        del self.__catalogo_general[isbn]
        self.__guardar_libros_en_archivo()
        return "Libro eliminado correctamente."

    def registrar_usuario(self, usuario: Usuario) -> str:
        if usuario.usuario_id in self.__ids_usuarios:
            raise ValueError("El ID de usuario ya esta registrado.")

        self.__usuarios[usuario.usuario_id] = usuario
        self.__ids_usuarios.add(usuario.usuario_id)
        return "Usuario registrado correctamente."

    def dar_baja_usuario(self, usuario_id: str) -> str:
        usuario = self.__obtener_usuario(usuario_id)
        if usuario.libros_prestados:
            raise ValueError("No se puede dar de baja a un usuario con libros prestados.")

        del self.__usuarios[usuario.usuario_id]
        self.__ids_usuarios.remove(usuario.usuario_id)
        return "Usuario dado de baja correctamente."

    def prestar_libro(self, usuario_id: str, isbn: str) -> str:
        usuario = self.__obtener_usuario(usuario_id)
        isbn = isbn.strip()

        if isbn in self.__prestamos:
            raise ValueError("El libro ya se encuentra prestado.")

        libro = self.__libros_disponibles.get(isbn)
        if libro is None:
            raise ValueError("No existe un libro disponible con ese ISBN.")

        usuario.agregar_prestamo(isbn)
        self.__prestamos[isbn] = usuario.usuario_id
        del self.__libros_disponibles[isbn]
        return "Prestamo realizado correctamente."

    def devolver_libro(self, usuario_id: str, isbn: str) -> str:
        usuario = self.__obtener_usuario(usuario_id)
        isbn = isbn.strip()

        if not usuario.tiene_prestado(isbn):
            raise ValueError("Ese usuario no tiene prestado el libro indicado.")

        libro = self.__catalogo_general.get(isbn)
        if libro is None:
            raise ValueError("No se encontro el libro en el catalogo general.")

        usuario.remover_prestamo(isbn)
        del self.__prestamos[isbn]
        self.__libros_disponibles[isbn] = libro
        return "Libro devuelto correctamente."

    def buscar_por_titulo(self, titulo: str) -> list[Libro]:
        criterio = titulo.strip().lower()
        return [
            libro for libro in self.__catalogo_general.values() if criterio in libro.titulo.lower()
        ]

    def buscar_por_autor(self, autor: str) -> list[Libro]:
        criterio = autor.strip().lower()
        return [
            libro for libro in self.__catalogo_general.values() if criterio in libro.autor.lower()
        ]

    def buscar_por_categoria(self, categoria: str) -> list[Libro]:
        criterio = categoria.strip().lower()
        return [
            libro
            for libro in self.__catalogo_general.values()
            if criterio in libro.categoria.lower()
        ]

    def listar_libros_usuario(self, usuario_id: str) -> list[Libro]:
        usuario = self.__obtener_usuario(usuario_id)
        return [self.__catalogo_general[isbn] for isbn in usuario.libros_prestados]

    def listar_libros_disponibles(self) -> list[Libro]:
        return list(self.__libros_disponibles.values())

    def listar_usuarios(self) -> list[Usuario]:
        return list(self.__usuarios.values())

    def __obtener_usuario(self, usuario_id: str) -> Usuario:
        usuario = self.__usuarios.get(usuario_id.strip())
        if usuario is None:
            raise ValueError("No existe un usuario con ese ID.")
        return usuario

    def __guardar_libros_en_archivo(self) -> None:
        if self.__ruta_libros is None:
            return

        # Guarda el catalogo actualizado en el archivo.
        lineas = [
            f"{libro.titulo}|{libro.autor}|{libro.categoria}|{libro.isbn}"
            for libro in self.__catalogo_general.values()
        ]
        self.__ruta_libros.write_text("\n".join(lineas), encoding="utf-8")
