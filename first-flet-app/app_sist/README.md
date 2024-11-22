# Sistema de Controle de Estoque

An inventory control system built with Python and Flet, using MySQL for data storage.

## Features

- User management with role-based access control
- Product management with QR code support
- Supplier management
- Category management
- Stock movement tracking
- Movement history with filtering
- Multi-language support (PT-BR, EN, ES)
- Dark/Light theme support

## Technical Stack

- Python 3.12
- Flet for UI
- MySQL for database
- QR Code generation and scanning
- OpenCV for QR code reading

## Database Structure

- Users table for authentication and authorization
- Categories table for product organization
- Suppliers table for product sourcing
- Products table with QR code support
- Movements table for stock transactions

## Setup

1. Install required packages:
pip install flet mysql-connector-python qrcode opencv-python numpy


2. Set up the database:
- Install XAMPP
- Start MySQL service
- Import database.sql

3. Run the application:
python first-flet-app/app_sist/main.py