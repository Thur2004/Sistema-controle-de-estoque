import flet as ft
from io import BytesIO
import qrcode
import base64
import numpy as np
import cv2
from datetime import datetime
import mysql.connector
from mysql.connector import Error

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
        "login": "Entrar",
        "username": "Usuário",
        "password": "Senha",
        "login_error": "Usuário ou senha inválidos",
        "logout": "Sair",
        "login_button": "Entrar",
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
        "product_list_title": "Product List",
        "register_button_text": "Register",
        "edit_button_text": "Edit",
        "delete_button_text": "Delete",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "login_error": "Invalid username or password",
        "logout": "Logout",
        "login_button": "Login",
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
        "product_list_title": "Lista de Productos",
        "register_button_text": "Registrar",
        "edit_button_text": "Editar",
        "delete_button_text": "Borrar",
        "login": "Iniciar sesión",
        "username": "Usuario",
        "password": "Contraseña",
        "login_error": "Usuario o contraseña inválidos",
        "logout": "Cerrar sesión",
        "login_button": "Iniciar sesión",
    }
}

# Database connection configuration
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Default XAMPP password is empty
            database="inventory_system"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

# Initialize database and tables
def init_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
        cursor.execute("USE inventory_system")
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                qr_code TEXT
            )
        """)
        
        # Create movements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movements (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATETIME NOT NULL,
                action_type VARCHAR(50) NOT NULL,
                product_name VARCHAR(255) NOT NULL,
                quantity INT NOT NULL
            )
        """)
        
        # Create suppliers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                contact VARCHAR(100),
                email VARCHAR(255),
                address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        connection.commit()
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_default_admin():
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            # Create default admin user
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                ("admin", "admin123", "admin")
            )
            connection.commit()
    except Error as e:
        print(f"Error creating default admin: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Função principal
def main(page: ft.Page):
    # Initial state setup
    page.user = None
    page.title = translations["pt"]["title"]
    current_language = "pt"
    page.theme_mode = ft.ThemeMode.LIGHT

    def verify_credentials(username, password):
        try:
            connection = create_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            return user
        except Error as e:
            print(f"Error verifying credentials: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def login(e):
        user = verify_credentials(
            username_field.value,
            password_field.value
        )
        if user:
            page.user = user
            show_main_interface()
        else:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(translations[current_language]["login_error"]))
            )
        page.update()

    def logout(e):
        page.user = None
        show_login_interface()
        page.update()

    def show_login_interface():
        page.clean()
        page.appbar = None
        page.add(login_view)
        # Clear credentials
        username_field.value = ""
        password_field.value = ""
        page.update()

    def show_main_interface():
        page.clean()
        page.appbar = appbar
        page.add(main_content)
        page.update()

    # Login interface components
    username_field = ft.TextField(
        label=translations[current_language]["username"],
        width=300
    )
    password_field = ft.TextField(
        label=translations[current_language]["password"],
        password=True,
        width=300,
        on_submit=login  # Allow login with Enter key
    )

    login_view = ft.Container(
        content=ft.Column(
            [
                ft.Text(translations[current_language]["login"], size=32, weight="bold"),
                username_field,
                password_field,
                ft.ElevatedButton(
                    text=translations[current_language]["login_button"],
                    on_click=login,
                    width=300
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    # Define change_language function before popup menu
    def change_language(e):
        nonlocal current_language
        selected_language = e.control.data
        current_language = selected_language
        update_ui()  # Atualiza a interface com o novo idioma

    # Then create popup menu
    language_popup_menu = ft.PopupMenuButton(
        icon=ft.icons.PUBLIC,
        tooltip=translations[current_language]["language_button_text"],
        items=[
            ft.PopupMenuItem(text="Português", data="pt", on_click=change_language),
            ft.PopupMenuItem(text="English", data="en", on_click=change_language),
            ft.PopupMenuItem(text="Español", data="es", on_click=change_language),
        ],
    )

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    # Define theme toggle button before appbar
    theme_toggle_button = ft.IconButton(
        icon=ft.icons.BRIGHTNESS_6,
        tooltip=translations[current_language]["theme_button_text"],
        on_click=toggle_theme
    )

    # Define help dialog and its functions first
    help_dialog = ft.AlertDialog(
        title=ft.Text(translations[current_language]["help_button_text"]),
        content=ft.Text(translations[current_language]["help_content"]),
        actions=[ft.TextButton("Fechar", on_click=lambda e: close_help_dialog())]
    )

    def show_help_dialog(e):
        help_dialog.open = True
        page.overlay.append(help_dialog)
        page.update()

    def close_help_dialog():
        help_dialog.open = False
        page.update()

    # Then define help button
    help_button = ft.IconButton(
        ft.icons.HELP, 
        tooltip=translations[current_language]["help_button_text"], 
        on_click=show_help_dialog
    )

    # Define movement history function before appbar
    def show_movement_history(e):
        page.clean()
        page.appbar = appbar  # Keep the appbar

        # Create a new movement history view
        movement_history_view = ft.Column([
            ft.Text("Histórico de Movimentações", size=30, weight="bold"),
            movement_list,
            ft.ElevatedButton("Voltar", on_click=go_back)
        ], alignment=ft.MainAxisAlignment.START, expand=True)

        page.add(movement_history_view)
        refresh_movement_list()  # Update the movement list
        page.update()

    # Then create appbar using all the buttons
    appbar = ft.AppBar(
        title=ft.Text(translations[current_language]["title"]),
        center_title=True,
        actions=[
            language_popup_menu, 
            theme_toggle_button, 
            help_button, 
            ft.IconButton(ft.icons.ADMIN_PANEL_SETTINGS, tooltip="Admin"),
            ft.IconButton(
                ft.icons.HISTORY, 
                tooltip="Ver Histórico", 
                on_click=show_movement_history
            ),
            ft.IconButton(  # Add logout button
                ft.icons.LOGOUT,
                tooltip=translations[current_language]["logout"],
                on_click=logout
            )
        ],
    )

    # Initialize database and create default admin
    init_database()
    create_default_admin()
    
    # Start with login interface
    show_login_interface()

    # Estado inicial
    page.qr_dialog = None
    page.title = translations["pt"]["title"]
    current_language = "pt"  # Padrão: Português
    page.theme_mode = ft.ThemeMode.LIGHT  # Padrão: Modo claro
    products = []
    
    # Declara a lista de produtos fora da função
    product_list = ft.Column()

    qr_code_storage = [] # Array para armazenar os QR codes
    myresult = ft.Column()  # Para mostrar resultados do QR Code

    movements = []  # Lista global para armazenar cada movimentação de estoque
    # Elemento UI para lista de movimentações
    movement_list = ft.Column()

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

    # Modified functions to use database instead of local storage
    def add_product(name, quantity):
        if name and quantity.isdigit():
            try:
                connection = create_db_connection()
                cursor = connection.cursor()
                
                # Generate QR code with product information
                qr_data = f"{name}|{quantity}"  # Format: "product_name|quantity"
                qr_code = generate_qr_code(qr_data)
                
                cursor.execute(
                    "INSERT INTO products (name, quantity, qr_code) VALUES (%s, %s, %s)",
                    (name, int(quantity), qr_code)
                )
                connection.commit()
                refresh_product_list()
                close_product_dialog()
            except Error as e:
                print(f"Error adding product: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def process_qr_code_scan(action_type, qr_data):
        try:
            # Parse QR code data
            product_name = qr_data.split('|')[0]
            
            connection = create_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Get current product quantity
            cursor.execute("SELECT quantity FROM products WHERE name = %s", (product_name,))
            result = cursor.fetchone()
            
            if result:
                current_quantity = result['quantity']
                
                # Update quantity based on action type
                if action_type == "exit":
                    if current_quantity > 0:
                        new_quantity = current_quantity - 1
                        cursor.execute(
                            "UPDATE products SET quantity = %s WHERE name = %s",
                            (new_quantity, product_name)
                        )
                        record_movement("Saída", product_name, 1)
                    else:
                        print("Produto sem estoque!")
                        return
                else:  # entry
                    new_quantity = current_quantity + 1
                    cursor.execute(
                        "UPDATE products SET quantity = %s WHERE name = %s",
                        (new_quantity, product_name)
                    )
                    record_movement("Entrada", product_name, 1)
                
                connection.commit()
                refresh_product_list()
                
            else:
                print("Produto não encontrado!")
                
        except Error as e:
            print(f"Error processing QR code: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def read_qrcode(action_type):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detector = cv2.QRCodeDetector()
            data, points, _ = detector.detectAndDecode(gray)

            if data:
                cv2.polylines(frame, [np.int32(points)], True, (255, 0, 0), 2, cv2.LINE_AA)
                print(f"QR Code Data: {data}")
                
                # Process the scanned QR code
                process_qr_code_scan(action_type, data)
                
                cap.release()
                cv2.destroyAllWindows()
                break
                
            cv2.imshow("QR CODE DETECTION", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
                
        if cap.isOpened():
            cap.release()
            cv2.destroyAllWindows()

    def refresh_product_list():
        try:
            connection = create_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            
            product_list.controls.clear()
            for product in products:
                product_list.controls.append(
                    ft.Row([
                        ft.Text(f"{product['name']} - {product['quantity']}", size=16),
                        ft.ElevatedButton(
                            translations[current_language]["edit_button_text"],
                            on_click=lambda e, id=product['id']: edit_product_dialog(id)
                        ),
                        ft.ElevatedButton(
                            translations[current_language]["delete_button_text"],
                            on_click=lambda e, id=product['id']: delete_product(id)
                        ),
                        ft.ElevatedButton(
                            "Ver QR Code",
                            on_click=lambda e, id=product['id']: show_qr_code_for_product(id)
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            page.update()
        except Error as e:
            print(f"Error refreshing product list: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def record_movement(action_type, product_name, quantity):
        try:
            connection = create_db_connection()
            cursor = connection.cursor()
            
            cursor.execute(
                "INSERT INTO movements (date, action_type, product_name, quantity) VALUES (%s, %s, %s, %s)",
                (datetime.now(), action_type, product_name, quantity)
            )
            connection.commit()
            refresh_movement_list()
        except Error as e:
            print(f"Error recording movement: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def refresh_movement_list():
        try:
            connection = create_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM movements ORDER BY date DESC")
            movements = cursor.fetchall()
            
            movement_list.controls.clear()
            for movement in movements:
                movement_list.controls.append(
                    ft.Row([
                        ft.Text(f"{movement['date']} - {movement['action_type']} - {movement['product_name']} - {movement['quantity']}")
                    ])
                )
            page.update()
        except Error as e:
            print(f"Error refreshing movement list: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def add_product_dialog(e):
        product_dialog.open = True
        page.overlay.append(product_dialog)
        page.update()

    def generate_qr_code(data):
        qr = qrcode.make(data)
        buffered = BytesIO()
        qr.save(buffered, format="PNG")  # Salva como PNG
        return base64.b64encode(buffered.getvalue()).decode("utf-8")  # Retorna o QR code gerado


    def show_qr_code_for_product(product_id):
        try:
            connection = create_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT name, qr_code FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            
            if product:
                qr_dialog = ft.AlertDialog(
                    title=ft.Text(f"QR Code - {product['name']}"),
                    content=ft.Column(
                        [
                            ft.Image(src_base64=product['qr_code'], width=200, height=200),
                            ft.Text("Escaneie este QR Code para gerenciar o estoque do produto."),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    actions=[
                        ft.TextButton("Fechar", on_click=lambda e: close_dialog(qr_dialog))
                    ]
                )
                
                page.overlay.append(qr_dialog)
                qr_dialog.open = True
                page.update()
                
        except Error as e:
            print(f"Error showing QR code: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    # Função para registrar saída do estoque (chamado na função scan_qr_code ao detectar saída)
    def register_stock_exit(product_name, quantity):
        record_movement("Saída", product_name, quantity)
        refresh_movement_list()

    # Função para registrar entrada no estoque (chamado na função scan_qr_code ao detectar entrada)
    def register_stock_entry(product_name, quantity):
        record_movement("Entrada", product_name, quantity)
        refresh_movement_list()

    # Função para exibir o registro de movimentações
    def show_movement_history(e):
        page.clean()
        page.appbar = appbar  # Keep the appbar

        # Create a new movement history view
        movement_history_view = ft.Column([
            ft.Text("Histórico de Movimentações", size=30, weight="bold"),
            movement_list,
            ft.ElevatedButton("Voltar", on_click=go_back)
        ], alignment=ft.MainAxisAlignment.START, expand=True)

        page.add(movement_history_view)
        refresh_movement_list()  # Update the movement list
        page.update()

    # Cria a interface de histórico de movimentações
    # movement_history_page = ft.Column(
    #     [
    #         ft.Text("Histórico de Movimentações", size=30),
    #         movement_list,
    #         # ft.ElevatedButton("Voltar", on_click=go_back)  # Botão para voltar ao menu principal
    #     ],
    #     alignment=ft.MainAxisAlignment.START,
    #     expand=True
    # )
    
    # page.add(movement_history_page)
    # page.update()

    # # cards.append(
    # #     create_card(ft.icons.HISTORY, "history", show_movement_history)
    # # )

    def menu_page():
        return ft.Column(
            [
                ft.Text("Sistema de Controle de Estoque", size=24, weight="bold"),
                ft.ElevatedButton("Cadastro de Produtos", on_click=show_product_management_page),
                ft.ElevatedButton("Registro de Movimentações", on_click=show_movement_history),
                ft.ElevatedButton("Histórico de Movimentações", on_click=show_movement_history),
            ]
        )

    # Função para voltar ao menu principal
    def go_back(e):
        page.clean()  # Limpa a interface atual
        page.add(menu_page)  # Retorna para a página do menu principal
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
        if page.user and page.user["role"] == "admin":
            page.clean()
            # Your existing user management page code...
        else:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Access denied. Administrators only."))
            )

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
        stock_exit_dialog = ft.AlertDialog(
            title=ft.Text(translations[current_language]["stock_exit"]),
            content=ft.Column([
                ft.ElevatedButton(
                    translations[current_language]["scan_qr_code"],
                    on_click=lambda e: read_qrcode("exit")
                )
            ]),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: close_dialog(stock_exit_dialog))
            ]
        )
        page.overlay.append(stock_exit_dialog)
        stock_exit_dialog.open = True
        page.update()

    def show_stock_entry_dialog(e):
        stock_entry_dialog = ft.AlertDialog(
            title=ft.Text(translations[current_language]["stock_entry"]),
            content=ft.Column([
                ft.ElevatedButton(
                    translations[current_language]["scan_qr_code"],
                    on_click=lambda e: read_qrcode("entry")
                )
            ]),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: close_dialog(stock_entry_dialog))
            ]
        )
        page.overlay.append(stock_entry_dialog)
        stock_entry_dialog.open = True
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
        actions=[
            language_popup_menu, 
            theme_toggle_button, 
            help_button, 
            ft.IconButton(ft.icons.ADMIN_PANEL_SETTINGS, tooltip="Admin"),
            ft.IconButton(
                ft.icons.HISTORY, 
                tooltip="Ver Histórico", 
                on_click=show_movement_history
            )
        ],
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

def delete_product(product_id):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        connection.commit()
        refresh_product_list()
    except Error as e:
        print(f"Error deleting product: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Executar o app
ft.app(target=main)