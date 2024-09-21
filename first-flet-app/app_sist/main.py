import flet as ft
import qrcode
from io import BytesIO
from base64 import b64encode

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
        "generate_qr_code": "Gerar QR Code",
        "scan_qr_code": "Escanear QR Code",
        "input_product_code": "Insira o código do produto",
        "product_list_title": "Lista de Produtos",
        "edit_button_text": "Editar",
        "delete_button_text": "Deletar",

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
        "scan_qr_code": "Scan QR Code",
        "input_product_code": "Enter product code",
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
        "scan_qr_code": "Escanear QR Code",
        "input_product_code": "Ingrese el código del producto",
    }
}

# Função principal
def main(page: ft.Page):
    # Estado inicial
    page.title = translations["pt"]["title"]
    current_language = "pt"  # Padrão: Português
    page.theme_mode = ft.ThemeMode.LIGHT  # Padrão: Modo claro
    products = []
    
    # Declara a lista de produtos fora da função
    product_list = ft.Column()

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
        
        
        
    def close_product_dialog(e=None):
        if product_dialog.open:
            product_dialog.open = False
            page.update()

    def close_edit_dialog(e=None):
        for control in page.overlay:
            if isinstance(control, ft.AlertDialog):
                control.open = False
        page.update()

    def close_help_dialog():
        for control in page.overlay:
            if isinstance(control, ft.AlertDialog):
                control.open = False
        page.update()

    def add_product(name, quantity):
        if name and quantity.isdigit():
            products.append({"name": name, "quantity": int(quantity)})
            refresh_product_list()
            close_product_dialog()

    def edit_product(index, name, quantity):
        if name and quantity.isdigit():
            products[index] = {"name": name, "quantity": int(quantity)}
            refresh_product_list()
            close_edit_dialog()

    def delete_product(index):
        products.pop(index)
        refresh_product_list()

    def refresh_product_list():
        product_list.controls.clear()
        for index, product in enumerate(products):
            product_list.controls.append(
                ft.Row([
                    ft.Text(f"{product['name']} - {product['quantity']}", size=16),
                    ft.ElevatedButton(translations[current_language]["edit_button_text"], on_click=lambda e, idx=index: edit_product_dialog(idx)),
                    ft.ElevatedButton(translations[current_language]["delete_button_text"], on_click=lambda e, idx=index: delete_product(idx)),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
        page.update()

    def add_product_dialog(e):
        product_dialog.open = True
        page.overlay.append(product_dialog)
        page.update()

    def generate_qr_code(name):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(name)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return b64encode(buffered.getvalue()).decode('utf-8')

    def show_qr_code(name):
        qr_image = generate_qr_code(name)
        qr_dialog = ft.AlertDialog(
            title=ft.Text("QR Code"),
            content=ft.Column([
                ft.Image(src=f"data:image/png;base64,{qr_image}", width=200, height=200),
                ft.Text("Este QR Code pode ser escaneado para identificar o produto."),
            ]),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: close_qr_dialog(qr_dialog))
            ]
        )
        page.overlay.append(qr_dialog)
        qr_dialog.open = True
        page.update()

    def close_qr_dialog(dialog):
        dialog.open = False
        page.update()

    def show_product_management_page(e):
        page.clean()
        page.appbar = appbar

        refresh_product_list()

        product_management_page = ft.Column([
            ft.Text(translations[current_language]["product_list_title"], size=30),
            product_list,
            ft.Row([
                ft.ElevatedButton(translations[current_language]["register_button_text"], on_click=add_product_dialog),
                ft.ElevatedButton("Voltar", on_click=go_back)
            ], alignment=ft.MainAxisAlignment.END)
        ], alignment=ft.MainAxisAlignment.START, expand=True)

        page.add(product_management_page)
        page.update()

    def go_back(e):
        # Volta para a interface anterior 
        page.clean()  # Limpa a página atual
        page.appbar = appbar  # Recria a appbar
        page.add(main_content)  # Volta para o conteúdo principal
        page.update()

    product_dialog = ft.AlertDialog(
        title=ft.Text(translations[current_language]["register_product_title"]),
        content=ft.Column([
            ft.TextField(label=translations[current_language]["product_name_label"]),
            ft.TextField(label=translations[current_language]["product_quantity_label"], keyboard_type=ft.KeyboardType.NUMBER)
        ]),
        actions=[
            ft.TextButton(translations[current_language]["register_button_text"], on_click=lambda e: add_product(product_dialog.content.controls[0].value, product_dialog.content.controls[1].value)),
            ft.TextButton(translations[current_language]["generate_qr_code"], on_click=lambda e: show_qr_code(product_dialog.content.controls[0].value)),
            ft.TextButton("Fechar", on_click=close_product_dialog)
        ]
    )

    def edit_product_dialog(index):
        product = products[index]
        edit_dialog = ft.AlertDialog(
            title=ft.Text(translations[current_language]["register_product_title"]),
            content=ft.Column([
                ft.TextField(label=translations[current_language]["product_name_label"], value=product['name']),
                ft.TextField(label=translations[current_language]["product_quantity_label"], value=str(product['quantity']), keyboard_type=ft.KeyboardType.NUMBER)
            ]),
            actions=[
                ft.TextButton(translations[current_language]["register_button_text"], on_click=lambda e: edit_product(index, edit_dialog.content.controls[0].value, edit_dialog.content.controls[1].value)),
                ft.TextButton("Fechar", on_click=close_edit_dialog)
            ]
        )
        page.overlay.append(edit_dialog)
        edit_dialog.open = True
        page.update()

        
        

    # Função para exibir a interface de Gestão de Usuários
    def show_user_management_page(e):
        page.clean()  # Limpa a página atual
        
        def go_back_to_main(e):
            page.clean()
            page.appbar = appbar
            page.add(main_content)  # Volta para a interface principal
            page.update()

        # Adiciona um botão para voltar à interface principal
        user_management_page = ft.Column(
            [
                ft.Text("Gestão de Usuários", size=30),
                ft.ElevatedButton("Voltar", on_click=go_back_to_main),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

        page.add(user_management_page)
        page.update()

    # Função para exibir a caixa de diálogo de ajuda
    def show_help_dialog(e):
        help_dialog.open = True
        page.overlay.append(help_dialog)
        page.update()

    # Função para registrar produto
    def show_product_registration_dialog(e):
        product_dialog.open = True
        page.overlay.append(product_dialog)
        page.update()

    # Função para registrar fornecedor
    def show_supplier_registration_dialog(e):
        supplier_dialog.open = True
        page.overlay.append(supplier_dialog)
        page.update()

    # Caixa de diálogo com informações sobre o sistema
    help_dialog = ft.AlertDialog(
        title=ft.Text(translations[current_language]["help_button_text"]),
        content=ft.Text(translations[current_language]["help_content"]),
        actions=[ft.TextButton("Fechar", on_click=lambda e: close_help_dialog())]
    )

    # Função para fechar a caixa de diálogo
    def close_help_dialog():
        help_dialog.open = False
        page.update()

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
            ft.PopupMenuItem(text="Português", data="pt", on_click=change_language),
            ft.PopupMenuItem(text="English", data="en", on_click=change_language),
            ft.PopupMenuItem(text="Español", data="es", on_click=change_language),
        ],
    )
    
    #saida e entrada de produto com qr code
    def show_stock_exit_dialog(e):
        stock_exit_dialog.open = True
        page.overlay.append(stock_exit_dialog)
        page.update()

    def show_stock_entry_dialog(e):
        stock_entry_dialog.open = True
        page.overlay.append(stock_entry_dialog)
        page.update()

    stock_exit_dialog = ft.AlertDialog(
        title=ft.Text(translations[current_language]["stock_exit"]),
        content=ft.Column([
            ft.TextField(label=translations[current_language]["input_product_code"]),
            ft.ElevatedButton(translations[current_language]["scan_qr_code"], on_click=lambda e: scan_qr_code("exit")),
        ]),
        actions=[
            ft.TextButton("Fechar", on_click=lambda e: close_dialog(stock_exit_dialog)),
        ],
    )

    stock_entry_dialog = ft.AlertDialog(
        title=ft.Text(translations[current_language]["stock_entry"]),
        content=ft.Column([
            ft.TextField(label=translations[current_language]["input_product_code"]),
            ft.ElevatedButton(translations[current_language]["scan_qr_code"], on_click=lambda e: scan_qr_code("entry")),
        ]),
        actions=[
            ft.TextButton("Fechar", on_click=lambda e: close_dialog(stock_entry_dialog)),
        ],
    )

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    def scan_qr_code(action):
        # Lógica de leitura do QR Code pode ser implementada aqui
        # Exemplo fictício:
        print(f"Scanning QR Code for {action}...")
        # Implementar a lógica real aqui...
        page.update()

    # Botão para alternar tema
    theme_toggle_button = ft.IconButton(
        icon=ft.icons.BRIGHTNESS_6,
        tooltip=translations[current_language]["theme_button_text"],
        on_click=toggle_theme
    )

    # Botão Ajuda
    help_button = ft.IconButton(ft.icons.HELP, tooltip=translations[current_language]["help_button_text"], on_click=show_help_dialog)

    # Criar o AppBar
    appbar = ft.AppBar(
        title=ft.Text(translations[current_language]["title"]),
        center_title=True,
        actions=[language_popup_menu, theme_toggle_button, help_button, ft.IconButton(ft.icons.ADMIN_PANEL_SETTINGS, tooltip="Admin")],
    )

    # Lista de cards
    cards = [
        create_card(ft.icons.PERSON, "user_management", show_user_management_page),
        create_card(ft.icons.GROUP, "supplier_registration", show_supplier_registration_dialog),
        create_card(ft.icons.SHOPPING_BAG, "product_registration", show_product_registration_dialog),
        create_card(ft.icons.REMOVE_SHOPPING_CART, "stock_exit", show_stock_exit_dialog),
        create_card(ft.icons.ADD_SHOPPING_CART, "stock_entry", show_stock_entry_dialog),
        create_card(ft.icons.INVENTORY, "product_management", show_product_management_page),
    ]

    # Conteúdo principal da página
    main_content = ft.Column(
        [
            ft.Row(cards[:3], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Row(cards[3:], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )

    page.appbar = appbar
    page.add(main_content)
    page.update()

# Executar o app
ft.app(target=main)
