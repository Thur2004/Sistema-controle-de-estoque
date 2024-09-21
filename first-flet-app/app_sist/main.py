import flet as ft

# Dicionário de traduções
translations = {
    "pt": {
        "title": "Controle de Estoque",
        "user_management": "Gestão de Usuário",
        "supplier_registration": "Cadastro de Fornecedores",
        "product_management": "Gestão de Produtos",
        "product_registration": "Cadastro de Produtos",
        "stock_exit": "Saída do Estoque",
        "stock_entry": "Entradas no Estoque",
        "help_content": "Este sistema permite:\n- Gestão de usuários.\n- Cadastro de fornecedores.\n- Gestão e cadastro de produtos.\n- Controle de entradas e saídas do estoque.",
        "help_button_text": "Ajuda",
        "language_button_text": "Idioma",
        "theme_button_text": "Alternar Tema",
        "register_product_title": "Cadastro de Produto",
        "product_name_label": "Nome do Produto",
        "product_quantity_label": "Quantidade",
        "register_supplier_title": "Cadastro de Fornecedor",
        "supplier_name_label": "Nome do Fornecedor",
        "supplier_contact_label": "Contato",
        "register_button_text": "Cadastrar",
    },
    "en": {
        "title": "Inventory Control",
        "user_management": "User Management",
        "supplier_registration": "Supplier Registration",
        "product_management": "Product Management",
        "product_registration": "Product Registration",
        "stock_exit": "Stock Exit",
        "stock_entry": "Stock Entry",
        "help_content": "This system allows:\n- User management.\n- Supplier registration.\n- Product management and registration.\n- Control of stock entries and exits.",
        "help_button_text": "Help",
        "language_button_text": "Language",
        "theme_button_text": "Toggle Theme",
        "register_product_title": "Product Registration",
        "product_name_label": "Product Name",
        "product_quantity_label": "Quantity",
        "register_supplier_title": "Supplier Registration",
        "supplier_name_label": "Supplier Name",
        "supplier_contact_label": "Contact",
    },
    "es": {
        "title": "Control de Inventario",
        "user_management": "Gestión de Usuario",
        "supplier_registration": "Registro de Proveedores",
        "product_management": "Gestión de Productos",
        "product_registration": "Registro de Productos",
        "stock_exit": "Salida de Inventario",
        "stock_entry": "Entrada de Inventario",
        "help_content": "Este sistema permite:\n- Gestión de usuarios.\n- Registro de proveedores.\n- Gestión y registro de productos.\n- Control de entradas e salidas de inventario.",
        "help_button_text": "Ayuda",
        "language_button_text": "Idioma",
        "theme_button_text": "Alternar Tema",
        "register_product_title": "Registro de Producto",
        "product_name_label": "Nombre del Producto",
        "product_quantity_label": "Cantidad",
        "register_supplier_title": "Registro de Proveedor",
        "supplier_name_label": "Nombre del Proveedor",
        "supplier_contact_label": "Contacto",
    }
}

# Função principal
def main(page: ft.Page):
    # Estado inicial
    page.title = "Controle de Estoque"
    current_language = "pt"  # Padrão: Português
    page.theme_mode = ft.ThemeMode.LIGHT  # Padrão: Modo claro

    # Função para trocar de idioma
    def change_language(e):
        nonlocal current_language
        selected_language = e.control.data
        current_language = selected_language
        update_ui()  # Atualiza a interface com o novo idioma

    # Função para alternar entre dark/light mode
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    # Função para atualizar a interface com o idioma selecionado
    def update_ui():
        appbar.title = ft.Text(translations[current_language]["title"])
        cards[0].content.content.controls[1].value = translations[current_language]["user_management"]
        cards[1].content.content.controls[1].value = translations[current_language]["supplier_registration"]
        cards[2].content.content.controls[1].value = translations[current_language]["product_registration"]
        cards[3].content.content.controls[1].value = translations[current_language]["stock_exit"]
        cards[4].content.content.controls[1].value = translations[current_language]["stock_entry"]
        cards[5].content.content.controls[1].value = translations[current_language]["product_management"]
        help_button.tooltip = translations[current_language]["help_button_text"]
        help_dialog.title = ft.Text(translations[current_language]["help_button_text"])
        help_dialog.content = ft.Text(translations[current_language]["help_content"])
        language_popup_menu.tooltip = translations[current_language]["language_button_text"]
        theme_toggle_button.tooltip = translations[current_language]["theme_button_text"]
        product_dialog.title = ft.Text(translations[current_language]["register_product_title"])
        supplier_dialog.title = ft.Text(translations[current_language]["register_supplier_title"])
        page.update()

    # Função para criar cards clicáveis
    def create_card(icon, text_key, on_click):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(icon, size=50),
                        ft.Text(translations[current_language][text_key], size=18, text_align=ft.TextAlign.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                padding=20,
                on_click=on_click,  # Usar on_click no Container
            ),
            elevation=4,
            margin=10,
        )

    # Função para exibir a caixa de diálogo de ajuda
    def show_help_dialog(e):
        help_dialog.open = True
        page.update()

    # Função para registrar produto
    def show_product_registration_dialog(e):
        product_dialog.open = True
        page.update()

    # Função para registrar fornecedor
    def show_supplier_registration_dialog(e):
        supplier_dialog.open = True
        page.update()

    # Caixa de diálogo com informações sobre o sistema
    help_dialog = ft.AlertDialog(
        title=ft.Text(translations[current_language]["help_button_text"]),
        content=ft.Text(translations[current_language]["help_content"]),
        actions=[
            ft.TextButton("Fechar", on_click=lambda e: close_help_dialog())
        ]
    )

    # Função para fechar a caixa de diálogo
    def close_help_dialog():
        help_dialog.open = False
        page.update()

    # Diálogo de registro de produto
    product_dialog = ft.AlertDialog(
        title=ft.Text(translations[current_language]["register_product_title"]),
        content=ft.Column([
            ft.TextField(label=translations[current_language]["product_name_label"]),
            ft.TextField(label=translations[current_language]["product_quantity_label"], keyboard_type=ft.KeyboardType.NUMBER)
        ]),
        actions=[
            ft.TextButton(translations[current_language]["register_button_text"], on_click=lambda e: register_product()),
            ft.TextButton("Fechar", on_click=lambda e: close_product_dialog())
        ]
    )

    # Diálogo de registro de fornecedor
    supplier_dialog = ft.AlertDialog(
        title=ft.Text(translations[current_language]["register_supplier_title"]),
        content=ft.Column([
            ft.TextField(label=translations[current_language]["supplier_name_label"]),
            ft.TextField(label=translations[current_language]["supplier_contact_label"])
        ]),
        actions=[
            ft.TextButton(translations[current_language]["register_button_text"], on_click=lambda e: register_supplier()),
            ft.TextButton("Fechar", on_click=lambda e: close_supplier_dialog())
        ]
    )

    def register_product():
        # Lógica para registrar o produto pode ser implementada aqui
        product_dialog.open = False
        page.update()

    def close_product_dialog():
        product_dialog.open = False
        page.update()

    def register_supplier():
        # Lógica para registrar o fornecedor pode ser implementada aqui
        supplier_dialog.open = False
        page.update()

    def close_supplier_dialog():
        supplier_dialog.open = False
        page.update()

    # Menu suspenso de idiomas
    language_popup_menu = ft.PopupMenuButton(
        icon=ft.icons.PUBLIC,
        tooltip=translations[current_language]["language_button_text"],
        items=[
            ft.PopupMenuItem(text="Português", on_click=change_language, data="pt"),
            ft.PopupMenuItem(text="English", on_click=change_language, data="en"),
            ft.PopupMenuItem(text="Español", on_click=change_language, data="es"),
        ]
    )

    # Botão para alternar entre Light e Dark mode
    theme_toggle_button = ft.IconButton(
        icon=ft.icons.BRIGHTNESS_6, tooltip=translations[current_language]["theme_button_text"], on_click=toggle_theme
    )

    # Botão Ajuda
    help_button = ft.IconButton(ft.icons.HELP, tooltip=translations[current_language]["help_button_text"], on_click=show_help_dialog)

    # Criar o AppBar
    appbar = ft.AppBar(
        title=ft.Text(translations[current_language]["title"]),
        center_title=True,
        actions=[
            language_popup_menu,
            theme_toggle_button,
            help_button,
            ft.IconButton(ft.icons.ADMIN_PANEL_SETTINGS, tooltip="Admin"),
        ],
    )

    # Lista de cards
    cards = [
        create_card(ft.icons.PERSON, "user_management", None),
        create_card(ft.icons.GROUP, "supplier_registration", show_supplier_registration_dialog),
        create_card(ft.icons.SHOPPING_BAG, "product_registration", show_product_registration_dialog),
        create_card(ft.icons.REMOVE_SHOPPING_CART, "stock_exit", None),
        create_card(ft.icons.ADD_SHOPPING_CART, "stock_entry", None),
        create_card(ft.icons.INVENTORY, "product_management", None),
    ]

    # Layout principal
    page.add(
        ft.Column(
            [
                ft.Row(
                    cards[:3],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Row(
                    cards[3:],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )

    # Definir AppBar e rodar a interface
    page.appbar = appbar
    page.overlay.append(help_dialog)
    page.overlay.append(product_dialog)
    page.overlay.append(supplier_dialog)
    page.update()

# Executar o app
ft.app(target=main)