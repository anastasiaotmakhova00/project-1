#!/usr/bin/env python
"""
Flask Calculator Application Entry Point
=========================================
Точка входа для запуска приложения калькулятора.
"""
import os
from dotenv import load_dotenv
from app import create_app

# Загрузка переменных окружения из .env файла
load_dotenv()

# Создание приложения используя Application Factory
app = create_app(config_name=os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Запуск development сервера
    debug = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print("=" * 60)
    print("Flask Calculator Application")
    print("=" * 60)
    print(f"Running on: http://localhost:{port}")
    print(f"Debug mode: {debug}")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )
