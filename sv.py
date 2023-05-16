from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm,Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from riotwatcher import LolWatcher, ApiError

#VAR de iniciacion
db = SQLAlchemy()
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = "thisisasecretkey"
db.init_app(app)

#configuracion del login_manager 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" #Nombre de la instancia del login_manager


@login_manager.user_loader #se utiliza para volver a cargar el objeto de usuario desde el ID de usuario almacenado en la sesión. Debe tomar la ID de cadena de un usuario y devolver el objeto de usuario correspondiente. 
#Carga lo que se va a utiizar despues en def load_user
def load_user(user_id):
    """
    The load_user function is used by Flask-Login to load a user from the database.
    It takes a unicode ID as an argument and returns the corresponding user object.
    
    
    :param user_id: Get the user from the database
    :return: The user object with the given id
    :doc-author: Trelent
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    Modelo de usuario para la base de datos.

    Atributos:
        id (int): ID del usuario (clave primaria).
        username (str): Nombre de usuario del usuario.
        password (str): Contraseña del usuario.
    """
    id = db.Column(db.Integer, primary_key=True)#al declarar primary_key=True para la variable id, se indica que este campo será el identificador único de cada registro de usuario en la tabla correspondiente en la base de datos.
    username = db.Column(db.String(20), nullable=False, unique=True) #al definir nullable=False para username, se establece que cada instancia de User debe tener un valor válido y no nulo para el campo username. Esto significa que el nombre de usuario debe ser proporcionado y no puede dejarse en blanco en la base de datos.
    #Al establecer unique=True para username, se garantiza que no puede haber registros en la base de datos con el mismo valor de username. Esto significa que cada nombre de usuario debe ser único entre todos los registros de la tabla de usuarios.
    password = db.Column(db.String(80), nullable=False)# idem para el nullable 

class RegisterForm(FlaskForm):
    """
    Se crea el form de registroo de usuario, en donde vamos a crear 2 campos de forms, un user y un pass.
    data en https://wtforms.readthedocs.io/en/2.3.x/fields/
    
    Args:
        FlaskForm (_type_): _description_

    Raises:
        ValidationError: _description_
    """
    
    username = StringField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder":"Username"})#Stores and processes data, and generates HTML for a form field.
    password = PasswordField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "Password"})#The same here, idem last line
    """
    los validadores se utilizan para aplicar reglas de validación a los campos de formulario y asegurarse de que los datos ingresados cumplan con ciertos requisitos antes de su procesamiento o almacenamiento.
    El render_kw={"placeholder": "Username"} especifica que el atributo placeholder del campo de texto HTML correspondiente se establece en "Username". Esto hará que el campo de entrada en el formulario muestre la palabra "Username" como una pista visual para el usuario.
    En resumen, render_kw es utilizado para personalizar los atributos HTML de los campos de formulario, y en este caso específico, se utiliza para agregar el atributo placeholder a los campos de texto, proporcionando una pista visual al usuario
    """
    submit = SubmitField("Register")
    
    def validate_user(self, username):
        """
        The validate_user function checks if the username already exists in the database.
        If it does, then a ValidationError is raised and an error message is displayed to 
        the user.
        
        :param self: Make the validate_user function a method of the registerform class
        :param username: Check if the username already exists in the database
        :return: A validationerror if the username already exists
        :doc-author: Trelent
        """
        existing_user_username = User.Query.filter_by(username=username.data).first()
        
        if existing_user_username:
            raise ValidationError("Ese usuario ya existe, elegi otro")
           
class LoginForm(FlaskForm):
    """
    Se crea el form de registro de usuario, en donde vamos a crear 2 campos de forms, un user y un pass.
    data en https://wtforms.readthedocs.io/en/2.3.x/fields/
    
    Args:
        FlaskForm (_type_): _description_

    Raises:
        ValidationError: _description_
    """
    username = StringField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField("Login")



def riot_api():
    """
    The riot_api function is used to get the ranked stats of a user.
    It uses the Riot Games API and returns a dictionary with all the data.
    
    :return: A dictionary with the ranked_stats data
    :doc-author: Trelent
    """
    lol_watcher = LolWatcher(api_key="RGAPI-575daa22-c3e2-4210-892a-36803231ec43")  # api
    region = "la2"
    data_usuario = lol_watcher.summoner.by_name(region, summoner_name=current_user.username)
    
    ranked_stats = lol_watcher.league.by_summoner(region, data_usuario['id'])  # Datos importantes
    return ranked_stats




@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/login", methods=['GET','POST'])
def login():
    """
    The login function is used to log a user into the application.
    The function takes no arguments and returns a rendered template of the login page.
    If the form is validated, it will check if there exists a user with that username in our database. 
    If so, it will then check if their password matches what they entered on the form using bcrypt's built-in method for checking passwords.
    
    :return: A redirect to the dashboard, so it should be a get request
    :doc-author: Trelent
    """
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route("/dashboard", methods=["GET","POST"])
@login_required #If you decorate a view with this, it will ensure that the current user is logged in and authenticated before calling the actual view.
def dashboard():
    datos = riot_api()
    return render_template("dashboard.html",datos = datos)


@app.route("/logout", methods=["GET","POST"])
@login_required #If you decorate a view with this, it will ensure that the current user is logged in and authenticated before calling the actual view.
def logout():
    logout_user()#Logs a user out. (You do not need to pass the actual user.) This will also clean up the remember me cookie if it exists.
    return redirect(url_for("home"))    



@app.route("/register", methods = ['GET','POST'])
def register():
    """
    The register function is responsible for handling the registration of new users.
    It takes in a username and password, hashes the password using bcrypt, and then adds
    the user to the database. It also redirects to login if successful.
    
    :return: A redirect to the login page
    :doc-author: Trelent
    """
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(password=form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
        
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
    