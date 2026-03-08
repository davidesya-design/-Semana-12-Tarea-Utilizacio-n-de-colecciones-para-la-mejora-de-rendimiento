class Usuario:
    """Representa a un usuario registrado y sus libros prestados."""

    def __init__(self, nombre: str, usuario_id: str) -> None:
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacio.")
        if not usuario_id.strip():
            raise ValueError("El ID de usuario no puede estar vacio.")

        self.__nombre = nombre.strip()
        self.__usuario_id = usuario_id.strip()
        # Los libros prestados se guardan en una lista.
        self.__libros_prestados: list[str] = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def usuario_id(self) -> str:
        return self.__usuario_id

    @property
    def libros_prestados(self) -> list[str]:
        return list(self.__libros_prestados)

    def agregar_prestamo(self, isbn: str) -> None:
        if isbn not in self.__libros_prestados:
            self.__libros_prestados.append(isbn)

    def remover_prestamo(self, isbn: str) -> None:
        if isbn in self.__libros_prestados:
            self.__libros_prestados.remove(isbn)

    def tiene_prestado(self, isbn: str) -> bool:
        return isbn in self.__libros_prestados

    def __str__(self) -> str:
        return f"ID: {self.__usuario_id} | Nombre: {self.__nombre}"
