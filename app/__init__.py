"""
Application Factory
===================
Реализует паттерн Application Factory для гибкого создания экземпляра Flask приложения.
Обеспечивает инициализацию расширений, конфигурации и регистрацию маршрутов.
"""
from flask import Flask
from flask_babel import Babel

# Инициализация расширений без привязки к конкретному приложению
babel = Babel()


def create_app(config_name: str = 'development') -> Flask:
    """
    Фабрика приложений для создания экземпляра Flask приложения.
    
    Args:
        config_name: Имя конфигурации ('development', 'testing', 'production')
        
    Returns:
        Готовое к использованию Flask приложение
    """
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    
    # Конфигурация приложения
    app.config['JSON_SORT_KEYS'] = False
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_LANGUAGES'] = {
        'en': 'English',
        'ru': 'Русский'
    }
    
    if config_name == 'testing':
        app.config['TESTING'] = True
    
    # Инициализация расширений
    babel.init_app(app)
    
    # Локализация: функция для определения локали
    @app.before_request
    def before_request():
        """Функция для установки локали перед каждым запросом."""
        # Можно расширить для определения локали по параметрам URL или cookies
        pass
    
    # Регистрация blueprints и маршрутов
    from .routes import register_routes
    register_routes(app)
    
    return app
