from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, BooleanField, SelectField, DateTimeField, DateField
from wtforms.validators import Required, Length, Optional
from flask_login import current_user
from datetime import datetime


class AddProject(FlaskForm):
    name = StringField('项目名：', validators=[Required(), Length(1, 64)])
    submit = SubmitField('保存')


class AddTask(FlaskForm):
    task = StringField('任务：', validators=[Required(), Length(1, 64)])
    title = SelectField('标签：', render_kw={"style": "width:20%;"})
    new_title = StringField('新标签：', validators=[Optional(), Length(
        1, 32)], render_kw={"style": "width:20%;"})
    project = SelectField('项目:', render_kw={"style": "width:20%;"})
    timenode = StringField('时间节点：', render_kw={
                           "style": "width:20%;"}, default=datetime.now().strftime("%Y-%m-%d"))
    priority = SelectField(
        '优先级：', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], render_kw={"style": "width:20%;"})
    submit = SubmitField('保存')

    def __init__(self, *args, **kwargs):
        super(AddTask, self).__init__(*args, **kwargs)
        self.project.choices = [(p.name, p.name)
                                for p in current_user.projects]
        self.title.choices = [(t.id, t.title)
                              for t in current_user.titles]


class Search(FlaskForm):
    s = StringField('', validators=[Required(),
                                    Length(1, 64)], id="search")
    search = SubmitField('提交')
