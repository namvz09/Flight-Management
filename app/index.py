from flask_login import current_user
from app import app, login, controllers, dao, admin
from flask import render_template, request, redirect, session
from app.models import UserRole, Comment, FlightSchedule
from app import db

app.add_url_rule('/', 'index', controllers.index, methods=['get', 'post'])
app.add_url_rule('/login', 'login', controllers.login, methods=['get', 'post'])
app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controllers.logout)
app.add_url_rule('/forgotPass', 'forgotPass', controllers.forgotPass, methods=['get', 'post'])


app.add_url_rule('/flight_list', 'flight_list', controllers.flight_list, methods=['get'])
app.add_url_rule('/form_ticket/<int:f_id>', 'form_ticket', controllers.form_ticket, methods=['get'])
app.add_url_rule('/pay/<int:f_id>', 'pay', controllers.pay, methods=['get'])
app.add_url_rule('/preview_ticket/<int:u_id>', 'preview_ticket', controllers.preview_ticket, methods=['get'])

app.add_url_rule('/api/flight_schedule', 'create_flight_schedule', controllers.create_flight_schedule,
                 methods=['post', 'patch'])
app.add_url_rule('/api/flight_schedule/search', 'search_flight_schedule', controllers.search_flight_schedule,
                 methods=['post'])
app.add_url_rule('/api/form_ticket/<int:f_id>', 'create_form_ticket', controllers.create_form_ticket,
                 methods=['post'])
app.add_url_rule('/api/webhook', 'webhook', controllers.webhook, methods=['POST'])
app.add_url_rule('/api/momo_payment/<int:f_id>', 'momo_payment', controllers.momo_payment, methods=['POST'])
app.add_url_rule('/api/pay/<int:f_id>', 'pay_ticket', controllers.pay_ticket,
                 methods=['post'])
app.add_url_rule('/api/flight_schedule/add/<int:f_id>', 'add_flight_schedule', controllers.add_flight_schedule,
                 methods=['post'])
app.add_url_rule('/api/flight_schedule/delete/<int:f_id>', 'delete_flight_schedule', controllers.delete_flight_schedule,
                 methods=['post'])
app.add_url_rule('/api/user/confirm', 'confirm_user', controllers.confirm_user,
                 methods=['post'])
app.add_url_rule('/api/admin_rules', 'create_admin_rules', controllers.create_admin_rules,
                 methods=['post'])
app.add_url_rule('/api/get_stats/<int:month>', 'get_stats', controllers.get_stats,
                 methods=['post'])


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_attributes():
    return {
        'user_role': UserRole
    }

@app.route('/flight_schedule/<int:flight_id>/comments', methods=['GET', 'POST'])
def flight_schedule_comments(flight_id):
    if request.method == 'POST':
        content = request.form['content']
        author_id = current_user.id
        comment = Comment(flight_sche_id=flight_id, author_id=author_id, content=content)
        db.session.add(comment)
        db.session.commit()

    flight_schedule = FlightSchedule.query.get(flight_id)
    comments = flight_schedule.comments

    return render_template('flight_schedule_comments.html', flight_schedule=flight_schedule, comments=comments)


if __name__ == '__main__':
    app.run(debug=True)
