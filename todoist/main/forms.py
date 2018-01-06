from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, DateTimeField, DateField
from wtforms.validators import Required, Length, Optional
from flask_login import current_user


class AddProject(FlaskForm):
    name = StringField('项目名：', validators=[Required(), Length(1, 64)])
    submit = SubmitField('保存')


class AddTask(FlaskForm):
    task = StringField('任务：', validators=[Required(), Length(1, 64)])
    title = SelectField('标签：', validators=[Optional()])
    new_title = StringField('新标签：', validators=[Optional(), Length(1, 8)])
    project = SelectField('项目:')
    timenode = StringField('时间节点：')
    priority = SelectField(
        '优先级：', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    tasksave = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(AddTask, self).__init__(*args, **kwargs)
        self.project.choices = [(p.name, p.name)
                                for p in current_user.projects]
        self.title.choices = [(t.id, t.title)
                              for t in current_user.titles]


class EditTask(FlaskForm):
    task = StringField('任务：', validators=[Required(), Length(1, 64)])
    project = SelectField('项目：')
    # title = SelectField('标签：')
    # new_title = StringField('新标签：')
    timenode = StringField('时间节点：')
    priority = SelectField(
        '优先级：', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    tasksave = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(EditTask, self).__init__(*args, **kwargs)
        self.project.choices = [(p.name, p.name)
                                for p in current_user.projects]
        # self.title.choices = [(t.title, t.id)
        #                       for t in current_user.titles]
