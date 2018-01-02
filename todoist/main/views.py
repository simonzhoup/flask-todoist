from flask import render_template, session, redirect, url_for
from datetime import datetime, timezone, timedelta
from flask_login import login_required, current_user
from .forms import AddProject, AddTask

from . import main
from .. import db
from ..models import User, Project, Task


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    today = datetime.utcnow().replace(
        tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    taskform = AddTask()
    projectform = AddProject()
    if projectform.validate_on_submit():
        p = Project(name=projectform.name.data, user_id=current_user.id)
        db.session.add(p)
        return redirect(url_for('.index'))
    if taskform.validate_on_submit():
        t = Task(task=taskform.task.data, project=taskform.project.data,
                 timenode=taskform.timenode.data)
        db.session.add(t)
        return redirect(url_for('.index'))
    taskform.timenode.data = datetime.now() + timedelta(days=1)
    return render_template('base.html', today=today, taskform=taskform, projectform=projectform)
