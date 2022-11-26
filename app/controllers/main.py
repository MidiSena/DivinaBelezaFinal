import os
from app import app
from app import db
from app.models import models
from app.models.models import Clientes, Funcionarios, Servicos, Agendamentos
from flask import render_template, request, redirect, url_for
from sqlalchemy import func
from datetime import datetime
from flask.helpers import flash
from .forms import Cadastro, SearchForm, CriarConta, FuncionarioForm, LoginForm, EditarFuncForm, ServicoForm, CadastrarServicos, AgendaForm, AgendamentoForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    current_user,
    login_user,
    login_required,
    current_user,
    logout_user
)



@app.route('/')
def index():
    return render_template("index.html")


# Pesquisar Cliente
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route('/pesquisar', methods=["GET", "POST"])
@login_required
def pesquisar_cliente():
    form = SearchForm()
    cliente = Clientes.query
    if form.validate_on_submit:
        #pegar os dados do formulário de submissão
        pesquisar_cliente=form.pesquisar.data
        cliente = cliente.filter(func.lower(Clientes.nome)==func.lower(pesquisar_cliente)).all()
    return render_template('pesquisar_cliente.html', pesquisar=pesquisar_cliente, cliente=cliente)

@app.route('/pesquisar/<int:cliente_id>')
def cliente(cliente_id):
    cliente = Clientes.query.get_or_404(cliente_id)
    return render_template('cliente_procurado.html', cliente=cliente)


#cadastrar cliente
@app.route('/cadastro_cliente', methods=['GET', 'POST'])
@login_required
def registro():
    nome = None
    form = Cadastro()
    if request.method == 'POST' and form.validate_on_submit():
            user_email = models.Clientes.query.filter_by(email=form.email.data).first()
            if user_email is None:
                user = models.Clientes(nome=form.nome.data, sobrenome=form.sobrenome.data, cpf=form.cpf.data, email=form.email.data, telefone=form.telefone.data)
                db.session.add(user)
                db.session.commit()
            nome=form.nome.data
            form.nome.data = ''
            form.sobrenome.data = ''
            form.cpf.data = ''
            form.email.data =''
            form.telefone.data=''
            flash('Cadastro realizado com sucesso!', 'success')
            #return render_template('afterCadastro.html')
    return render_template('cadastro_cliente.html', form=form)


#editar cliente
@app.route('/edit/<int:cliente_id>', methods=('GET', 'POST'))
def editar_cliente(cliente_id):
    form = Cadastro()
    cliente = Clientes.query.get_or_404(cliente_id)
    admin = current_user.administrador
    if request.method == "POST":
        cliente.nome = request.form['nome']
        cliente.sobrenome = request.form['sobrenome']
        cliente.cpf = request.form['cpf']
        cliente.email = request.form['email']
        cliente.telefone = request.form['telefone']

        try: 
            db.session.commit()
            flash("Alteração realizada com sucesso!")
            return render_template("pesquisar_cliente.html", 
                    form=form,
                    cliente = cliente,
                    cliente_id=id, admin=admin)
        except:
            flash("Ocorreu um erro, tente Novamente!")
            return render_template("editar_cliente.html",
                    form=form,
                    cliente = cliente,
                    cliente_id=id, admin=admin)
    else:
        
        return render_template("editar_cliente.html", 
				form=form,
				cliente=cliente,
				cliente_id=id, admin=admin)


# apagar cliente
@app.post('/pesquisar/<int:cliente_id>/delete')
@login_required
def delete(cliente_id):
    admin = current_user.administrador
    if admin == 'sim':
        cliente = Clientes.query.get_or_404(cliente_id)
        db.session.delete(cliente)
        db.session.commit()
        return redirect(url_for('pesquisar_cliente', admin=admin))
        
    else:
        flash('Desculpe, você não tem autorização para excluir clientes!')
        return redirect(url_for('pesquisar_cliente'))


#registrar funcionarios
@app.route('/registrofuncionario', methods=['GET', 'POST'])
#@login_required
def registrar_funcionario():
    nome = None
    form = CriarConta()
    if request.method == 'POST' and form.validate_on_submit():
        nome = request.form['nome']
        sobrenome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        telefone = request.form['telefone']
        administrador = request.form['administrador']
        senha = request.form['senha']
                
        user_email = Funcionarios.query.filter_by(email=form.email.data).first()
        if user_email is None:
            user = Funcionarios(nome=form.nome.data, sobrenome=form.sobrenome.data, cpf=form.cpf.data, 
            email=form.email.data, telefone=form.telefone.data,
            administrador=form.administrador.data, senha=generate_password_hash(senha, method='sha256'))
            db.session.add(user)
            db.session.commit()
            
            flash('Cadastro realizado com sucesso!', 'success')
            #return render_template('afterCadastro.html')
    return render_template('registrofuncionario.html', form=form)


#pesquisar funcionario
@app.context_processor
def basef():
    form = FuncionarioForm()
    return dict(form=form)


@app.route('/pesquisarfuncionario', methods=["GET", "POST"])
@login_required
def pesquisar_funcionario():
    form = FuncionarioForm()
    funcionario = Funcionarios.query
    if form.validate_on_submit:
        #pegar os dados do formulário de submissão
        pesquisar_funcionario=form.pesquisarfuncionario.data
        funcionario = funcionario.filter(func.lower(Funcionarios.nome)==func.lower(pesquisar_funcionario)).all()
    return render_template('pesquisar_funcionario.html', pesquisar=pesquisar_funcionario, funcionario=funcionario)


@app.route('/pesquisarfuncionario/<int:funcionario_id>')
@login_required
def funcionario(funcionario_id):
    funcionario = Funcionarios.query.get_or_404(funcionario_id)
    return render_template('funcionario_procurado.html', funcionario=funcionario)


#editar funcionario
@app.route('/editfuncionario/<int:funcionario_id>', methods=('GET', 'POST'))
@login_required
def editfuncionario(funcionario_id):
    form = CriarConta()
    funcionario = Funcionarios.query.get_or_404(funcionario_id)
    admin = current_user.administrador
    
    if request.method == "POST":
        funcionario.nome = request.form['nome']
        funcionario.sobrenome = request.form['sobrenome']
        funcionario.cpf = request.form['cpf']
        funcionario.email = request.form['email']
        funcionario.telefone = request.form['telefone']
        funcionario.administrador = request.form['administrador']
        
        try:
            db.session.commit()
            flash("Alteração realizada com sucesso!")
            return render_template("editar_funcionario.html", 
                form=form,
                funcionario = funcionario,
                funcionario_id=funcionario_id, admin=admin)
        except:
            flash("Ocorreu um erro, tente Novamente!")
            return render_template("editar_funcionario.html", 
                form=form,
                funcionario=funcionario,
                funcionario_id=funcionario_id, admin=admin)
 
    else:
        return render_template("editar_funcionario.html",
                form=form,
                funcionario=funcionario,
                funcionario_id=funcionario_id, admin=admin)


#apagar Funcionario
@app.post('/pesquisarfuncionario/<int:funcionario_id>/delete')
@login_required
def deletefuncionario(funcionario_id):
    admin = current_user.administrador
    if admin == 'sim':
        funcionario = Funcionarios.query.get_or_404(funcionario_id)
        db.session.delete(funcionario)
        db.session.commit()
        return redirect(url_for('pesquisar_funcionario'))
    else:
        flash('Desculpe, você não tem autorização para excluir funcionários!')
        return redirect(url_for('pesquisar_funcionario'))
        
   
#Login   
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Funcionarios.query.filter_by(email=form.email.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.senha, form.senha.data):
                if user.administrador=='sim':
                    login_user(user)
                    flash("Login efetuado com sucesso!")
                
                    return render_template('administrador.html')
                else:
                    login_user(user)
                    flash("Login efetuado com sucesso!")
                    return render_template('areafuncionario.html')
            else:
                flash("Senha incorreta. Tente novamente!")
        else:
            flash("O usuário não existe! Tente novamente!")
    return render_template('login.html', form=form)


#area funcionario
@app.route('/areafuncionario')
@login_required
def areafuncionario():
    return render_template('areafuncionario.html')

@app.route('/areaadministrador')
@login_required
def admin():
    if not current_user.administrador == 'sim':
        flash("Desculpe, você não tem autorização para acessar essa página")
        return render_template('areafuncionario.html')
    else:
        return render_template('administrador.html')
    
#sair do sistema
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("Você saiu do sistema!")
	return redirect(url_for('index'))

#cadastrar serviço
@app.route('/registrarservico', methods=['GET', 'POST'])
@login_required
def registrar_servico():
    form =  CadastrarServicos()
    if request.method == 'POST' and form.validate_on_submit():
        servico = request.form['servico']
        preco = request.form['preco']
        tempo = request.form['tempo']
                        
        servico = models.Servicos.query.filter_by(servico=form.servico.data).first()
        if servico is None:
            servico = models.Servicos(servico=form.servico.data, preco=form.preco.data, tempo=form.tempo.data)
            db.session.add(servico)
            db.session.commit()
            
            flash('Cadastro realizado com sucesso!', 'success')
            #return render_template('afterCadastro.html')
    return render_template('registroservico.html', form=form)

# Pesquisar serviço
@app.context_processor
def bases():
    form = ServicoForm()
    return dict(form=form)


@app.route('/pesquisarservico', methods=["GET", "POST"])
@login_required
def pesquisar_servico():
    form = ServicoForm()
    servico = Servicos.query
    if form.validate_on_submit:
        #pegar os dados do formulário de submissão
        pesquisar_servico=form.pesquisarservico.data
        servico = servico.filter(func.lower(Servicos.servico)==func.lower(pesquisar_servico)).all()
    return render_template('pesquisar_servico.html', pesquisar=pesquisar_servico, servico=servico)


@app.route('/pesquisarservico/<int:servico_id>')
@login_required
def servico(servico_id):
    servico = Servicos.query.get_or_404(servico_id)
    return render_template('servico_procurado.html', servico=servico)

#editar serviço
@app.route('/<int:servico_id>/editarservico', methods=('GET', 'POST'))
@login_required
def editar_servico(servico_id):
    form = CadastrarServicos()
    servico = Servicos.query.get_or_404(servico_id)
    if request.method == "POST":
        servico.servico = request.form['servico']
        servico.preco = request.form['preco']
        servico.tempo = request.form['tempo']

        try:
            db.session.commit()
            flash("Alteração realizada com sucesso!")
            return render_template("pesquisar_servico.html", 
				form=form,
				servico = servico,
                servico_id=servico_id)
        except:
            #flash("Ocorreu um erro, tente Novamente!")
            return render_template("editar_servico.html", 
				form=form,
				servico = servico,
                servico_id=servico_id)
    else:
        return render_template("editar_servico.html", 
				form=form,
				servico = servico,
                servico_id=servico_id)

#apagar Serviço
@login_required
@app.post('/pesquisarservico/<int:servico_id>/delete')
@login_required
def delete_servico(servico_id):
    admin = current_user.administrador
    if admin == 'sim':
        servico = Servicos.query.get_or_404(servico_id)
        db.session.delete(servico)
        db.session.commit()
        return redirect(url_for('pesquisar_servico'))
    else:
        flash('Desculpe, você não tem autorização para excluir servicos!')
        return redirect(url_for('pesquisar_servico'))
################################################################################
############################### AGENDA #########################################
################################################################################

@app.route('/criar_agendamento', methods=['GET', 'POST'])
def criar_agendamento():
    form = AgendaForm()
    funcionario = Funcionarios.query.filter_by().all()
    cliente = Clientes.query.filter_by().all()
    servico = Servicos.query.filter_by().all()
    agenda = {'agendamento_id': "", 'cliente_id': "", 'servico_id': "", 'id': ""}
    
    today_datetime = datetime.today().strftime('%Y-%m-%d %H:%M')
    today_datetime = datetime.strptime(today_datetime, '%Y-%m-%d %H:%M')

    if request.method == 'POST' and form.validate_on_submit:
        cliente_id = request.form.get('cliente_id')
        agendamento_data = request.form.get('data')
        servico_id = request.form.get("servico_id")
        id = request.form.get("id") #id_funcionario

        print(agendamento_data, type(agendamento_data))

        servicos = Servicos.query.filter_by(servico_id=form.servico_id.data).first()

        datafim =  (str(form.agendamento_data.data)[:-6] + ' ' + str(int(str(form.agendamento_data.data)[-5:-3]) + servicos.tempo)
                     +str(form.agendamento_data.data)[-3:])
        agendamento_data_fim  = datetime.strptime(datafim, '%Y-%m-%d %H:%M')

        verificar_horario = Agendamentos.query.filter_by().all()
  
        datainicio =  (str(form.agendamento_data.data)[:-6] + ' ' +
                       str(form.agendamento_data.data)[-5:])
        agendamento_data_inicio  = datetime.strptime(datainicio, '%Y-%m-%d %H:%M')

        b = 0

        for horario in verificar_horario:
            if (agendamento_data_inicio >= horario.agendamento_data and agendamento_data_inicio <= horario.agendamento_data_fim) or (agendamento_data_fim >= horario.agendamento_data and agendamento_data_fim <= horario.agendamento_data_fim):
                 if int(id) == horario.id or int(cliente_id) == horario.cliente_id:
                    b=b+1
        if b > 0:
            a = 1
        else:
            a = None

        open_datetime = str(form.agendamento_data.data)[:-6] + ' 09:00'
        open_datetime = datetime.strptime(open_datetime, '%Y-%m-%d %H:%M')
        close_datetime = str(form.agendamento_data.data)[:-6] + ' 19:00'
        close_datetime = datetime.strptime(close_datetime, '%Y-%m-%d %H:%M')

        if a == None:
            if agendamento_data_inicio < today_datetime or agendamento_data_inicio<open_datetime or agendamento_data_inicio>close_datetime:
                flash('Data ou horário inválido', 'danger')
            else:
                agendamento = Agendamentos(cliente_id=form.cliente_id.data, agendamento_data=form.agendamento_data.data,
                                            agendamento_data_fim=agendamento_data_fim, servico_id=form.servico_id.data,
                                            id=form.id.data)
                db.session.add(agendamento)
                db.session.commit()
            
                flash('Agendamento realizado com sucesso', 'success')
                return redirect(url_for('criar_agendamento'))
        else:
                flash('Já existe agendamento no horário selecionado', 'danger')
                return redirect(url_for('criar_agendamento'))
    return render_template("agendamentos.html", form=form, funcionarios=funcionario,
                            cliente=cliente, servicos=servico, agendamento=agenda)

    
@app.route('/agendamentos')
def agendamentos():
    agendamentos = db.session.query(Clientes, Funcionarios, Agendamentos).\
        select_from(Agendamentos).join(Clientes).join(Funcionarios).order_by(Agendamentos.agendamento_data).all()
    return render_template("agenda1.html", agendamentos=agendamentos)

# Pesquisar agendamentos
@app.route('/pesquisaragendamento', methods=["GET", "POST"])
@login_required
def pesquisar_agendamento():
    form = AgendamentoForm()
    agendamento = Agendamentos.query
    if form.validate_on_submit:
        #pegar os dados do formulário de submissão
        pesquisar_agendamento=form.pesquisaragendamento.data
        agendamento = agendamento.filter(func.lower(Agendamentos.agendamento)==func.lower(pesquisar_agendamento)).all()
    return render_template('pesquisar_agendamento.html', pesquisar=pesquisar_agendamento, agendamento=agendamento)


@app.route('/agendamentos/<int:agendamento_id>')
@login_required
def agendamento(agendamento_id):
    agendamento = Agendamentos.query.get_or_404(agendamento_id)
    return render_template('agendamento_procurado.html', agendamento=agendamento)

#EditarAgendamentos
@app.route('/editaragendamento/<int:agendamento_id>', methods=('GET', 'POST'))
#@login_required
def editagendamento(agendamento_id):
    form = AgendaForm()
    funcionario = Funcionarios.query.filter_by().all()
    servico = Servicos.query.filter_by().all()
    agendamento = Agendamentos.query.get_or_404(agendamento_id)
    cliente = Clientes.query.filter_by(cliente_id=agendamento.cliente_id).first()


    if request.method == "POST":
        agendamento.cliente_id = request.form.get('cliente_id')
        agendamento.agendamento_data = request.form.get('agendamento_data')
        agendamento.servico_id = request.form.get('servico_id')
        agendamento.id = request.form.get('id')

        today_datetime = datetime.today().strftime('%Y-%m-%d %H:%M')
        today_datetime = datetime.strptime(today_datetime, '%Y-%m-%d %H:%M')

        servicos = Servicos.query.filter_by(servico_id=form.servico_id.data).first()
        
        datafim =  (str(form.agendamento_data.data)[:-9] + ' ' + str(int(str(form.agendamento_data.data)[-9:-6]) + servicos.tempo)
                     +str(form.agendamento_data.data)[-6:])
        agendamento_data_fim  = datetime.strptime(datafim, '%Y-%m-%d %H:%M:%S')

        verificar_horario = Agendamentos.query.filter_by().all()
  
        datainicio =  (str(form.agendamento_data.data)[:-9] + ' ' +
                       str(form.agendamento_data.data)[-8:])
        agendamento_data_inicio  = datetime.strptime(datainicio, '%Y-%m-%d %H:%M:%S')
        b = 0

        for horario in verificar_horario:
            if type(horario.agendamento_data)==str:
                horario_AD = datetime.strptime(horario.agendamento_data, '%Y-%m-%d %H:%M:%S')
            else: horario_AD = horario.agendamento_data

            if type(horario.agendamento_data_fim)==str:
                horario_ADF = datetime.strptime(horario.agendamento_data_fim, '%Y-%m-%d %H:%M:%S')
            else: horario_ADF = horario.agendamento_data_fim

            if (agendamento_data_inicio >= horario_AD  and agendamento_data_inicio <= horario_ADF) or (agendamento_data_fim >= horario_AD  and agendamento_data_fim <= horario_ADF):
                 if int(agendamento.id) == horario.id or int(agendamento.cliente_id) == horario.cliente_id:
                    b=b+1
        if b > 0:
            a = 1
        else:
            a = None
        open_datetime = str(form.agendamento_data.data)[:10] + ' 09:00'
        open_datetime = datetime.strptime(open_datetime, '%Y-%m-%d %H:%M')
        close_datetime = str(form.agendamento_data.data)[:10] + ' 19:00'
        close_datetime = datetime.strptime(close_datetime, '%Y-%m-%d %H:%M')

        if a == None and agendamento_data_inicio >= today_datetime and agendamento_data_inicio>=open_datetime and agendamento_data_inicio<=close_datetime: # and ....
            agendamento.agendamento_data_fim = agendamento_data_fim
            try:
                db.session.commit()
                flash("Alteração realizada com sucesso!")
                return redirect(url_for("agendamentos"))
            except:
                #flash("Ocorreu um erro, tente Novamente!")
                return redirect(url_for("agendamentos"))
        else:
            flash('Data ou horário inválido', 'danger')

    return render_template("editar_agendamento.html", 
                    form=form,
                    agendamento=agendamento,
                    agendamento_id=agendamento_id,
                    cliente=cliente,
                    funcionario=funcionario,
                    servico=servico)


#ApagarAgendamento
@login_required
@app.post('/delete/<int:agendamento_id>')
@login_required
def delete_agendamento(agendamento_id):
    agendamento = Agendamentos.query.get_or_404(agendamento_id)
    db.session.delete(agendamento)
    db.session.commit()
    flash('Agendamento apagado com sucesso')
    return redirect(url_for('agendamentos'))
