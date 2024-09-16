""" import flet as ft

def main(page: ft.Page):
    page.title = "Controle de Estoque"
    page.theme_mode = ft.ThemeMode.LIGHT # Pode trocar para DARK

    # Função para criar cards clicáveis
    def create_card(icon, text):
        return ft.GestureDetector(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(icon, size=50),
                            ft.Text(text, size=18, text_align=ft.TextAlign.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=20,
                ),
                elevation=4,
                margin=10,
            ),
            on_tap=lambda e: handle_click(text)  # Função para tratar o clique
        )

    # Função para lidar com o clique
    def handle_click(section_name):
        print(f"Clicou no card: {section_name}")  # Log no console
        page.snack_bar = ft.SnackBar(ft.Text(f"Você clicou em {section_name}!"))
        page.snack_bar.open = True
        page.update()

    # Criar o AppBar com opções de Língua, Ajuda e Admin (Não funciona ainda, mas é uma base)
    page.appbar = ft.AppBar(
        title=ft.Text("Menu xxx Controle de Estoque"),
        center_title=True,
        actions=[
            ft.IconButton(ft.icons.LANGUAGE, tooltip="Trocar Língua"),
            ft.IconButton(ft.icons.HELP, tooltip="Ajuda"),
            ft.IconButton(ft.icons.ADMIN_PANEL_SETTINGS, tooltip="Admin"),
        ],
    )

    # Layout principal
    page.add(
        ft.Column(
            [
                ft.Text("Controle de Estoque xxx", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row(
                    [
                        create_card(ft.icons.PERSON, "Gestão de Usuário"),
                        create_card(ft.icons.GROUP, "Cadastro de Fornecedores"),
                        create_card(ft.icons.SHOPPING_CART, "Cadastro de Produtos"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Row(
                    [
                        create_card(ft.icons.REMOVE_SHOPPING_CART, "Saída do Estoque"),
                        create_card(ft.icons.ADD_SHOPPING_CART, "Entradas no Estoque"),
                        create_card(ft.icons.BAR_CHART, "Gráficos"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Row(
                    [
                        create_card(ft.icons.PEOPLE, "Cadastro de Clientes"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )

# Executar o app
ft.app(target=main) """


#O comando de cima é pra testar se os botões estava funcionando, mostrando no console a mensagem
#O comando de baixo é o que vai ser depois, quando clica nos botões ele vai para alguma outra parte do sist

import flet as ft

def main(page: ft.Page):
    page.title = "Controle de Estoque"
    page.theme_mode = ft.ThemeMode.LIGHT # Pode trocar para DARK

    # Função para criar cards clicáveis
    def create_card(icon, text, route):
        return ft.GestureDetector(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(icon, size=50),
                            ft.Text(text, size=18, text_align=ft.TextAlign.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=20,
                ),
                elevation=4,
                margin=10,
            ),
            on_tap=lambda e: page.go(route)  # Navegar para outra parte do sistema ao clicar
        )

    # Criar o AppBar com opções de Língua, Ajuda e Admin (Não funciona ainda, é uma base)
    page.appbar = ft.AppBar(
        title=ft.Text("Menu xxx Controle de Estoque"),
        center_title=True,
        actions=[
            ft.IconButton(ft.icons.LANGUAGE, tooltip="Trocar Língua"),
            ft.IconButton(ft.icons.HELP, tooltip="Ajuda"),
            ft.IconButton(ft.icons.ADMIN_PANEL_SETTINGS, tooltip="Admin"),
        ],
    )

    # Layout principal
    page.add(
        ft.Column(
            [
                ft.Text("Controle de Estoque xxx", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row(
                    [
                        create_card(ft.icons.PERSON, "Gestão de Usuário", "/usuarios"),
                        create_card(ft.icons.GROUP, "Cadastro de Fornecedores", "/fornecedores"),
                        create_card(ft.icons.SHOPPING_CART, "Cadastro de Produtos", "/produtos"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Row(
                    [
                        create_card(ft.icons.REMOVE_SHOPPING_CART, "Saída do Estoque", "/saida"),
                        create_card(ft.icons.ADD_SHOPPING_CART, "Entradas no Estoque", "/entrada"),
                        create_card(ft.icons.BAR_CHART, "Gráficos", "/graficos"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Row(
                    [
                        create_card(ft.icons.PEOPLE, "Cadastro de Clientes", "/clientes"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )

# Executar o app
ft.app(target=main)