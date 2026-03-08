class Libro:
    """Representa un libro dentro del catalogo de la biblioteca."""

    def __init__(self, titulo: str, autor: str, categoria: str, isbn: str) -> None:
        if not titulo.strip():
            raise ValueError("El titulo no puede estar vacio.")
        if not autor.strip():
            raise ValueError("El autor no puede estar vacio.")
        if not categoria.strip():
            raise ValueError("La categoria no puede estar vacia.")
        if not isbn.strip():
            raise ValueError("El ISBN no puede estar vacio.")

        # Titulo y autor se guardan en una tupla.
        self.__titulo_autor = (titulo.strip(), autor.strip())
        self.__categoria = categoria.strip()
        self.__isbn = isbn.strip()

    @property
    def titulo_autor(self) -> tuple[str, str]:
        return self.__titulo_autor

    @property
    def titulo(self) -> str:
        return self.__titulo_autor[0]

    @property
    def autor(self) -> str:
        return self.__titulo_autor[1]

    @property
    def categoria(self) -> str:
        return self.__categoria

    @property
    def isbn(self) -> str:
        return self.__isbn

    def __str__(self) -> str:
        return (
            f"ISBN: {self.__isbn} | Titulo: {self.titulo} | "
            f"Autor: {self.autor} | Categoria: {self.__categoria}"
        )
