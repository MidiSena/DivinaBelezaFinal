from xmlrpc.client import Boolean
from app import app
from flask import Blueprint, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import form, StringField, SubmitField, IntegerField, PasswordField, SelectField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email, NumberRange, length, ValidationError
from app import db
from app.models import models


class SearchForm(FlaskForm):
    pesquisar=StringField("Pesquisar", validators=[DataRequired()])
    submit = SubmitField("Submit")

class Cadastro(FlaskForm):

    nome = StringField("Nome", validators=[DataRequired(message="Campo obrigatório."),
            length(min=1, max=64, message="O nome é muito longo. Por favor, use abreviação ")
        ])
    sobrenome = StringField("Sobrenome", validators=[DataRequired(message="Campo obrigatório."),
            length(min=1, max=64, message="O nome é muito longo. Por favor, use abreviação ")
        ])
    cpf = IntegerField("CPF", validators=[NumberRange(min=10000000000, max=99999999999)])
    email = EmailField("E-mail", validators=[DataRequired(), length(min=2, max=30)])
    telefone = IntegerField("Telefone", validators=[DataRequired()])
    submit = SubmitField('Registrar')


    def validate_email(self, email):
        user_email = models.Clientes.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError("E-mail já cadastrado. Indique outro.")

    def validate_cpf(self, cpf):
        user_cpf = models.Clientes.query.filter_by(cpf=cpf.data).first()
        if user_cpf:
            raise ValidationError("Já existe usuário com esse CPF.")

class CriarConta(FlaskForm):
    nome = StringField('Nome',
                         id='username_create',
                         validators=[DataRequired()])
    sobrenome = StringField('Sobrenome',
                         id='sobrenome_create',
                         validators=[DataRequired()])
    cpf = IntegerField("CPF", validators=[NumberRange(min=10000000000, max=99999999999)])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), length(min=2, max=30)])
    telefone = StringField("Telefone", validators=[DataRequired()])
    administrador = StringField('Administrador',
                             id='administrador_create',
                             validators=[DataRequired()])
    senha = PasswordField('Senha',
                             id='pwd_create',
                             validators=[DataRequired()])
    submit = SubmitField('Registrar')
        
    def validate_email(self, email):
        user_email = models.Funcionarios.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError("E-mail já cadastrado. Indique outro.")
    def validate_cpf(self, cpf):
        user_cpf = models.Funcionarios.query.filter_by(cpf=cpf.data).first()
        if user_cpf:
            raise ValidationError("Já existe funcionário cadastrado com esse CPF.")

class FuncionarioForm(FlaskForm):
    pesquisarfuncionario=StringField("Pesquisar", validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])
    submit = SubmitField("Submit")

class EditarFuncForm(FlaskForm):
    nome = StringField('Nome',
                         id='username_create',
                         validators=[DataRequired()])
    sobrenome = StringField('Sobrenome',
                         id='sobrenome_create',
                         validators=[DataRequired()])
    cpf = IntegerField("CPF", validators=[NumberRange(min=10000000000, max=99999999999)])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), length(min=2, max=30)])
    telefone = IntegerField("Telefone", validators=[NumberRange(min=1000000000, max=9999999999)])
    administrador = StringField('Administrador',
                             id='administrador_create',
                             validators=[DataRequired()])
    submit = SubmitField('Registrar')

class CadastrarServicos(FlaskForm):
    servico = StringField("Serviço", validators=[DataRequired(message="Campo obrigatório."),
            length(min=1, max=64, message="O nome é muito longo. Por favor, use abreviação ")
        ])
    preco = StringField("Preço", validators=[DataRequired(message="Campo obrigatório."),
            length(min=1, max=64, message="O nome é muito longo. Por favor, use abreviação ")
        ])
    tempo = IntegerField("Tempo", validators=[NumberRange(min=1, max=24)])
    submit = SubmitField('Cadastrar')

class ServicoForm(FlaskForm):
    pesquisarservico=StringField("Pesquisar", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AgendaForm(FlaskForm):
    cliente_id = StringField('Cliente',
                             id='id_create',
                             validators=[DataRequired()])
    agendamento_data = StringField('Data',
                       id='data_create',
                       validators=[DataRequired()])
    
    servico_id = StringField('Serviço',
                             id='servico_create',
                             validators=[DataRequired()])
    id = StringField('Funcionario',
                             id='funcionario_create',
                             validators=[DataRequired()]) # funcionario_id
    submit = SubmitField("Cadastrar")

class ServicoForm(FlaskForm):
    pesquisarservico=StringField("Pesquisar", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AgendamentoForm(FlaskForm):
    pesquisaragendamento=StringField("Pesquisar", validators=[DataRequired()])
    submit = SubmitField("Submit")
    