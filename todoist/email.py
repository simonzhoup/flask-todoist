from flask_mail import Message
from threading import Thread
from flask import render_template, current_app
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MYTODOIST_MAIL_PREFIX'] + subject,
                  sender=app.config['MYTODOIST_MAIL_SENDER'], recipients=[to])
    msg.body = render_template('email/' + template + '.txt', **kwargs)
    msg.html = render_template('email/' + template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
