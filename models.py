from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import InputRequired

class VirtualMachine():
    def __init__(self, name, id, status):
        self.name = name
        self.id = id
        self.status = status

class VmForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(message="Поле не может быть пустым")])
    cpu = InputRequired('cpu', validators=[InputRequired(), Length(message="Поле не может быть пустым")])
    ram = InputRequired('name', validators=[InputRequired(), Length(message="Поле не может быть пустым")])
    os = SelectField(u'os', choices = ['Windows','Linux','Mac'], validators = [Required()])
    sdisk = SelectField(u'sdisk', choices = ['Windows','Linux','Mac'], validators = [Required()])
    odisk = StringField('name', validators=[DataRequired()])