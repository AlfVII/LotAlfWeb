from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField, TextAreaField, StringField, EmailField, RadioField, FloatField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Optional, InputRequired
from datetime import datetime
from app import local_db


class RequiredIf(DataRequired):
    """Validator which makes a field required if another field is set and has a truthy value.

    Usage::
        login_method = StringField('', [AnyOf(['email', 'facebook'])])
        email = StringField('', [RequiredIf(login_method='email')])
        password = StringField('', [RequiredIf(login_method='email')])
        facebook_token = StringField('', [RequiredIf(login_method='facebook')])
    Sources:
        - http://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - http://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms
        - https://gist.github.com/devxoul/7638142#file-wtf_required_if-py
    """
    field_flags = ('requiredif',)

    def __init__(self, message=None, *args, **kwargs):
        super(RequiredIf).__init__()
        self.message = message
        self.conditions = kwargs

    # field is requiring that name field in the form is data value in the form
    def __call__(self, form, field):
        for name, data in self.conditions.items():
            other_field = form[name]
            if other_field is None:
                raise Exception('no field named "%s" in form' % name)
            if other_field.data == data and not field.data:
                DataRequired.__call__(self, form, field)
            Optional()(form, field)


class NumberForm(FlaskForm):

    local_db_inst = local_db.LocalDB()
    regions = local_db_inst.get_all_regions()

    statuses = ['Perfecto', 'Defectuoso', 'Falta']
    coins = ['Selecciona la moneda', 'Euro', 'Peseta']
    initial_year = 1967
    maximum_lot = 105
    origins = ['Selecciona el origen', 'Ordinario', 'Navidad', 'Extraordinario', 'Especial', 'Niño', 'Antiguo', 'Jueves', 'Escrito']
    retailer_regions = regions
    retailer_regions.insert(0, "Selecciona la comunidad")
    lot_choices = [(x, x) for x in range(1, maximum_lot + 2)]
    lot_choices.insert(0, ("Default", "Selecciona el sorteo"))
    year_choices = [(x, x) for x in range(initial_year, datetime.now().year + 1)]
    year_choices.insert(0, ("Default", "Selecciona el año"))

    status = SelectField(u'Estado', choices=[(status, status) for status in statuses], validators=[DataRequired()])
    origin = SelectField(u'Origen', choices=[(origin, origin) if origin != 'Selecciona el origen' else ("Default", "Selecciona el origen") for origin in origins])
    lot = SelectField(u'Sorteo', choices=lot_choices, validators=[Optional()])
    year = SelectField(u'Año', choices=year_choices, validators=[Optional()])
    coin = SelectField(u'Moneda', choices=[(coin, coin) if coin != 'Selecciona la moneda' else ("Default", "Selecciona la moneda") for coin in coins], validators=[Optional()])
    retailer_region = SelectField(u'Comunidad', choices=[(retailer_region.title(), retailer_region.title()) if retailer_region != "Selecciona la comunidad" else ("Default", "Selecciona la comunidad") for retailer_region in retailer_regions], validators=[Optional()])
    retailer_province = SelectField(u'Provincia', validators=[Optional()])
    retailer_town = SelectField(u'Municipio', validators=[Optional()])
    retailer_number = IntegerField(u'Número', validators=[Optional()])
    copies = IntegerField(u'Número de copias', default=1, validators=[DataRequired()])

    submit = SubmitField('Guardar')


class PostForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    post = TextAreaField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Añadir comentario')


class RetailerForm(FlaskForm):

    local_db_inst = local_db.LocalDB()
    regions = local_db_inst.get_all_regions()
    retailer_regions = regions
    retailer_regions.insert(0, "Selecciona la comunidad")
    retailer_region = SelectField(u'Comunidad', choices=[(retailer_region.title(), retailer_region.title()) if retailer_region != "Selecciona la comunidad" else ("Default", "Selecciona la comunidad") for retailer_region in retailer_regions], validators=[Optional()])
    retailer_province = SelectField(u'Provincia', validators=[Optional()])
    retailer_town = SelectField(u'Municipio', validators=[Optional()])
    retailer_number = IntegerField(u'Número', validators=[Optional()])
    retailer_street = TextAreaField(u'Calle', validators=[Optional()], render_kw={"rows": 1})
    retailer_street_number = TextAreaField(u'Nº de calle', validators=[Optional()], render_kw={"rows": 1})
    retailer_postal_code = IntegerField(u'Cód. postal', validators=[Optional()])
    retailer_telephone = IntegerField(u'Nº telefono', validators=[Optional()])
    retailer_latitude = FloatField(u'Latitud', validators=[Optional()])
    retailer_longitude = FloatField(u'Lonfigud', validators=[Optional()])

    number = IntegerField(u'Nº lotería', validators=[RequiredIf(owned='Owned')])
    owned = RadioField(u'', choices=[("Owned", "Está en la colección"), ("Not owned", "Falta la colección")], validators=[Optional()])
    submit_save = SubmitField('Guardar')
