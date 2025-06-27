import flet as ft
import os
import subprocess
import shutil
import threading

from shlex import quote

BLACK = ft.Colors.BLACK
WHITE = ft.Colors.WHITE

######### PACMAN LIBRARIES ######
# Thanks https://github.com/peakwinter/python-pacman/tree/master

__PACMAN_BIN = shutil.which("pacman")  # default to use the system's pacman binary


def get_bin():
    # Return the current pacman binary being used.
    return __PACMAN_BIN


def set_bin(path):
    # Set a custom pacman binary.
    # If the pacman binary is set to an AUR helper, this module may also be used to interact with AUR.
    global __PACMAN_BIN
    if isinstance(path, str) and (
        os.path.isfile(path) or os.path.isfile(shutil.which(path))  # type: ignore
    ):
        __PACMAN_BIN = shutil.which(path)
    else:
        raise IOError("This executable does not exist.")


def pacman(flags, pkgs=[], eflgs=[], pacman_bin=__PACMAN_BIN):
    # Subprocess wrapper, get all data"""
    if not pkgs:
        cmd = [pacman_bin, "--noconfirm", flags]
    elif type(pkgs) is list:
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
    page.window.min_height = 600
    page.window.min_width = 800

    ##### Colors #####
    page_color = ft.Colors.GREY_300
    base_color = ft.Colors.RED_300
    page.bgcolor = page_color

    # SALIDA DE Text
    output_text = ft.Text(value="", selectable=True, color=BLACK)

    # Image
    img = ft.Image(
        src=f"./images/logo_develop.png",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
    )

    # Logo
    img_l = ft.Image(
        src=f"./images/logo_develop.png",
        width=150,
        height=150,
        fit=ft.ImageFit.CONTAIN,
    )

    ################ Dialogs ###############

    ####### Dialog EDITORS #######

    # Dialog to install editors and close dialog
    def close_dlg_editor_and_install(e):
        dlg_editor.open = False
        print("Dialog closed")
        install_editors(e)
        page.update()

    # Dialog to close dialog
    def close_dlg_editor(e):
        dlg_editor.open = False
        print("Dialog closed")
        page.update()

    # Dialog to open dialog
    def open_dlg_editor(e):
        page.floating_action_button
        page.dialog = dlg_editor
        dlg_editor.open = True
        print("Dialog opened")
        page.update()

    ####### Dialog TECNOLOGIES ########

    def close_dlg_tecn_and_install(e):
        dlg_tecn.open = False
        print("Dialog closed")
        install_tecnologies(e)
        page.update()

    def close_dlg_tecn(e):
        dlg_tecn.open = False
        print("Dialog closed")
        page.update()

    def open_dlg_tecn(e):
        page.dialog = dlg_tecn
        dlg_tecn.open = True
        print("Dialog opened")
        page.update()

    ######## Dialog OTHERS ########

    def close_dlg_other_and_install(e):
        dlg_other.open = False
        print("Dialog other closed and install")
        install_other(e)
        page.update()

    def close_dlg_other(e):
        dlg_other.open = False
        print("Dialog other closed")
        page.update()

    def open_dlg_other(e):
        page.dialog = dlg_other
        dlg_other.open = True
        print("Dialog opened")
        page.update()

    ######## Dialog CREDITS ########

    # Dialog to open credits dialog
    def open_dlg_credits(e):
        page.overlay.append(dlg_credits)
        dlg_credits.open = True
        print("Dialog opened")
        page.update()

    def close_dlg_credits(e):
        dlg_credits.open = False
        print("Dialog closed")
        page.update()

    ######## Dialog REQUERIMENTS #######

    def close_dlg_yay(e):
        dlg_install_yay.open = False
        print("Dialog closed")
        page.update()

    def close_dlg_yay_install(e):
        dlg_install_yay.open = False
        print("Dialog closed")
        exec_install_yay()
        page.update()

    def open_dlg_yay():
        page.dialog = dlg_install_yay
        dlg_install_yay.open = True
        print("Dialog opened")
        page.update()

    ####### Dialog INSTALLED #######

    def open_dlg_installed():
        page.dialog = dlg_installed
        dlg_installed.open = True
        print("Dialog installed open")
        page.update()

    def close_dlg_installed(e):
        dlg_installed.open = False
        print("Dialog installed close")
        page.update()

    ####### Brute Dialogs #######

    dlg_installed = ft.AlertDialog(
        modal=True,
        title=ft.Text("ALERT"),
        content=ft.Text("Item installed or not selected"),
        actions=[
            ft.TextButton(text="Accept", on_click=close_dlg_installed),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=print("Dialog dismissed"),
    )

    dlg_editor = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please Confirm"),
        content=ft.Text("Do you want to install the selected editors?"),
        actions=[
            ft.TextButton(text="Cancel", on_click=close_dlg_editor),
            ft.TextButton(text="Install", on_click=close_dlg_editor_and_install),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=print("Dialog dismissed"),
    )

    dlg_tecn = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please Confirm"),
        content=ft.Text("Do you want to install the selected tecnologies?"),
        actions=[
            ft.TextButton(text="Cancel", on_click=close_dlg_tecn),
            ft.TextButton(text="Install", on_click=close_dlg_tecn_and_install),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=print("Dialog dismissed"),
    )

    dlg_other = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please Confirm"),
        content=ft.Text("Do you want to install the selected items?"),
        actions=[
            ft.TextButton(text="Cancel", on_click=close_dlg_other),
            ft.TextButton(text="Install", on_click=close_dlg_other_and_install),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=print("Dialog dismissed"),
    )

    def open_github(e):
        page.launch_url("https://github.com/CarlosMolinesPastor/develop")

    dlg_credits = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Credits",
            color=base_color,
        ),
        content=ft.Column(
            [
                img_l,
                ft.Text(
                    "This applications is made with love by karlinux to learn and improve the flet and python language",
                    color=base_color,
                ),
                ft.Text(
                    "The project is open source and you can contribute to it through the following link:",
                    color=base_color,
                ),
                ft.TextButton(
                    text="https://github.com/CarlosMolinesPastor/develop",
                    on_click=open_github,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        actions=[
            ft.TextButton(text="Accept", on_click=close_dlg_credits),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=print("Dialog dismissed"),
    )

    dlg_install_yay = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please Confirm"),
        content=ft.Text(
            "You havent install yay and it is necessary for continues, Do you wat to continue with installation?"
        ),
        actions=[
            ft.TextButton(text="Cancel", on_click=close_dlg_yay),
            ft.TextButton(text="Install", on_click=close_dlg_yay_install),
        ],
        on_dismiss=print("Dialog dismissed"),
    )

    ################## CHECKBOX ##################

    # Universal
    blank = ft.Checkbox(
        label="blank",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
    )

    # Editors
    vscode = ft.Checkbox(
        label="vscode",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Multiplatform code editor for Microsoft",
    )
    neovim = ft.Checkbox(
        label="neovim",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Vim-fork focused on extensibility and usability",
    )
    zed = ft.Checkbox(
        label="zed",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Zed is a fully offline-capable, open-source text and code editor for power users",
    )
    geany = ft.Checkbox(
        label="geany",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Geany is a small and lightweight Integrated Development Environment",
    )
    sublime = ft.Checkbox(
        label="sublime text4",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Sublime Text is a sophisticated text editor for code, markup, and prose",
    )
    bluefish = ft.Checkbox(
        label="bluefish",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Bluefish is a powerful editor for experienced web designers and programmers",
    )
    lapce = ft.Checkbox(
        label="lapce",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Lapce is a code editor Multiplatform with a focus on performance and ease of use",
    )
    pycharm = ft.Checkbox(
        label="pycharm",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="PyCharm is the best IDE I've ever used. With PyCharm, you can work with Python, Django, and other frameworks",
    )
    intellij = ft.Checkbox(
        label="intellij",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="IntelliJ IDEA is a powerful Java integrated development environment (IDE) for developing computer software",
    )
    clion = ft.Checkbox(
        label="clion",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="CLion is a cross-platform IDE for C and C++",
    )
    rider = ft.Checkbox(
        label="rider",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Rider is a cross-platform .NET IDE based on the IntelliJ platform and ReSharper",
    )
    monodevelop = ft.Checkbox(
        label="monodevelop",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="MonoDevelop is a cross-platform IDE primarily designed for C# and other .NET languages",
    )
    androidstudio = ft.Checkbox(
        label="android-studio",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Android Studio is the official integrated development environment for Google's Android operating system",
    )
    gnomebuilder = ft.Checkbox(
        label="gnome-builder",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="GNOME Builder is an open-source IDE that is focused on creating an easy-to-use development environment for GNOME",
    )
    gedit = ft.Checkbox(
        label="gedit",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="gedit is the official text editor of the GNOME desktop environment",
    )
    eclipse = ft.Checkbox(
        label="eclipse",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Eclipse is an integrated development environment (IDE) used in computer programming",
    )
    arduino_ide = ft.Checkbox(
        label="arduino",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Arduino IDE is an open-source software that is mainly used for writing and uploading code in Arduino boards",
    )

    # Tecnologies
    git = ft.Checkbox(
        label="git",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Git is a distributed version-control system for tracking changes in source code during software development",
    )
    node = ft.Checkbox(
        label="nodejs",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Node.js is an open-source, cross-platform, back-end JavaScript runtime environment that runs on the V8 engine and executes JavaScript code outside a web browser",
    )
    mongo = ft.Checkbox(
        label="mongo/compass",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="MongoDB is a source-available cross-platform document-oriented database program. Classified as a NoSQL database program, MongoDB uses JSON-like documents with optional schemas",
    )
    mysql = ft.Checkbox(
        label="mysql",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="MySQL is an open-source relational database management system",
    )
    mariadb = ft.Checkbox(
        label="mariaDB",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="MariaDB is a community-developed, commercially supported fork of the MySQL relational database management system",
    )
    postgre = ft.Checkbox(
        label="postgreSQL",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="postgreSQL is a source-available cross-platform document-oriented database program.",
    )
    phpMyAdmin = ft.Checkbox(
        label="phpMyAdmin",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="phpMyAdmin is a free and open-source administration tool for MySQL and MariaDB",
    )
    mysql_workbench = ft.Checkbox(
        label="mysql-workbench",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="MySQL Workbench is a unified visual tool by Oracle for database architects, developers, and DBAs",
    )
    sqlitebrowser = ft.Checkbox(
        label="sqlitebrowser",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="DB Browser for SQLite is a high quality, visual, open-source tool to create, design, and edit database files compatible with SQLite",
    )
    mysql_clients = ft.Checkbox(
        label="mysql-clients",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="MySQL Workbench is a unified visual tool by Oracle for database architects, developers, and DBAs",
    )
    python = ft.Checkbox(
        label="python",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Python is an interpreted high-level general-purpose programming language",
    )
    rust = ft.Checkbox(
        label="rust",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Rust is a multi-paradigm system programming language focused on safety, especially safe concurrency",
    )
    java = ft.Checkbox(
        label="java",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Java is a class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible",
    )
    flutter = ft.Checkbox(
        label="flutter",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Flutter is an open-source UI software development kit created by Google",
    )
    docker = ft.Checkbox(
        label="docker",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers",
    )
    unity = ft.Checkbox(
        label="unity",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Unity is a cross-platform game engine developed by Unity Technologies",
    )
    godot = ft.Checkbox(
        label="godot",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Godot Engine is a feature-packed, cross-platform game engine to create 2D and 3D games from a unified interface",
    )
    godot_mono = ft.Checkbox(
        label="godot-mono",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Godot Engine is a feature-packed, this version is a mono version",
    )
    pixelorama = ft.Checkbox(
        label="pixelorama",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Pixelorama is a free and open-source sprite editor for pixel art",
    )

    # Others
    rb_neovim = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(
                    value="lazyvim",
                    label="lazyvim",
                    label_style=ft.TextStyle(color=WHITE),
                    fill_color=ft.Colors.WHITE,
                    tooltip="LazyVim is a simple and easy-to-use text editor that is designed to be fast and lightweight",
                ),
                ft.Radio(
                    value="nvchad",
                    label="nvchad",
                    label_style=ft.TextStyle(color=WHITE),
                    fill_color=ft.Colors.WHITE,
                    tooltip="NvChad is a Neovim configuration that takes the best of Vim and Emacs",
                ),
                ft.Radio(
                    value="astrovim",
                    label="astrovim",
                    label_style=ft.TextStyle(color=WHITE),
                    fill_color=ft.Colors.WHITE,
                    tooltip="AstroVim is a set of configurations for Neovim that aims to be a good starting point for anyone using Neovim",
                ),
            ],
        ),
    )

    penpot = ft.Checkbox(
        label="penpot",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Penpot is the first Open Source design and prototyping platform meant for cross-domain teams",
    )
    figma = ft.Checkbox(
        label="figma",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Figma is a vector graphics editor and prototyping tool which is primarily web-based",
    )
    pencil = ft.Checkbox(
        label="pencil",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Pencil is a free and open-source GUI prototyping tool that is quick, easy, and works across multiple platforms",
    )
    draw = ft.Checkbox(
        label="draw.io",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Draw.io is a free online diagram software for making flowcharts, process diagrams, org charts, UML, ER and network diagrams",
    )
    umlet = ft.Checkbox(
        label="umlet",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="UMLET is a free UML tool for fast UML diagrams",
    )
    umbrello = ft.Checkbox(
        label="umbrello",
        label_style=ft.TextStyle(color=WHITE),
        fill_color=WHITE,
        check_color=BLACK,
        tooltip="Umbrello UML Modeller is a Unified Modelling Language diagram program for KDE",
    )

    ################# FUNCTIONS ##################

    # Return True if the specified package is installed
    def is_installed(package):
        # Return True if the specified package is installed
        return pacman("-Q", package)["code"] == 0

    ###### function EDITORS #######
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
        if pycharm.value and not is_installed("pycharm-community-edition"):
            list_app.append("pycharm-community-edition")
        if intellij.value and not is_installed("intellij-idea-community-edition"):
            list_app.append("intellij-idea-community-edition")
        if rider.value and not is_installed("rider"):
            list_app.append("rider")
        if clion.value and not is_installed("clion"):
            list_app.append("clion")
        if monodevelop.value and not is_installed("monodevelop-bin"):
            list_app.append("monodevelop-bin")
        if androidstudio.value and not is_installed("android-studio"):
            list_app.append("android-studio")
        if gnomebuilder.value and not is_installed("gnome-builder"):
            list_app.append("gnome-builder")
        if gedit.value and not is_installed("gedit"):
            list_app.append("gedit gedit-plugins")
        if arduino_ide.value and not is_installed("arduino-ide"):
            list_app.append("arduino-ide")
        if eclipse.value and not is_installed("eclipse-java"):
            list_app.append("eclipse-java")

        if list_app:
            # make a string with the list of editors
            list_editors = " ".join(list_app)  # .replace(" ", "")
            exec_install_editors(
                list_editors
            )  # call the function to install the editors
            print(list_editors)
        else:
            open_dlg_installed()
            print(
                "Editor installed o not select"
            )  # if the list is empty print the message

    ###### function TECNOLOGIES #######
    def install_tecnologies(e):
        list_app = []
        if git.value and is_installed("git"):
            list_app.append("git")
        if node.value and not is_installed("node"):
            list_app.append("node npm")
        if mongo.value and not is_installed("mongodb-bin"):
            list_app.append("mongodb-bin mongosh-bin mongodb-tools mongodb-compass")
        if mysql.value and not is_installed("mysql"):
            list_app.append("mysql")
        if mariadb.value and not is_installed("mariadb"):
            list_app.append("mariadb")
        if postgre.value and not is_installed("postgresql"):
            list_app.append("postgresql")
        if phpMyAdmin.value and not is_installed("phpmyadmin"):
            list_app.append("phpmyadmin")
        if mysql_workbench.value and not is_installed("mysql-workbench"):
            list_app.append("mysql-workbench")
        if mysql_clients.value and not is_installed("mysql-clients"):
            list_app.append("mysql-clients")
        if sqlitebrowser.value and not is_installed("sqlitebrowser"):
            list_app.append("sqlitebrowser")
        if python.value and not is_installed("python"):
            list_app.append("python")
        if rust.value and not is_installed("rust"):
            list_app.append("rust")
        if java.value and not is_installed("jdk-openjdk"):
            list_app.append("jdk-openjdk")
        if flutter.value and not is_installed("flutter-bin"):
            list_app.append("flutter-bin google-chrome")
        if docker.value and not is_installed("docker"):
            list_app.append("docker docker-compose")
        if unity.value and not is_installed("unityhub"):
            list_app.append("unityhub")
        if godot.value and not is_installed("godot"):
            list_app.append("godot")
        if godot_mono.value and not is_installed("godot-mono"):
            list_app.append("godot-mono")
        if pixelorama.value and not is_installed("pixelorama"):
            list_app.append("pixelorama")

        if list_app:
            list_tecn = " ".join(list_app)
            exec_install_tecn(list_tecn)
        else:
            open_dlg_installed()
            print("Tecnologies installed or not selected")

    ###### function OTHERS #######
    def install_other(e):
        list_app = []
        if rb_neovim.value == "lazyvim":
            list_app.append("lazyvim")
        if rb_neovim.value == "nvchad":
            list_app.append("nvchad")
        if rb_neovim.value == "astrovim":
            list_app.append("astrovim")
        if penpot.value and not is_installed("penpot"):
            list_app.append("penpot")
        if figma.value and not is_installed("figma"):
            list_app.append("figma-linux")
        if pencil.value and not is_installed("pencil"):
            list_app.append("pencil")
        if draw.value and not is_installed("drawio-desktop"):
            list_app.append("drawio-desktop")
        if umlet.value and not is_installed("umlet"):
            list_app.append("umlet")
        if umbrello.value and not is_installed("umbrello"):
            list_app.append("umbrello")

        if list_app:
            list_others = " ".join(list_app)
            exec_install_others(list_others)
        else:
            open_dlg_installed()
            print("Others installed or not selected")

    ####### COMMANDS ########

    install_command = "sudo pacman -Syy && yay -S --noconfirm --needed"
    install_yay = "sudo pacman -S --noconfirm --needed base-devel git && git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si --noconfirm"
    add_user_flutter = "sudo usermod -a -G flutter $USER && echo $USER"
    add_user_docker = "sudo usermod -a -G docker $USER && echo $USER"
    lazyvim_command = "mv ~/.config/nvim{,.bak} && mv ~/.local/share/nvim{,.bak} && mv ~/.local/state/nvim{,.bak} && mv ~/.cache/nvim{,.bak} && git clone https://github.com/LazyVim/starter ~/.config/nvim && rm -rf ~/.config/nvim/.git"

    ######## INSTALL FUNCIONS  SIN TERMINAL########
    def exec_install_editors(list_editors):
        if list_editors:
            command = install_command + " " + list_editors

            def run():
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    text=True,
                )
                output = ""
                if process.stdout is not None:
                    for line in process.stdout:
                        output += line
                        print(
                            line, end=""
                        )  # Puedes actualizar un widget Flet aquí si lo deseas
                    process.wait()
                if process.returncode == 0:
                    print("Instalación completada correctamente.")
                else:
                    print("Error durante la instalación.")

            threading.Thread(target=run, daemon=True).start()
        else:
            print("Editors installed or not selected")

    def exec_install_tecn(list_tecn):
        if not list_tecn:
            print("Not list")
            return

        if "flutter-bin" in list_tecn and "docker" in list_tecn:
            command = (
                install_command
                + " "
                + list_tecn
                + " && "
                + add_user_flutter
                + " && "
                + add_user_docker
            )
        elif "flutter-bin" in list_tecn:
            command = install_command + " " + list_tecn + " && " + add_user_flutter
        elif "docker" in list_tecn:
            command = install_command + " " + list_tecn + " && " + add_user_docker
        else:
            command = install_command + " " + list_tecn

        def run():
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
            )
            output = ""
            if process.stdout is not None:
                for line in process.stdout:
                    output += line
                    print(
                        line, end=""
                    )  # Puedes actualizar un widget Flet aquí si lo deseas
                process.wait()
            if process.returncode == 0:
                print("Instalación completada correctamente.")
            else:
                print("Error durante la instalación.")

        threading.Thread(target=run, daemon=True).start()

    def exec_install_others(list_others):
        if not list_others:
            print("Not list")
            return

        if "lazyvim" in list_others and (
            "penpot" in list_others or "figma" in list_others
        ):
            command = install_command + " " + list_others + " && " + lazyvim_command
        elif "lazyvim" in list_others:
            command = lazyvim_command
        else:
            command = install_command + " " + list_others

        def run():
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
            )
            output = ""
            if process.stdout is not None:
                for line in process.stdout:
                    output += line
                    print(
                        line, end=""
                    )  # Puedes actualizar un widget Flet aquí si lo deseas
                process.wait()
            if process.returncode == 0:
                print("Instalación completada correctamente.")
            else:
                print("Error durante la instalación.")

        threading.Thread(target=run, daemon=True).start()

    ######### Check Yay #########

    def compr_yay():
        print("Compr se esta ejecutando")
        if not is_installed("yay"):
            print("yay is not installed")
            open_dlg_yay()
        else:
            print("Yay installed")

    def exec_install_yay():
        def run():
            process = subprocess.Popen(
                install_yay,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
                text=True,
            )
            output = ""
            if process.stdout is not None:
                for line in process.stdout:
                    output += line
                    print(
                        line, end=""
                    )  # Puedes actualizar un widget Flet aquí si lo deseas
                process.wait()
            if process.returncode == 0:
                print("Instalación de yay completada correctamente.")
            else:
                print("Error durante la instalación de yay.")

        threading.Thread(target=run, daemon=True).start()

    ############## ROUTE CHANGE ###############

    ###### PRINCIPAL ######
    def route_change(route):
        # Borramos las vistas si hubiera alguna
        page.views.clear()
        page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.RED_300))

        # Comprobe if yay is installed
        threading.Timer(2.0, compr_yay).start()

        ########  HOME ########
        # Anadimos la vista principal con la ruta slash y añadimos los controles de la pagina: un appbar
        # y dos botones elevados, uno para añadir productos y otro para buscar por fecha
        page.views.append(
            # Creamos la vista con la ruta slash
            ft.View(
                "/",
                # Añadimos los controles de la pagina
                [
                    ft.AppBar(
                        title=ft.Text("arch_develop :)", color=WHITE),
                        bgcolor=ft.Colors.RED_300,
                        actions=[  # type: ignore
                            ft.IconButton(
                                ft.Icons.CODE,
                                icon_color=WHITE,
                                on_click=open_dlg_credits,
                            )
                        ],
                    ),
                    img,
                    ft.ElevatedButton(
                        "text editors",
                        bgcolor=ft.Colors.RED_300,
                        color=ft.Colors.WHITE,
                        height=60,
                        width=350,
                        on_click=lambda _: page.go("/text_editors"),
                    ),
                    ft.ElevatedButton(
                        "tecnologies",
                        bgcolor=ft.Colors.RED_300,
                        color=ft.Colors.WHITE,
                        height=60,
                        width=350,
                        on_click=lambda _: page.go("/tecnologies"),
                    ),
                    ft.ElevatedButton(
                        "others",
                        bgcolor=ft.Colors.RED_300,
                        color=ft.Colors.WHITE,
                        height=60,
                        width=350,
                        on_click=lambda _: page.go("/others"),
                    ),
                    # ft.ElevatedButton(
                    #     "exit",
                    #     bgcolor=ft.Colors.RED_300,
                    #     color=ft.Colors.WHITE,
                    #     height=60,
                    #     width=350,
                    #     on_click=page.window_destroy,
                    # ),
                ],
                # Alineamos los controles en el centro de la pagina
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=24,
                padding=20,
            )
        )

        ######## EDITORS ########
        if page.route == "/text_editors":
            # Añadimos la vista con el AppBar y un botón para volver a la vista anterior
            (
                page.views.append(
                    ft.View(
                        "/text_editors",
                        [  # type: ignore
                            ft.AppBar(
                                title=ft.Text("text_editors :)", color=WHITE),
                                bgcolor=ft.Colors.RED_300,
                                color=WHITE,
                                actions=[  # type: ignore
                                    ft.IconButton(
                                        ft.Icons.CODE,
                                        on_click=open_dlg_credits,
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
                                                                geany,
                                                            ],
                                                            width=150,
                                                        ),
                                                        ft.Column(
                                                            [
                                                                sublime,
                                                                bluefish,
                                                                lapce,
                                                                monodevelop,
                                                            ],
                                                            width=150,
                                                        ),
                                                        ft.Column(
                                                            [
                                                                intellij,
                                                                clion,
                                                                rider,
                                                                pycharm,
                                                            ],
                                                            width=150,
                                                        ),
                                                        ft.Column(
                                                            [
                                                                androidstudio,
                                                                gnomebuilder,
                                                                gedit,
                                                                arduino_ide,
                                                            ],
                                                            width=150,
                                                        ),
                                                        ft.Column(
                                                            [
                                                                eclipse,
                                                            ],
                                                            width=150,
                                                        ),
                                                    ],
                                                    scroll=ft.ScrollMode.AUTO,
                                                ),
                                                expand=True,
                                                adaptive=True,
                                                # height=150,
                                                # width=510,
                                                padding=15,
                                                border_radius=ft.border_radius.all(15),
                                                bgcolor=base_color,
                                            ),
                                        ],
                                    ),
                                    ft.ElevatedButton(
                                        "install",
                                        bgcolor=base_color,
                                        color=ft.Colors.WHITE,
                                        on_click=open_dlg_editor,
                                    ),
                                ],
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=24,
                        padding=20,
                    )
                ),
            )
        page.update()

        ######## TECNOLOGIES #######
        if page.route == "/tecnologies":
            # Añadimos la vista con el AppBar y un botón para volver a la vista anterior
            (
                page.views.append(
                    ft.View(
                        "/tecnologies",
                        [  # type: ignore
                            ft.AppBar(
                                title=ft.Text("tecnologies :)", color=WHITE),
                                bgcolor=ft.Colors.RED_300,
                                color=WHITE,
                                actions=[  # type: ignore
                                    ft.IconButton(
                                        ft.Icons.CODE,
                                        on_click=open_dlg_credits,
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
                                                                git,
                                                                node,
                                                                docker,
                                                            ],
                                                            width=150,
                                                        ),
                                                        ft.Container(
                                                            ft.Column(
                                                                [
                                                                    ft.Text(
                                                                        "languages",
                                                                        color=WHITE,
                                                                        text_align=ft.TextAlign.CENTER,
                                                                    ),
                                                                    rust,
                                                                    java,
                                                                    python,
                                                                    flutter,
                                                                ],
                                                                width=150,
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                            ),
                                                            bgcolor=ft.Colors.GREEN_600,
                                                            border_radius=ft.border_radius.all(
                                                                15
                                                            ),
                                                            padding=15,
                                                        ),
                                                        ft.Container(
                                                            ft.Column(
                                                                [
                                                                    ft.Text(
                                                                        "game mode",
                                                                        color=WHITE,
                                                                        text_align=ft.TextAlign.CENTER,
                                                                    ),
                                                                    unity,
                                                                    godot,
                                                                    godot_mono,
                                                                    pixelorama,
                                                                ],
                                                                width=150,
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                            ),
                                                            bgcolor=ft.Colors.GREY_600,
                                                            border_radius=ft.border_radius.all(
                                                                15
                                                            ),
                                                            padding=15,
                                                        ),
                                                        ft.Container(
                                                            ft.Column(
                                                                [
                                                                    ft.Text(
                                                                        "data base",
                                                                        color=WHITE,
                                                                        text_align=ft.TextAlign.CENTER,
                                                                    ),
                                                                    ft.Row(
                                                                        [
                                                                            ft.Column(
                                                                                [
                                                                                    phpMyAdmin,
                                                                                    mysql,
                                                                                    mysql_clients,
                                                                                    mysql_workbench,
                                                                                ],
                                                                            ),
                                                                            ft.Column(
                                                                                [
                                                                                    postgre,
                                                                                    mongo,
                                                                                    mariadb,
                                                                                    sqlitebrowser,
                                                                                ]
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ],
                                                                width=320,
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                            ),
                                                            bgcolor=ft.Colors.ORANGE_900,
                                                            border_radius=ft.border_radius.all(
                                                                15
                                                            ),
                                                            padding=15,
                                                        ),
                                                    ],
                                                    scroll=ft.ScrollMode.AUTO,
                                                ),
                                                expand=True,
                                                adaptive=True,
                                                # height=150,
                                                # width=510,
                                                padding=15,
                                                border_radius=ft.border_radius.all(15),
                                                bgcolor=base_color,
                                            ),
                                        ],
                                    ),
                                    ft.ElevatedButton(
                                        "install",
                                        bgcolor=base_color,
                                        color=ft.Colors.WHITE,
                                        on_click=open_dlg_tecn,
                                    ),
                                ],
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=24,
                        padding=20,
                    )
                ),
            )
        page.update()

        ######## OTHERS ########
        if page.route == "/others":
            # Añadimos la vista con el AppBar y un botón para volver a la vista anterior
            (
                page.views.append(
                    ft.View(
                        "/others",
                        [  # type: ignore
                            ft.AppBar(
                                title=ft.Text("others :)", color=WHITE),
                                bgcolor=ft.Colors.RED_300,
                                color=WHITE,
                                actions=[  # type: ignore
                                    ft.IconButton(
                                        ft.Icons.CODE,
                                        on_click=open_dlg_credits,
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
                                                        ft.Container(
                                                            ft.Column(
                                                                [
                                                                    ft.Text(
                                                                        "neovim",
                                                                        color=WHITE,
                                                                        text_align=ft.TextAlign.CENTER,
                                                                    ),
                                                                    rb_neovim,
                                                                ],
                                                                width=150,
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                            ),
                                                            bgcolor=ft.Colors.GREY_600,
                                                            border_radius=ft.border_radius.all(
                                                                15
                                                            ),
                                                            padding=15,
                                                        ),
                                                        ft.Container(
                                                            ft.Column(
                                                                [
                                                                    ft.Text(
                                                                        "design tools",
                                                                        color=WHITE,
                                                                        text_align=ft.TextAlign.CENTER,
                                                                    ),
                                                                    ft.Row(
                                                                        [
                                                                            ft.Column(
                                                                                [
                                                                                    penpot,
                                                                                    figma,
                                                                                    pencil,
                                                                                ],
                                                                            ),
                                                                            ft.Column(
                                                                                [
                                                                                    draw,
                                                                                    umlet,
                                                                                    umbrello,
                                                                                ]
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ],
                                                                width=220,
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                            ),
                                                            bgcolor=ft.Colors.GREEN,
                                                            border_radius=ft.border_radius.all(
                                                                15
                                                            ),
                                                            padding=15,
                                                        ),
                                                        ft.Column(
                                                            [
                                                                blank,
                                                                blank,
                                                                blank,
                                                                blank,
                                                            ],
                                                            width=150,
                                                        ),
                                                        ft.Column(
                                                            [
                                                                blank,
                                                                blank,
                                                                blank,
                                                                blank,
                                                            ],
                                                            width=150,
                                                        ),
                                                    ],
                                                    scroll=ft.ScrollMode.AUTO,
                                                ),
                                                expand=True,
                                                adaptive=True,
                                                padding=15,
                                                border_radius=ft.border_radius.all(15),
                                                bgcolor=base_color,
                                            ),
                                        ],
                                    ),
                                    ft.ElevatedButton(
                                        "install",
                                        bgcolor=base_color,
                                        color=ft.Colors.WHITE,
                                        on_click=open_dlg_other,
                                    ),
                                ],
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=24,
                        padding=20,
                    )
                ),
            )
            page.update()

    page.update()

    # Funcion para volver a la vista anterior, anadimos la vista pop,
    # le decimos que la vista anterior sea la vista -1,
    # y le indicamos que vaya a la ruta
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        if top_view.route is not None:
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
