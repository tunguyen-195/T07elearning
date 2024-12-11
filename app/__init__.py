# app/__init__.py
from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager, mail, socketio, compress
from flask_login import current_user
from flask_socketio import SocketIO

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Khởi tạo các tiện ích mở rộng
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    socketio.init_app(app, message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'], async_mode='eventlet')
    compress.init_app(app)

    # Đăng ký các Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.student import bp as student_bp
    app.register_blueprint(student_bp, url_prefix='/student')

    from app.lecturer import bp as lecturer_bp
    app.register_blueprint(lecturer_bp, url_prefix='/lecturer')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Đăng ký các Blueprint khác như errors nếu cần
    # from app.errors import bp as errors_bp
    # app.register_blueprint(errors_bp)

    # Định nghĩa lệnh CLI 'seed' bên trong hàm create_app
    @app.cli.command("seed")
    def seed():
        """Chèn dữ liệu mẫu vào cơ sở dữ liệu."""
        from populate_db import populate
        populate()

    return app
