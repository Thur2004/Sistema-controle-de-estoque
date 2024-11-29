# Sistema de Controle de Estoque

Um sistema de gerenciamento de estoque multilíngue construído com Python e Flet, com integração de QR code e rastreamento de estoque em tempo real.

## Funcionalidades

- 🌐 Suporte multilíngue (Português, Inglês, Espanhol)
- 🔐 Autenticação de usuário e controle de acesso baseado em funções
- 📦 Gerenciamento de produtos com geração de QR code
- 📊 Rastreamento de movimentação de estoque (entradas/saídas)
- 👥 Gerenciamento de fornecedores
- 🎨 Alternância entre tema claro/escuro
- 📱 Design responsivo
- 📷 Leitura de QR code para operações rápidas de estoque

## Pré-requisitos

- Python 3.8+
- MySQL Server (XAMPP recomendado)
- Webcam (para leitura de QR code)

## Instalação

1. Clone o repositório:

bash
git clone https://github.com/seuusuario/sistema-controle-de-estoque.git
cd sistema-controle-de-estoque

2. Crie um ambiente virtual e ative-o:

bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

3. Instale os pacotes necessários:

bash
pip install -r requirements.txt

4. Configure o banco de dados:
   - Inicie o servidor MySQL (via XAMPP ou outro método)
   - Importe `database.sql` no seu servidor MySQL

## Pacotes Necessários

txt
flet>=0.9.0
mysql-connector-python>=8.0.0
qrcode>=7.3
opencv-python>=4.5.0
numpy>=1.19.0
Pillow>=8.0.0

## Configuração

1. Configuração do banco de dados (em `main.py`):

python
connection = mysql.connector.connect(
host="localhost",
user="root",
password="", # Atualize se você definiu uma senha
database="inventory_system"
)

## Uso

1. Inicie a aplicação:

bash
python main.py

2. Credenciais padrão do administrador:
   - Usuário: `admin`
   - Senha: `admin123`

## Visão Geral das Funcionalidades

### Gestão de Usuários
- Criar/Editar/Excluir usuários
- Atribuir funções (Admin/Usuário)
- Controle de acesso baseado em função

### Gestão de Produtos
- Adicionar/Editar/Excluir produtos
- Gerar QR codes para produtos
- Acompanhar níveis de estoque
- Ler QR codes para operações rápidas

### Operações de Estoque
- Registrar entradas de estoque
- Registrar saídas de estoque
- Visualizar histórico de movimentações
- Leitura de QR code para operações rápidas

### Funcionalidades Adicionais
- Suporte multilíngue
- Alternância de tema
- Documentação de ajuda
- Rastreamento de histórico de movimentações

## Recursos de Segurança

- Autenticação de usuário
- Controle de acesso baseado em função
- Seções exclusivas para administradores
- Login necessário para operações sensíveis

## Agradecimentos

- [Flet](https://flet.dev/) pelo framework de UI
- [OpenCV](https://opencv.org/) pela leitura de QR code
- [QRCode](https://pypi.org/project/qrcode/) pela geração de QR code

## Capturas de Tela

[Em breve...]
