import flet as ft
import os
import subprocess
import shutil
import threading
from shlex import quote

# Constants
BLACK = ft.Colors.BLACK
WHITE = ft.Colors.WHITE
BASE_COLOR = ft.Colors.RED_300
PAGE_COLOR = ft.Colors.GREY_300

# Pacman Configuration
PACMAN_BIN = shutil.which("pacman")  # Defínelo fuera de la clase, sin doble guion bajo

class PacmanManager:
    @staticmethod
    def get_bin():
        return PACMAN_BIN

    @staticmethod
    def set_bin(path):
        global PACMAN_BIN
        found = shutil.which(path)
        if isinstance(path, str) and (os.path.isfile(path) or (found is not None and os.path.isfile(found))):
            PACMAN_BIN = found if found is not None else path
        else:
            raise IOError("This executable does not exist.")

    @staticmethod
    def pacman(flags, pkgs=None, eflgs=None, pacman_bin=None):
        if pkgs is None:
            pkgs = []
        if eflgs is None:
            eflgs = []
        if pacman_bin is None:
            pacman_bin = PACMAN_BIN
        if not pkgs:
            cmd = [pacman_bin, "--noconfirm", flags]
        elif isinstance(pkgs, list):
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

    @staticmethod
    def is_installed(package):
        return PacmanManager.pacman("-Q", [package])["code"] == 0

class InstallationManager:
    def __init__(self, page):
        self.page = page
        self.password = None
        self.output_text = ft.Text(value="", selectable=True, color=BLACK)
        
    def set_password(self, password):
        self.password = password
        
    def verify_password(self):
        if not self.password:
            return False
        try:
            proc = subprocess.Popen(
                ['sudo', '-S', 'true'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate(self.password + '\n')
            return proc.returncode == 0
        except:
            return False
        
    def execute_command(self, command, success_message="Instalación completada correctamente", error_message="Error durante la instalación"):
        if not self.verify_password():
            self.show_error("Contraseña de sudo inválida o no configurada")
            return False
            
        def run():
            try:
                process = subprocess.Popen(
                    ['sudo', '-S'] + command.split(),
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                output = ""
                if process.stdout is not None:
                    for line in process.stdout:
                        output += line
                        self.update_output(line)
                
                process.wait()
                
                if process.returncode == 0:
                    self.update_output(f"\n{success_message}\n")
                else:
                    if process.stderr is not None:
                        error_output = process.stderr.read()
                        self.update_output(f"\n{error_message}\nError: {error_output}\n")
                    else:
                        error_output = ""
            except Exception as e:
                self.update_output(f"\nError: {str(e)}\n")
                
        threading.Thread(target=run, daemon=True).start()
        return True
        
    def update_output(self, text):
        self.output_text.value += text
        self.page.update()
        
    def show_error(self, message):
        self.update_output(f"\nERROR: {message}\n")

class DialogManager:
    def __init__(self, page, installation_manager):
        self.page = page
        self.installation_manager = installation_manager
        self.password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
        self.password_error = ft.Text(value="", color=ft.Colors.RED_400)
        
        # Create dialogs
        self.dlg_password = self._create_password_dialog()
        self.dlg_editor = self._create_confirmation_dialog(
            "Confirmar", 
            "¿Desea instalar los editores seleccionados?",
            None
        )
        self.dlg_tecn = self._create_confirmation_dialog(
            "Confirmar", 
            "¿Desea instalar las tecnologías seleccionadas?",
            None
        )
        self.dlg_other = self._create_confirmation_dialog(
            "Confirmar", 
            "¿Desea instalar los elementos seleccionados?",
            None
        )
        self.dlg_installed = self._create_info_dialog(
            "Información", 
            "Elemento ya instalado o no seleccionado"
        )
        self.dlg_install_yay = self._create_confirmation_dialog(
            "Confirmar", 
            "No tiene yay instalado y es necesario. ¿Desea instalarlo ahora?",
            None
        )
        
    def _create_password_dialog(self):
        def on_password_submit(e):
            password = self.password_field.value
            self.installation_manager.set_password(password)
            if self.installation_manager.verify_password():
                self.password_error.value = ""
                self.close_dialog(self.dlg_password)
                # Execute pending action if exists
                if self.pending_action is not None:
                    if hasattr(self, 'pending_action'):
                        self.pending_action()
                        delattr(self, 'pending_action')
                    else:
                        self.password_error.value = "Contraseña incorrecta"
            self.page.update()
            
        return ft.AlertDialog(
            modal=True,
            title=ft.Text("Contraseña de sudo"),
            content=ft.Column([
                self.password_field,
                self.password_error
            ]),
            actions=[
                ft.TextButton("Aceptar", on_click=on_password_submit),
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(self.dlg_password)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
    def _create_confirmation_dialog(self, title, content, callback):
        return ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.close_dialog(self.dlg_editor)),
                ft.TextButton("Instalar", on_click=lambda e: self._on_install_click(callback)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
    def _create_info_dialog(self, title, content):
        return ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.close_dialog(self.dlg_installed)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
    def _on_install_click(self, callback):
        self.close_dialog(self.dlg_editor)
        if not self.installation_manager.password:
            self.pending_action = callback
            self.open_dialog(self.dlg_password)
        else:
            callback()
        
    def open_dialog(self, dialog):
        if dialog not in self.page.overlay:
            self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
        
    def close_dialog(self, dialog):
        dialog.open = False
        self.page.update()

class CheckboxManager:
    def __init__(self):
        self.editors = self._create_editor_checkboxes()
        self.technologies = self._create_technology_checkboxes()
        self.others = self._create_other_controls()
        
    def _create_checkbox(self, label, tooltip=""):
        return ft.Checkbox(
            label=label,
            label_style=ft.TextStyle(color=WHITE),
            fill_color=WHITE,
            check_color=BLACK,
            tooltip=tooltip
        )
        
    def _create_editor_checkboxes(self):
        return {
            "vscode": self._create_checkbox("vscode", "Editor de código multiplataforma de Microsoft"),
            "neovim": self._create_checkbox("neovim", "Fork de Vim enfocado en extensibilidad y usabilidad"),
            "zed": self._create_checkbox("zed", "Editor de texto y código open-source totalmente offline"),
            "geany": self._create_checkbox("geany", "IDE pequeño y liviano"),
            "sublime": self._create_checkbox("sublime text4", "Editor de texto sofisticado"),
            "bluefish": self._create_checkbox("bluefish", "Editor potente para diseñadores web y programadores"),
            "lapce": self._create_checkbox("lapce", "Editor de código con enfoque en rendimiento"),
            "pycharm": self._create_checkbox("pycharm", "IDE para Python"),
            "intellij": self._create_checkbox("intellij", "IDE Java potente"),
            "clion": self._create_checkbox("clion", "IDE multiplataforma para C y C++"),
            "rider": self._create_checkbox("rider", "IDE .NET multiplataforma"),
            "monodevelop": self._create_checkbox("monodevelop", "IDE multiplataforma para .NET"),
            "androidstudio": self._create_checkbox("android-studio", "IDE oficial para Android"),
            "gnomebuilder": self._create_checkbox("gnome-builder", "IDE open-source para GNOME"),
            "gedit": self._create_checkbox("gedit", "Editor de texto oficial de GNOME"),
            "eclipse": self._create_checkbox("eclipse", "Entorno de desarrollo integrado"),
            "arduino_ide": self._create_checkbox("arduino", "IDE para programar placas Arduino"),
        }
        
    def _create_technology_checkboxes(self):
        return {
            "git": self._create_checkbox("git", "Sistema de control de versiones distribuido"),
            "node": self._create_checkbox("nodejs", "Entorno de ejecución para JavaScript"),
            "mongo": self._create_checkbox("mongo/compass", "Programa de base de datos MongoDB"),
            "mysql": self._create_checkbox("mysql", "Sistema de gestión de bases de datos relacional"),
            "mariadb": self._create_checkbox("mariaDB", "Fork de MySQL desarrollado por la comunidad"),
            "postgre": self._create_checkbox("postgreSQL", "Sistema de base de datos PostgreSQL"),
            "phpMyAdmin": self._create_checkbox("phpMyAdmin", "Herramienta de administración para MySQL/MariaDB"),
            "mysql_workbench": self._create_checkbox("mysql-workbench", "Herramienta visual para MySQL"),
            "sqlitebrowser": self._create_checkbox("sqlitebrowser", "Navegador de bases de datos SQLite"),
            "mysql_clients": self._create_checkbox("mysql-clients", "Clientes para MySQL"),
            "python": self._create_checkbox("python", "Lenguaje de programación Python"),
            "rust": self._create_checkbox("rust", "Lenguaje de programación Rust"),
            "java": self._create_checkbox("java", "Lenguaje de programación Java"),
            "flutter": self._create_checkbox("flutter", "Kit de herramientas UI de Google"),
            "docker": self._create_checkbox("docker", "Plataforma para contenedores"),
            "unity": self._create_checkbox("unity", "Motor de juegos Unity"),
            "godot": self._create_checkbox("godot", "Motor de juegos Godot"),
            "godot_mono": self._create_checkbox("godot-mono", "Motor Godot con soporte Mono"),
            "pixelorama": self._create_checkbox("pixelorama", "Editor de sprites para pixel art"),
        }
        
    def _create_other_controls(self):
        return {
            "rb_neovim": ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value="lazyvim", label="lazyvim", label_style=ft.TextStyle(color=WHITE)),
                    ft.Radio(value="nvchad", label="nvchad", label_style=ft.TextStyle(color=WHITE)),
                    ft.Radio(value="astrovim", label="astrovim", label_style=ft.TextStyle(color=WHITE)),
                ])
            ),
            "penpot": self._create_checkbox("penpot", "Plataforma de diseño y prototipado open-source"),
            "figma": self._create_checkbox("figma", "Editor de gráficos vectoriales y herramienta de prototipado"),
            "pencil": self._create_checkbox("pencil", "Herramienta de prototipado GUI"),
            "draw": self._create_checkbox("draw.io", "Software de diagramas online gratuito"),
            "umlet": self._create_checkbox("umlet", "Herramienta UML gratuita"),
            "umbrello": self._create_checkbox("umbrello", "Modelador UML para KDE"),
        }

class AppUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self._setup_page()
        self.checkbox_manager = CheckboxManager()
        self.installation_manager = InstallationManager(page)
        self.dialog_manager = DialogManager(page, self.installation_manager)
        self._setup_ui()
        
    def _setup_page(self):
        self.page.platform = ft.PagePlatform.LINUX
        self.page.title = "ArchDevelopers"
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window.min_height = 600
        self.page.window.min_width = 800
        self.page.bgcolor = PAGE_COLOR
        
    def _setup_ui(self):
        self.img = ft.Image(
            src=f"./images/logo_develop.png",
            width=200,
            height=200,
            fit=ft.ImageFit.CONTAIN,
        )
        
        self.img_l = ft.Image(
            src=f"./images/logo_develop.png",
            width=150,
            height=150,
            fit=ft.ImageFit.CONTAIN,
        )
        
        self._setup_routes()
        
    def _setup_routes(self):
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go(self.page.route)
        
    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        if top_view.route is not None:
            self.page.go(top_view.route)
            
    def route_change(self, route):
        self.page.views.clear()
        self.page.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=BASE_COLOR))
        
        # Home view
        self.page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        title=ft.Text("arch_develop :)", color=WHITE),
                        bgcolor=BASE_COLOR,
                        actions=[
                            ft.IconButton(
                                ft.Icons.CODE,
                                icon_color=WHITE,
                                on_click=self.open_credits_dialog,
                            )
                        ],
                    ),
                    self.img,
                    ft.ElevatedButton(
                        "Editores de texto",
                        bgcolor=BASE_COLOR,
                        color=WHITE,
                        height=60,
                        width=350,
                        on_click=lambda _: self.page.go("/text_editors"),
                    ),
                    ft.ElevatedButton(
                        "Tecnologías",
                        bgcolor=BASE_COLOR,
                        color=WHITE,
                        height=60,
                        width=350,
                        on_click=lambda _: self.page.go("/technologies"),
                    ),
                    ft.ElevatedButton(
                        "Otros",
                        bgcolor=BASE_COLOR,
                        color=WHITE,
                        height=60,
                        width=350,
                        on_click=lambda _: self.page.go("/others"),
                    ),
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=24,
                padding=20,
            )
        )
        
        # Editors view
        if self.page.route == "/text_editors":
            self._create_editors_view()
            
        # Technologies view
        if self.page.route == "/technologies":
            self._create_technologies_view()
            
        # Others view
        if self.page.route == "/others":
            self._create_others_view()
            
        self.page.update()
        
    def _create_editors_view(self):
        editors = self.checkbox_manager.editors
        self.page.views.append(
            ft.View(
                "/text_editors",
                [
                    ft.AppBar(
                        title=ft.Text("Editores de texto", color=WHITE),
                        bgcolor=BASE_COLOR,
                        actions=[
                            ft.IconButton(
                                ft.Icons.CODE,
                                on_click=self.open_credits_dialog,
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
                                                ft.Column([editors["vscode"], editors["neovim"], editors["zed"], editors["geany"]], width=150),
                                                ft.Column([editors["sublime"], editors["bluefish"], editors["lapce"], editors["monodevelop"]], width=150),
                                                ft.Column([editors["intellij"], editors["clion"], editors["rider"], editors["pycharm"]], width=150),
                                                ft.Column([editors["androidstudio"], editors["gnomebuilder"], editors["gedit"], editors["arduino_ide"]], width=150),
                                                ft.Column([editors["eclipse"]], width=150),
                                            ],
                                            scroll=ft.ScrollMode.AUTO,
                                        ),
                                        expand=True,
                                        adaptive=True,
                                        padding=15,
                                        border_radius=15,
                                        bgcolor=BASE_COLOR,
                                    ),
                                ],
                            ),
                            ft.ElevatedButton(
                                "Instalar",
                                bgcolor=BASE_COLOR,
                                color=WHITE,
                                on_click=lambda e: self.dialog_manager.open_dialog(self.dialog_manager.dlg_editor),
                            ),
                        ],
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=24,
                padding=20,
            )
        )
        
    def _create_technologies_view(self):
        tech = self.checkbox_manager.technologies
        self.page.views.append(
            ft.View(
                "/technologies",
                [
                    ft.AppBar(
                        title=ft.Text("Tecnologías", color=WHITE),
                        bgcolor=BASE_COLOR,
                        actions=[
                            ft.IconButton(
                                ft.Icons.CODE,
                                on_click=self.open_credits_dialog,
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
                                                ft.Column([tech["git"], tech["node"], tech["docker"]], width=150),
                                                ft.Container(
                                                    ft.Column(
                                                        [
                                                            ft.Text("Lenguajes", color=WHITE, text_align=ft.TextAlign.CENTER),
                                                            tech["rust"],
                                                            tech["java"],
                                                            tech["python"],
                                                            tech["flutter"],
                                                        ],
                                                        width=150,
                                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    ),
                                                    bgcolor=ft.Colors.GREEN_600,
                                                    border_radius=15,
                                                    padding=15,
                                                ),
                                                ft.Container(
                                                    ft.Column(
                                                        [
                                                            ft.Text("Modo juego", color=WHITE, text_align=ft.TextAlign.CENTER),
                                                            tech["unity"],
                                                            tech["godot"],
                                                            tech["godot_mono"],
                                                            tech["pixelorama"],
                                                        ],
                                                        width=150,
                                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    ),
                                                    bgcolor=ft.Colors.GREY_600,
                                                    border_radius=15,
                                                    padding=15,
                                                ),
                                                ft.Container(
                                                    ft.Column(
                                                        [
                                                            ft.Text("Bases de datos", color=WHITE, text_align=ft.TextAlign.CENTER),
                                                            ft.Row(
                                                                [
                                                                    ft.Column([tech["phpMyAdmin"], tech["mysql"], tech["mysql_clients"], tech["mysql_workbench"]]),
                                                                    ft.Column([tech["postgre"], tech["mongo"], tech["mariadb"], tech["sqlitebrowser"]])
                                                                ]
                                                            ),
                                                        ],
                                                        width=320,
                                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    ),
                                                    bgcolor=ft.Colors.ORANGE_900,
                                                    border_radius=15,
                                                    padding=15,
                                                ),
                                            ],
                                            scroll=ft.ScrollMode.AUTO,
                                        ),
                                        expand=True,
                                        adaptive=True,
                                        padding=15,
                                        border_radius=15,
                                        bgcolor=BASE_COLOR,
                                    ),
                                ],
                            ),
                            ft.ElevatedButton(
                                "Instalar",
                                bgcolor=BASE_COLOR,
                                color=WHITE,
                                on_click=lambda e: self.dialog_manager.open_dialog(self.dialog_manager.dlg_tecn),
                            ),
                        ],
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=24,
                padding=20,
            )
        )
        
    def _create_others_view(self):
        others = self.checkbox_manager.others
        blank = ft.Checkbox(label="blank", label_style=ft.TextStyle(color=WHITE))

        self.page.views.append(
            ft.View(
                "/others",
                [
                    ft.AppBar(
                        title=ft.Text("Otros", color=WHITE),
                        bgcolor=BASE_COLOR,
                        actions=[
                            ft.IconButton(
                                ft.Icons.CODE,
                                on_click=self.open_credits_dialog,
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
                                                            ft.Text("neovim", color=WHITE, text_align=ft.TextAlign.CENTER),
                                                            others["rb_neovim"],
                                                        ],
                                                        width=150,
                                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    ),
                                                    bgcolor=ft.Colors.GREY_600,
                                                    border_radius=15,
                                                    padding=15,
                                                ),
                                                ft.Container(
                                                    ft.Column(
                                                        [
                                                            ft.Text("Herramientas diseño", color=WHITE, text_align=ft.TextAlign.CENTER),
                                                            ft.Row(
                                                                [
                                                                    ft.Column([others["penpot"], others["figma"], others["pencil"]]),
                                                                    ft.Column([others["draw"], others["umlet"], others["umbrello"]])
                                                                ]
                                                            ),
                                                        ],
                                                        width=220,
                                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    ),
                                                    bgcolor=ft.Colors.GREEN,
                                                    border_radius=15,
                                                    padding=15,
                                                ),
                                                ft.Column([blank, blank, blank, blank], width=150),
                                                ft.Column([blank, blank, blank, blank], width=150),
                                            ],
                                            scroll=ft.ScrollMode.AUTO,
                                        ),
                                        expand=True,
                                        adaptive=True,
                                        padding=15,
                                        border_radius=15,
                                        bgcolor=BASE_COLOR,
                                    ),
                                ]
                            ),
                            ft.ElevatedButton(
                                "Instalar",
                                bgcolor=BASE_COLOR,
                                color=WHITE,
                                on_click=lambda e: self.dialog_manager.open_dialog(self.dialog_manager.dlg_other),
                            ),
                        ]
                    ),
                ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
            padding=20,
        )
    )
        
    def open_credits_dialog(self, e):
        def open_github(e):
            self.page.launch_url("https://github.com/CarlosMolinesPastor/develop")

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Créditos", color=BASE_COLOR),
            content=ft.Column(
                [
                    self.img_l,
                    ft.Text("Esta aplicación está hecha con amor por karlinux para aprender y mejorar Flet y Python", color=BASE_COLOR),
                    ft.Text("El proyecto es open source y puedes contribuir en el siguiente enlace:", color=BASE_COLOR),
                    ft.TextButton(
                        text="https://github.com/CarlosMolinesPastor/develop",
                        on_click=open_github,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            actions=[
                ft.TextButton("Aceptar", on_click=lambda e: self.dialog_manager.close_dialog(dlg)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.dialog_manager.open_dialog(dlg)
        
    def install_editors(self):
        editors = self.checkbox_manager.editors
        list_app = []
        
        editor_mapping = {
            "vscode": "visual-studio-code-bin",
            "neovim": "neovim",
            "zed": "zed",
            "geany": "geany geany-plugins",
            "sublime": "sublime-text-4",
            "bluefish": "bluefish",
            "lapce": "lapce",
            "pycharm": "pycharm-community-edition",
            "intellij": "intellij-idea-community-edition",
            "rider": "rider",
            "clion": "clion",
            "monodevelop": "monodevelop-bin",
            "androidstudio": "android-studio",
            "gnomebuilder": "gnome-builder",
            "gedit": "gedit gedit-plugins",
            "arduino_ide": "arduino-ide",
            "eclipse": "eclipse-java",
        }
        
        for editor_name, editor in editors.items():
            if editor.value and not PacmanManager.is_installed(editor_mapping[editor_name].split()[0]):
                list_app.append(editor_mapping[editor_name])
                
        if list_app:
            list_editors = " ".join(list_app)
            self.installation_manager.execute_command(f"yay -S --noconfirm --needed {list_editors}")
        else:
            self.dialog_manager.open_dialog(self.dialog_manager.dlg_installed)
            
    def install_technologies(self):
        tech = self.checkbox_manager.technologies
        list_app = []
        
        tech_mapping = {
            "git": "git",
            "node": "node npm",
            "mongo": "mongodb-bin mongosh-bin mongodb-tools mongodb-compass",
            "mysql": "mysql",
            "mariadb": "mariadb",
            "postgre": "postgresql",
            "phpMyAdmin": "phpmyadmin",
            "mysql_workbench": "mysql-workbench",
            "mysql_clients": "mysql-clients",
            "sqlitebrowser": "sqlitebrowser",
            "python": "python",
            "rust": "rust",
            "java": "jdk-openjdk",
            "flutter": "flutter-bin google-chrome",
            "docker": "docker docker-compose",
            "unity": "unityhub",
            "godot": "godot",
            "godot_mono": "godot-mono",
            "pixelorama": "pixelorama",
        }
        
        for tech_name, checkbox in tech.items():
            if checkbox.value and not PacmanManager.is_installed(tech_mapping[tech_name].split()[0]):
                list_app.append(tech_mapping[tech_name])
                
        if list_app:
            list_tech = " ".join(list_app)
            command = f"yay -S --noconfirm --needed {list_tech}"
            
            if "flutter-bin" in list_tech and "docker" in list_tech:
                command += " && sudo usermod -a -G flutter $USER && sudo usermod -a -G docker $USER"
            elif "flutter-bin" in list_tech:
                command += " && sudo usermod -a -G flutter $USER"
            elif "docker" in list_tech:
                command += " && sudo usermod -a -G docker $USER"
                
            self.installation_manager.execute_command(command)
        else:
            self.dialog_manager.open_dialog(self.dialog_manager.dlg_installed)
            
    def install_others(self):
        others = self.checkbox_manager.others
        list_app = []
        
        others_mapping = {
            "lazyvim": "lazyvim",
            "nvchad": "nvchad",
            "astrovim": "astrovim",
            "penpot": "penpot",
            "figma": "figma-linux",
            "pencil": "pencil",
            "draw": "drawio-desktop",
            "umlet": "umlet",
            "umbrello": "umbrello",
        }
        
        if others["rb_neovim"].value:
            list_app.append(others["rb_neovim"].value)
            
        for other_name, control in others.items():
            if other_name != "rb_neovim" and isinstance(control, ft.Checkbox) and control.value and not PacmanManager.is_installed(others_mapping[other_name]):
                list_app.append(others_mapping[other_name])
                
        if list_app:
            list_others = " ".join(list_app)
            command = f"yay -S --noconfirm --needed {list_others}"
            
            if "lazyvim" in list_others:
                command += " && mv ~/.config/nvim{,.bak} && mv ~/.local/share/nvim{,.bak} && mv ~/.local/state/nvim{,.bak} && mv ~/.cache/nvim{,.bak} && git clone https://github.com/LazyVim/starter ~/.config/nvim && rm -rf ~/.config/nvim/.git"
                
            self.installation_manager.execute_command(command)
        else:
            self.dialog_manager.open_dialog(self.dialog_manager.dlg_installed)
            
    def install_yay(self):
        command = "sudo pacman -S --noconfirm --needed base-devel git && git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si --noconfirm"
        self.installation_manager.execute_command(command)
        
    def check_yay_installed(self):
        if not PacmanManager.is_installed("yay"):
            self.dialog_manager.open_dialog(self.dialog_manager.dlg_install_yay)

def main(page: ft.Page):
    app = AppUI(page)
    # Check yay after 2 seconds
    threading.Timer(2.0, app.check_yay_installed).start()

ft.app(main)