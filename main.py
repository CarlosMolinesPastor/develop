import flet as ft
import os

from pyfiglet import Figlet
import subprocess

from flet_core.colors import BLACK, WHITE


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
    base_color = ft.colors.RED_400
    categories_color = ft.colors.BLACK87
    page.bgcolor = page_color

    ##Items##
    page.appbar = ft.AppBar(
        title=ft.Text("arch_developers :)", color=WHITE, expand=True, size=20),
        leading=ft.Icon(ft.icons.HOME, color=WHITE),
        bgcolor=base_color,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Credits"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="EXIT",
                        checked=False,
                        on_click=lambda: print("checked"),
                    ),
                ]
            ),
        ],
    )

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

    def compb_apps_check(e):
        list_app = []
        if vscode.value:
            list_app.append("visual-studio-code-bin")
        if neovim.value:
            list_app.append("neovim")
        if zed.value:
            list_app.append("zed")
        if geany.value:
            list_app.append("geany geany-plugins")
        if sublime.value:
            list_app.append("sublime-text-4")
        if bluefish.value:
            list_app.append("bluefish")
        if lapce.value:
            list_app.append("lapce")
        if list_app:
            # Creamos de la lista un string con los nombres de las apps
            comand = " ".join(list_app)
            execute_command(comand)
            print(comand)
        else:
            print("No apps selected")

    def openTerminal(e):
        os.system("xterm -e 'bash -c \"python3 --version; bash\" '")

    My_Cmmnd = "sudo pacman -Syy && yay -S --noconfirm --needed"
    # My_Cmmnd2 = str(list_app)

    def execute_command(e):
        if list:
            process = (
                subprocess.Popen(
                    "xfce4-terminal -e 'bash -c \"" + My_Cmmnd + " " + e + ";bash\"' ",
                    stdout=subprocess.PIPE,
                    stderr=None,
                    shell=True,
                ),
            )
        else:
            print("No apps selected")

    codetxt = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    ft.Column(
                        [
                            ft.Text(
                                "select and install whatever you want",
                                color=ft.colors.WHITE,
                                size=20,
                            ),
                            ft.Text(
                                "instalation_mode",
                                color=ft.colors.WHITE,
                                size=10,
                                text_align=ft.TextAlign.RIGHT,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    height=75,
                    padding=5,
                    border_radius=ft.border_radius.all(15),
                    # bgcolor=ft.colors.BLACK,
                    alignment=ft.alignment.center,
                ),
                ft.Row(
                    [
                        ft.Container(
                            ft.Text("editors", color=ft.colors.WHITE, size=18),
                            height=150,
                            width=180,
                            padding=5,
                            border_radius=ft.border_radius.all(15),
                            bgcolor=categories_color,
                            alignment=ft.alignment.center,
                        ),
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
                                    ft.ElevatedButton(
                                        text="Install Editors",
                                        color=ft.colors.WHITE,
                                        bgcolor=base_color,
                                        height=60,
                                        width=170,
                                        on_click=compb_apps_check,
                                    ),
                                ],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            expand=True,
                            adaptive=True,
                            height=150,
                            width=510,
                            padding=15,
                            border_radius=ft.border_radius.all(15),
                            bgcolor=categories_color,
                            alignment=ft.alignment.center,
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Container(
                            ft.Text("tecnologies", color=ft.colors.WHITE, size=18),
                            height=150,
                            width=180,
                            padding=10,
                            border_radius=ft.border_radius.all(15),
                            bgcolor=categories_color,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            git,
                                            node,
                                            mongo,
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
                                    ft.ElevatedButton(
                                        text="Install tecnologies",
                                        color=ft.colors.WHITE,
                                        bgcolor=base_color,
                                        height=60,
                                        width=170,
                                        on_click=lambda: page.window_close,
                                    ),
                                ],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            expand=True,
                            adaptive=True,
                            height=150,
                            padding=15,
                            border_radius=ft.border_radius.all(15),
                            bgcolor=categories_color,
                            alignment=ft.alignment.center,
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Container(
                            ft.Text("others", color=ft.colors.WHITE, size=18),
                            height=150,
                            width=180,
                            padding=10,
                            border_radius=ft.border_radius.all(15),
                            bgcolor=categories_color,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Column(
                                        [lazyvim, homebrew, docker],
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
                                    ft.ElevatedButton(
                                        text="Install others",
                                        color=ft.colors.WHITE,
                                        bgcolor=base_color,
                                        height=60,
                                        width=170,
                                        on_click=lambda: page.window_close,
                                    ),
                                ],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            expand=True,
                            adaptive=True,
                            height=150,
                            padding=15,
                            border_radius=ft.border_radius.all(15),
                            bgcolor=categories_color,
                            alignment=ft.alignment.center,
                        ),
                    ],
                ),
            ],
        ),
        alignment=ft.alignment.center,
        margin=10,
        padding=15,
        bgcolor=base_color,
        border_radius=ft.border_radius.all(30),
    )
    buttons = ft.Container(
        ft.Row(
            [
                ft.ElevatedButton(
                    text="Exit",
                    color=ft.colors.WHITE,
                    bgcolor=base_color,
                    height=60,
                    width=280,
                    on_click=lambda: page.window_close,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.END,
        ),
        margin=10,
    )

    page.add(codetxt)
    page.add(buttons)


ft.app(main)
