# run.py
from app import create_app, db
from app.models import User, Role, Course, Enrollment, LectureSession, Assignment, Submission, Notification, ScreenShareRequest
from flask_migrate import Migrate
import eventlet
from app.extensions import socketio

app = create_app()
migrate = Migrate(app, db)

# Để có thể sử dụng shell context
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'Course': Course, 'Enrollment': Enrollment,
            'LectureSession': LectureSession, 'Assignment': Assignment, 'Submission': Submission,
            'Notification': Notification, 'ScreenShareRequest': ScreenShareRequest}

if __name__ == '__main__':
    socketio.run(app, debug=True)
