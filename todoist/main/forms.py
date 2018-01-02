from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, DateTimeField, DateField
from wtforms.validators import Required, Length
from flask_login import current_user


class AddProject(FlaskForm):
    name = StringField('项目名：', validators=[Required(), Length(1, 64)])
    submit = SubmitField('保存')


class AddTask(FlaskForm):
    task = StringField('任务：', validators=[Required(), Length(1, 64)])
    project = SelectField('项目:')
    timenode = DateField('时间节点：')
    priority = SelectField(
        '优先级：', choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4)], coerce=int)
    tasksave = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(AddTask, self).__init__(*args, **kwargs)
        self.project.choices = [(p.name, p.name)
                                for p in current_user.projects]
