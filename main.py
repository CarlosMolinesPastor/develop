import flet as ft
import os

from pyfiglet import Figlet
import subprocess, os, shutil
from urllib import request
from shlex import quote

from flet_core.colors import BLACK, WHITE

######### PACMAN LIBRARIES ######
# Thanks https://github.com/peakwinter/python-pacman/tree/master

__PACMAN_BIN = shutil.which("pacman")  # default to use the system's pacman binary


def get_bin():
    """
    Return the current pacman binary being used.
    """
    return __PACMAN_BIN


def set_bin(path):
    """
    Set a custom pacman binary.
    If the pacman binary is set to an AUR helper, this module may also be used to interact with AUR.
    """
    global __PACMAN_BIN
    if isinstance(path, str) and (
        os.path.isfile(path) or os.path.isfile(shutil.which(path))
    ):
        __PACMAN_BIN = shutil.which(path)
    else:
        raise IOError("This executable does not exist.")


def pacman(flags, pkgs=[], eflgs=[], pacman_bin=__PACMAN_BIN):
    """Subprocess wrapper, get all data"""
    if not pkgs:
        cmd = [pacman_bin, "--noconfirm", flags]
    elif type(pkgs) == list:
        cmd = [pacman_bin, "--noconfirm", flags]
        cmd += [quote(s) for s in pkgs]
    else:
        cmd = [pacman_bin, "--noconfirm", flags, pkgs]
    if eflgs and any(eflgs):
        eflgs = [x for x in eflgs if x]
        cmd += eflgs
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    data = p.communicate()
    data = {
        "code": p.returncode,
        "stdout": data[0].decode(),
        "stderr": data[1].rstrip(b"\n").decode(),
    }
    return data


################ MAIN #################


def main(page: ft.Page):
    page.platform = ft.PagePlatform.LINUX
    page.title = "ArchDevelopers"
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_min_height = 600
    page.window_min_width = 800

    ##### Colors #####
    page_color = ft.colors.GREY_300
    base_color = ft.colors.RED_300
    categories_color = ft.colors.BLACK87
    page.bgcolor = page_color

    #### Checkbox ########
    # Editors
    vscode = ft.Checkbox(
        label="vscode",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    neovim = ft.Checkbox(
        label="neovim",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    zed = ft.Checkbox(
        label="zed",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    geany = ft.Checkbox(
        label="geany",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    sublime = ft.Checkbox(
        label="sublime text4",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    bluefish = ft.Checkbox(
        label="bluefish",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    lapce = ft.Checkbox(
        label="lapce",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )

    # Tecnologies
    git = ft.Checkbox(
        label="git",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    node = ft.Checkbox(
        label="nodejs",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    mongo = ft.Checkbox(
        label="mongo/compass",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    # Others
    lazyvim = ft.Checkbox(
        label="lazyvim",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    homebrew = ft.Checkbox(
        label="homebrew",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )
    docker = ft.Checkbox(
        label="docker",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )

    def checkbox_cleared():
        # Clear all checkboxes
        for checkbox in [
            vscode,
            neovim,
            zed,
            geany,
            sublime,
            bluefish,
            lapce,
            git,
            node,
            mongo,
            lazyvim,
            homebrew,
            docker,
        ]:
            checkbox.clear()

    def is_installed(package):
        # Return True if the specified package is installed
        return pacman("-Q", package)["code"] == 0

    def install_editors(e):
        list_app = []
        if vscode.value and not is_installed("visual-studio-code-bin"):
            list_app.append("visual-studio-code-bin")
        if neovim.value and not is_installed("neovim"):
            list_app.append("neovim")
        if zed.value and not is_installed("zed"):
            list_app.append("zed")
        if geany.value and not is_installed("geany"):
            list_app.append("geany geany-plugins")
        if sublime.value and not is_installed("sublime-text"):
            list_app.append("sublime-text-4")
        if bluefish.value and not is_installed("bluefish"):
            list_app.append("bluefish")
        if lapce.value and not is_installed("lapce"):
            list_app.append("lapce")
        if list_app:
            # Creamos de la lista un string con los nombres de las apps
            list_editors = " ".join(list_app)
            exec_install_editors(list_editors)
            print(list_editors)
        else:
            print("Editor installed o not select")

    def openTerminal(e):
        os.system("xterm -e 'bash -c \"python3 --version; bash\" '")

    My_Cmmnd = "sudo pacman -Syy && yay -S --noconfirm --needed"
    # My_Cmmnd2 = str(list_app)

    def exec_install_editors(list_editors):
        if list_editors:
            process = (
                subprocess.Popen(
                    "xfce4-terminal -e 'bash -c \"" + My_Cmmnd + " " + list_editors + ";bash\"' ",
                    stdout=subprocess.PIPE,
                    stderr=None,
                    shell=True,
                ),
            )
        else:
            print("Editors installed or not selected")

    # ####### ROUTE CHANGE ########
    def route_change(route):

        # Borramos las vistas si hubiera alguna
        page.views.clear()
        page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.RED_300))

        # #######  HOME ########
        # Anadimos la vista principal con la ruta slash y añadimos los controles de la pagina: un appbar
        # y dos botones elevados, uno para añadir productos y otro para buscar por fecha
        page.views.append(
            # Creamos la vista con la ruta slash
            ft.View(
                "/",
                # Añadimos los controles de la pagina
                [
                    ft.AppBar(
                        title=ft.Text("arch_develop :)", color=WHITE), bgcolor=ft.colors.RED_300
                    ),
                    ft.ElevatedButton(
                        "text editors",
                        bgcolor=ft.colors.RED_300,
                        color=ft.colors.WHITE,
                        height=60,
                        width=350,
                        on_click=lambda _: page.go("/text_editors"),
                    ),
                    ft.ElevatedButton(
                        "tecnologies",
                        bgcolor=ft.colors.RED_300,
                        color=ft.colors.WHITE,
                        height=60,
                        width=350,
                        on_click=lambda _: page.go("/tecnologies"),
                    ),
                    ft.ElevatedButton(
                        "others",
                        bgcolor=ft.colors.RED_300,
                        color=ft.colors.WHITE,
                        height=60,
                        width=350,
                        on_click=lambda _: page.go("/others"),
                    ),
                ],
                # Alineamos los controles en el centro de la pagina
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=24,
            )
        )
        if page.route == "/text_editors":
            # Añadimos la vista con el AppBar y un botón para volver a la vista anterior
            page.views.append(
                ft.View(
                    "/text_editors",
                    [
                        ft.AppBar(
                            title=ft.Text("text_editors :)"),
                            bgcolor=ft.colors.RED_300,
                            actions=[
                                ft.IconButton(
                                    ft.icons.HOME,
                                    on_click=lambda _: page.go("/"),
                                )
                            ],
                        ),
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Container(
                                            ft.Row(
                                                [
                                                    ft.Column(
                                                        [
                                                            vscode,
                                                            neovim,
                                                            zed,
                                                        ],
                                                        width=150,
                                                    ),
                                                    ft.Column(
                                                        [
                                                            geany,
                                                            sublime,
                                                            bluefish,
                                                        ],
                                                        width=150,
                                                    ),
                                                    ft.Column(
                                                        [
                                                            lapce,
                                                            sublime,
                                                            bluefish,
                                                        ],
                                                        width=150,
                                                    ),
                                                ],
                                                scroll=ft.ScrollMode.AUTO,
                                            ),
                                            expand=True,
                                            adaptive=True,
                                            #height=150,
                                            #width=510,
                                            padding=15,
                                            border_radius=ft.border_radius.all(15),
                                            bgcolor=base_color,
                                        ),
                                    ],
                                ),
                                ft.ElevatedButton(
                                    "install",
                                    bgcolor=base_color,
                                    color=ft.colors.WHITE,
                                    on_click=install_editors,
                                ),
                            ],
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=24,
                    padding=20,
                )
            ),
            page.update(),
        page.update()

    page.update()

    # Funcion para volver a la vista anterior, anadimos la vista pop,
    # le decimos que la vista anterior sea la vista -1,
    # y le indicamos que vaya a la ruta
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Unimos los cambios con las funciones, es decir cuando cambia
    # la ruta le asignamos la funcion de route_change,
    # cuando queremos ir hacia atras la funcion view_pop,
    # y cuando clikamos nos desplazamos a la ruta
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


# Iniciamos la app
ft.app(main)
