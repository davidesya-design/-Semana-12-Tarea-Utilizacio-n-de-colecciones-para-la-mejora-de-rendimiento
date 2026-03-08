from modelos.libro import Libro
from modelos.usuario import Usuario
from servicios.biblioteca_servicio import BibliotecaServicio
from pathlib import Path


ARCHIVO_LIBROS = Path(__file__).resolve().parent.parent / "libros.txt"


def mostrar_menu_principal() -> None:
    # Menu principal del programa.
    print("\n=== Biblioteca Digital ===")
    print("1. Gestion de libros")
    print("2. Gestion de usuarios")
    print("3. Prestamos y devoluciones")
    print("4. Busquedas y listados")
    print("0. Salir")


def mostrar_submenu_libros() -> None:
    print("\n--- Gestion de libros ---")
    print("1. Anadir libro")
    print("2. Quitar libro")
    print("3. Listar libros disponibles")
    print("0. Volver")


def mostrar_submenu_usuarios() -> None:
    print("\n--- Gestion de usuarios ---")
    print("1. Registrar usuario")
    print("2. Dar de baja usuario")
    print("3. Listar usuarios")
    print("0. Volver")


def mostrar_submenu_prestamos() -> None:
    print("\n--- Prestamos y devoluciones ---")
    print("1. Prestar libro")
    print("2. Devolver libro")
    print("3. Listar libros prestados de un usuario")
    print("0. Volver")


def mostrar_submenu_busquedas() -> None:
    print("\n--- Busquedas y listados ---")
    print("1. Buscar por titulo")
    print("2. Buscar por autor")
    print("3. Buscar por categoria")
    print("0. Volver")


def leer_no_vacio(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El valor no puede estar vacio.")


def mostrar_libros(libros: list[Libro]) -> None:
    if not libros:
        print("No se encontraron libros.")
        return

    for libro in libros:
        print(libro)


def mostrar_usuarios(usuarios: list[Usuario]) -> None:
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    for usuario in usuarios:
        print(usuario)


def menu_libros(servicio: BibliotecaServicio) -> None:
    while True:
        mostrar_submenu_libros()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "0":
            break

        if opcion == "1":
            libro = Libro(
                leer_no_vacio("Titulo: "),
                leer_no_vacio("Autor: "),
                leer_no_vacio("Categoria: "),
                leer_no_vacio("ISBN: "),
            )
            print(servicio.agregar_libro(libro))
        elif opcion == "2":
            print(servicio.quitar_libro(leer_no_vacio("ISBN del libro a quitar: ")))
        elif opcion == "3":
            mostrar_libros(servicio.listar_libros_disponibles())
        else:
            print("Opcion invalida. Intente nuevamente.")


def menu_usuarios(servicio: BibliotecaServicio) -> None:
    while True:
        mostrar_submenu_usuarios()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "0":
            break

        if opcion == "1":
            usuario = Usuario(
                leer_no_vacio("Nombre del usuario: "),
                leer_no_vacio("ID del usuario: "),
            )
            print(servicio.registrar_usuario(usuario))
        elif opcion == "2":
            print(servicio.dar_baja_usuario(leer_no_vacio("ID del usuario a dar de baja: ")))
        elif opcion == "3":
            mostrar_usuarios(servicio.listar_usuarios())
        else:
            print("Opcion invalida. Intente nuevamente.")


def menu_prestamos(servicio: BibliotecaServicio) -> None:
    while True:
        mostrar_submenu_prestamos()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "0":
            break

        if opcion == "1":
            print(
                servicio.prestar_libro(
                    leer_no_vacio("ID del usuario: "),
                    leer_no_vacio("ISBN del libro: "),
                )
            )
        elif opcion == "2":
            print(
                servicio.devolver_libro(
                    leer_no_vacio("ID del usuario: "),
                    leer_no_vacio("ISBN del libro: "),
                )
            )
        elif opcion == "3":
            mostrar_libros(servicio.listar_libros_usuario(leer_no_vacio("ID del usuario: ")))
        else:
            print("Opcion invalida. Intente nuevamente.")


def menu_busquedas(servicio: BibliotecaServicio) -> None:
    while True:
        mostrar_submenu_busquedas()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "0":
            break

        if opcion == "1":
            mostrar_libros(servicio.buscar_por_titulo(leer_no_vacio("Titulo a buscar: ")))
        elif opcion == "2":
            mostrar_libros(servicio.buscar_por_autor(leer_no_vacio("Autor a buscar: ")))
        elif opcion == "3":
            mostrar_libros(servicio.buscar_por_categoria(leer_no_vacio("Categoria a buscar: ")))
        else:
            print("Opcion invalida. Intente nuevamente.")


def ejecutar_menu() -> None:
    # main.py solo inicia el sistema y muestra menus.
    servicio = BibliotecaServicio()
    servicio.cargar_libros_desde_archivo(str(ARCHIVO_LIBROS))

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opcion: ").strip()

        try:
            if opcion == "1":
                menu_libros(servicio)
            elif opcion == "2":
                menu_usuarios(servicio)
            elif opcion == "3":
                menu_prestamos(servicio)
            elif opcion == "4":
                menu_busquedas(servicio)
            elif opcion == "0":
                print("Hasta luego.")
                break
            else:
                print("Opcion invalida. Intente nuevamente.")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    ejecutar_menu()
