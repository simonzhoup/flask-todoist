from flask import render_template, session, redirect, url_for, request, abort, make_response
from datetime import datetime, timezone, timedelta
from flask_login import login_required, current_user
from .forms import AddProject, AddTask, Search

from . import main
from .. import db
from ..models import User, Project, Task, Titles
from sqlalchemy import and_, or_
from collections import OrderedDict


@main.before_request
def main_form():
    if current_user.is_authenticated:
        projectform = AddProject()
        if projectform.validate_on_submit():
            p = Project(name=projectform.name.data, user_id=current_user.id)
            db.session.add(p)
            return redirect(url_for('.index'))


@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search = Search()
    edit_task_form = AddTask()
    projectform = AddProject()
    if not search.s.data:
        return redirect(url_for('.index'))
    key = '%' + search.s.data + '%'
    tasks = Task.query.filter(Task.task.like(key)).all()
    return render_template('tasks-from-project.html', tasks=tasks, key=search.s.data, search=search, edit_task_form=edit_task_form, projectform=projectform)


@main.route('/add-task', methods=['GET', 'POST'])
@login_required
def add_task():
    edit_task_form = AddTask()
    if edit_task_form.validate_on_submit():
        t = Task(task=taskform.task.data, project=taskform.project.data,
                 timenode=taskform.timenode.data, user_id=current_user.id)
        if taskform.new_title.data:
            nt = Titles(title=taskform.new_title.data,
                        user_id=current_user.id)
            db.session.add(nt)
            db.session.commit()
            t.title = nt.id
            db.session.add(t)
        else:
            t.title = taskform.new_title.data
            db.session.add(t)
        return redirect(request.referrer)


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    now = datetime.now()
    search = Search()
    edit_task_form = AddTask()
    projectform = AddProject()
    today_tasks = current_user.tasks.filter(
        Task.timenode == datetime.now().strftime("%Y-%m-%d")).all()
    overdue_tasks = current_user.tasks.filter(and_(Task.filish == False,
                                                   Task.timenode < datetime.now().strftime("%Y-%m-%d"))).all()
    return render_template('today.html', now=now, search=search, today_tasks=today_tasks, edit_task_form=edit_task_form, projectform=projectform, overdue_tasks=overdue_tasks)


@main.route('/sevenday', methods=['GET', 'POST'])
@login_required
def sevenday():
    search = Search()
    edit_task_form = AddTask()
    projectform = AddProject()
    days = []
    for i in range(7):
        days.append((datetime.now() + timedelta(days=i)
                     ).strftime("%Y-%m-%d"))
    tasks7 = OrderedDict()
    for day in days:
        tasks7[day] = []
        for task in current_user.tasks.all():
            if task.timenode == day:
                tasks7[day].append(task)
    return render_template('seven-day.html', search=search, tasks7=tasks7, edit_task_form=edit_task_form, projectform=projectform)


@main.route('/task/filish/<int:id>')
@login_required
def task_filish(id):
    task = Task.query.get_or_404(id)
    task.filish = True
    db.session.add(task)
    return redirect(request.referrer)


@main.route('/task/unfilish/<int:id>')
@login_required
def task_unfilish(id):
    task = Task.query.get_or_404(id)
    task.filish = False
    db.session.add(task)
    return redirect(request.referrer)


@main.route('/task/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'GET':
        return redirect(url_for('.index'))
    if request.method == 'POST':
        task.task = request.form.get('task_task' + str(id))
        if request.form.get('project' + str(id)):
            task.project = request.form.get('project' + str(id))
        task.timenode = request.form.get('timenode' + str(id))
        task.priority = request.form.get('priority' + str(id))
        db.session.add(task)
    return redirect(request.referrer)


@main.route('/project/<project>', methods=['GET', 'POST'])
@login_required
def project(project):
    p = Project.query.filter_by(name=project).all()
    if not p:
        abort(404)
    tasks = Task.query.filter_by(
        project=project).filter_by(filish=False).all()
    edit_task_form = AddTask()
    projectform = AddProject()
    search = Search()
    return render_template('tasks-from-project.html', search=search, edit_task_form=edit_task_form, projectform=projectform, tasks=tasks, project=project, page_p=project)


@main.route('/title')
@login_required
def show_title():
    resp = make_response(redirect(request.referrer))
    resp.set_cookie('show_what', 'title', max_age=60 * 60 * 24 * 30)
    return resp


@main.route('/project')
@login_required
def show_project():
    resp = make_response(redirect(request.referrer))
    resp.set_cookie('show_what', 'project', max_age=60 * 60 * 24 * 30)
    return resp


@main.route('/title/<title>', methods=['GET', 'POST'])
@login_required
def title(title):
    t = Titles.query.filter_by(title=title).first()
    if not t:
        abort(404)
    tasks = Task.query.filter_by(title=t.id).filter_by(filish=False).all()
    edit_task_form = AddTask()
    projectform = AddProject()
    search = Search()
    return render_template('tasks-from-project.html', search=search, tasks=tasks, edit_task_form=edit_task_form, projectform=projectform, title=title)
