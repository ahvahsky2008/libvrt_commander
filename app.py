from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import InputRequired

from flask.templating import render_template
from libvirt_wrapper import get_vms, start_vm, stop_vm
from flask import Flask
app = Flask(__name__)

class VmForm(FlaskForm):
    storage_disks = []
    optical_disks = []
    name = StringField('name', validators=[InputRequired(), Length(message="Поле не может быть пустым")])
    cpu = InputRequired('cpu', validators=[InputRequired(), Length(message="Поле не может быть пустым")])
    ram = InputRequired('name', validators=[InputRequired(), Length(message="Поле не может быть пустым")])
    os = SelectField(u'os', choices = ['Windows','Linux','Mac'], validators = [Required()])
    sdisk = SelectField('sdisk')
    odisk = SelectField('odisk')


@app.route('/manage/create_vm')
def manage_create_vm():
    form = VmForm()
    form.sdisk = get_vms()
    if form.validate_on_submit():
        name = form.name.data
        cpu = form.cpu.data
        ram = form.ram.data
        os = form.os.data

    pass

@app.route('/list_vms')
@app.route('/')
def list_vms():
    vms = get_vms()
    for vm in vms:
        print(vm.name)
    return render_template('list_vms.html', vms = vms)



@app.route('/manage/<int:vm_id>/start')
def start(vm_id):
    start_vm(vm_id)
    
    return render_template('list_vms.html', vms = vms)


@app.route('/manage/<int:vm_id>/stop')
def stop(vm_id):
    stop_vm(vm_id)
    
    return render_template('list_vms.html', vms = vms)





if __name__ == '__main__':
    app.run(debug=True)


#создать ВМ
#подключить образ диска к жесткому диску
#подключить образ диска к оптическому диску

#уметь стартовать ВМ
#останавливать
#ставить на паузу
#резьюмить
#сохранять состояние ВМ (save).