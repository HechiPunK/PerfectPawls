import os
from flask import Flask, render_template, request, redirect, url_for, flash #aqui mando a llamar flask
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

from config import config

#modelos
from models.ModelSocioeconomic import ModelSocioeconomic
from models.ModelUser import ModelUser
from models.ModelAdoptions import ModelAdoptions
from models.ModelShelters import ModelShelters

#entities
from models.entities.Socioeconomic import Socioeconomic
from models.entities.User import User
from models.entities.Adoptions import Adoption
from models.entities.Shelter import Shelter

#Aqui voy a crear una instancia de flask
app=Flask(__name__)

#aqui se declara el maiil
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'perfectpawls410@gmail.com'
app.config['MAIL_PASSWORD'] = 'cgla xufr jaan zgdj'  # Asegúrate de usar un App Password
mail = Mail(app)

#Declara la proteccion a formularios, Inicializa la ejecucion de la conexion y habilita las sesiones
csrf=CSRFProtect()
db=MySQL(app)
login_manager_app=LoginManager(app)

#configuracion de la carpeta de imagenes
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

PROFILE_UPLOAD_FOLDER = 'static/profile_pics'
app.config['PROFILE_UPLOAD_FOLDER'] = PROFILE_UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(subject, recipients, body, sender=None):
    """
    Función para enviar correos electrónicos.
    """
    try:
        sender = sender or app.config['MAIL_USERNAME']  # Usa el correo configurado
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = body
        mail.send(msg)
        return True
    except Exception as ex:
        print(f"Error al enviar el correo: {ex}")
        return False

#carga el usuario
@login_manager_app.user_loader
def load_user(id):
    user = ModelUser.get_by_id(db, id)
    if user:
        return user
    shelter = ModelShelters.get_by_id(db, id)
    return shelter

@app.context_processor
def inject_user_type():
    if current_user.is_authenticated:
        return {'is_shelter': isinstance(current_user, Shelter)}
    return {'is_shelter': False}

#Aqui van las rutas o sea mis enlaces
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def ruta_login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']

        # Intentar autenticar como usuario normal
        user = User(0, username, password)
        logged_user = ModelUser.login(db, user)
        if logged_user and logged_user.password:
            login_user(logged_user)
            return redirect(url_for('ruta_profile'))

        # Intentar autenticar como refugio
        shelter = Shelter(0, username, password)
        logged_shelter = ModelShelters.login(db, shelter)
        if logged_shelter and logged_shelter.password:
            login_user(logged_shelter)
            return redirect(url_for('ruta_profile_refugio'))

        # Si no se encuentra en ninguna tabla
        flash("Invalid username or password", "danger")
    return render_template('login.html')

@app.route('/newaccount', methods = ['GET', 'POST'])
def ruta_newaccount():
    if request.method == 'POST':
        username = request.form['username']
        mail = request.form['e-mail']
        password = request.form['password']
        phone = request.form['phone']  
        user = User(0, username, password, mail, phone)
        #Esto lo agregue para validar que tenga 10 numeros el phone
        if not phone or len(phone) != 10:
            flash("The telephone number must be exactly 10 digits long.")
            return render_template('newaccount.html')
        #Esto era para checar por que no se mandaba el numero
        print(f"Datos recibidos: {username}, {mail}, {password}, {phone}")
        
        if ModelUser.register(db, user):
            flash("User successfully registered")
            return redirect(url_for('index'))
        else:
            flash("Error when registering the user. Possibly already exists.")
            return render_template('newaccount.html')
    return render_template('newaccount.html')

@app.route('/adoptions', methods=['GET'])
def ruta_cat():
    try:
        adoptions = ModelAdoptions.get_all(db)
        
        # Obtener los parámetros de búsqueda
        types = request.args.getlist('type')
        sizes = request.args.getlist('size')
        ages = request.args.getlist('age') 
        colors = request.args.getlist('color')

        # Filtrar las adopciones según los criterios seleccionados
        if types or sizes or ages or colors:
            filtered_adoptions = [
                adoption for adoption in adoptions
                if (not types or adoption.type in types) and
                (not sizes or adoption.size in sizes) and
                (not ages or adoption.age in ages) and
                (not colors or adoption.color in colors)
            ]
            adoptions = filtered_adoptions

        # Verificar si se encontraron resultados
        no_results = len(adoptions) == 0

        return render_template('adoptions.html', adoptions=adoptions, no_results=no_results)
    except Exception as ex:
        flash(str(ex))
        return redirect(url_for('index'))

@app.route('/add-adoption', methods=['GET', 'POST'])
@login_required
def ruta_add():
    if request.method == 'POST':
        image_file = request.files['image']
        
        # Verificar si la imagen es válida y guardarla
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)  # Guarda la imagen en la carpeta 'static/img'

        # Guardar solo la ruta relativa en la base de datos
            image_url = f"img/{filename}"
            name = request.form['name']
            pet_type = request.form['type']
            sex = request.form['sex']
            age = request.form['age']
            size = request.form['size']
            color = request.form['color']
            sterilized = request.form['sterilized']
            vaccinated = request.form['vaccinated']
            description = request.form['description']
            id_sesion = current_user.id  

            new_adoption = Adoption(0, image_url, pet_type, name, sex, age, size, color, sterilized, vaccinated, description, id_sesion )

            try:
                if ModelAdoptions.add_adoption(db, new_adoption):
                    flash("Registration successfully completed", "success")
                    return redirect(url_for('ruta_cat'))
                else:
                    flash("Error when registering the pet", "danger")
            except Exception as ex:
                flash(str(ex))
                return redirect(url_for('index'))
            
    return render_template('addadoption.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('ruta_login'))

#agregue para que te aparezcan las mascotas que has subido.
@app.route('/profile')
@login_required
def ruta_profile():
    # Verificar que no sea un refugio
    if isinstance(current_user, Shelter):
        flash("Access denied", "danger")
        return redirect(url_for('ruta_login'))
    
    # Obtener las adopciones del usuario logueado
    id_sesion = current_user.id  # Obtener el ID del usuario logueado
    adoptions = ModelAdoptions.get_by_id(db, id_sesion)

    # Pasar las adopciones al template
    return render_template('profile.html', adoptions=adoptions)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    id_sesion = current_user.id  # Obtener el ID del usuario logueado
    print(f"Usuario actual: {id_sesion}, Adopción a eliminar: {id}")
    print(dir(ModelAdoptions))  

    if ModelAdoptions.delete(db, id, id_sesion):  # Llamar al método para eliminar la adopción
        flash("Adoption successfully removed", "success")
    else:
        flash("You do not have permission to delete this adoption", "danger")
    
    return redirect(url_for('ruta_profile'))

@app.route('/profile-refugio')
@login_required
def ruta_profile_refugio():
    # Verificar que sea un refugio
    if not isinstance(current_user, Shelter):
        flash("Access denied", "danger")
        return redirect(url_for('ruta_login'))
    return render_template('profile_refugio.html')

@app.route('/update-profile', methods=['GET', 'POST'])   
@login_required
def update_profile():
    if request.method == 'POST':
        # Procesar los datos del formulario
        image = request.files.get('profile_pic')
        description = request.form.get('description')
        phone = request.form.get('phone')
        address = request.form.get('address')

        # Manejar la imagen
        profile_pic_path = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            profile_pic_path = os.path.join(app.config['PROFILE_UPLOAD_FOLDER'], filename)
            image.save(profile_pic_path)
            profile_pic_path = f'profile_pics/{filename}'

        # Actualizar el objeto del usuario
        current_user.profile_pic = profile_pic_path if profile_pic_path else current_user.profile_pic
        current_user.description = description if description else current_user.description
        current_user.phone = phone if phone else current_user.phone
        current_user.address = address if address else current_user.address


        try:
            # Guardar en la base de datos
            if ModelUser.update_profile(db, current_user):
                flash("Profile successfully updated", "success")
                # Refrescar datos del usuario
                db.connection.commit()
            else:
                flash("No changes were made", "info")
        except Exception as ex:
            flash(str(ex), "danger")

        return redirect(url_for('ruta_profile'))

    return render_template('update_profile.html', user=current_user)

@app.route('/socioeconomic', methods=['GET', 'POST'])
@login_required
def ruta_study():
    if request.method == 'POST':
        pregunta1 = request.form['pregunta1']
        pregunta2 = request.form['pregunta2']
        pregunta3 = request.form['pregunta3']
        pregunta4 = request.form['pregunta4']
        pregunta5 = request.form['pregunta5']
        pregunta6 = request.form['respuestaAbierta']
        id_sesion = current_user.id
        
        socioeconomic = Socioeconomic(0, pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6, id_sesion)
        
        if ModelSocioeconomic.answers(db, socioeconomic):
            flash("Socioeconomic study done!")
            return redirect(url_for('ruta_cat'))
        else:
            flash("Error in making the socio-economic study")
            return render_template('index.html')
        
    return render_template('socioeconomic.html')
    
@app.route('/adoption-summary/<int:id_adoption>', methods=['GET'])
@login_required
def adoption_summary(id_adoption):
    try:
        # Obtener los datos de la adopción
        adoption = ModelAdoptions.get_adoption_by_id(db, id_adoption)
        if not adoption:
            flash("Adoption not found", "danger")
            return redirect(url_for('ruta_cat'))

        # Obtener datos adicionales (usuario que ofrece la adopción, etc.)
        owner = ModelUser.get_by_id(db, adoption.id_sesion)
        if not owner:
            flash("Owner not found", "danger")
            return redirect(url_for('ruta_cat'))

        # Obtener datos del usuario que está adoptando
        adopter = ModelUser.get_by_id(db, current_user.id)
        if not adopter:
            flash("Adopter not found", "danger")
            return redirect(url_for('ruta_cat'))

        # Obtener el estudio socioeconómico del adoptante
        socioeconomic = ModelSocioeconomic.get_by_id(db, current_user.id)
        if not socioeconomic:
            flash("Socioeconomic study done!", "danger")
            return redirect(url_for('ruta_study'))

        # Renderizar el template de resumen de adopción
        return render_template('adoption_summary.html', 
                               adoption=adoption,
                               owner=owner,
                               adopter=adopter,
                               socioeconomic=socioeconomic)
    except Exception as ex:
        flash(f"Error: {str(ex)}", "danger")
        return redirect(url_for('index'))

    
@app.route('/confirm-adoption/<int:id_adoption>', methods=['POST'])
@login_required
def confirm_adoption(id_adoption):
    try:
        # Obtener los datos de la adopción
        adoption = ModelAdoptions.get_adoption_by_id(db, id_adoption)
        if not adoption:
            flash("Adoption not found", "danger")
            return redirect(url_for('ruta_cat'))

        # Obtener datos del dueño (owner)
        owner = ModelUser.get_by_id(db, adoption.id_sesion)
        if not owner or not owner.mail:
            flash("Owner's email not available", "danger")
            return redirect(url_for('adoption_summary', id_adoption=id_adoption))

        # Obtener datos del adoptante (usuario actual)
        adopter = ModelUser.get_by_id(db, current_user.id)
        if not adopter:
            flash("Adopter not found", "danger")
            return redirect(url_for('adoption_summary', id_adoption=id_adoption))
        
        # Obtener el estudio socioeconómico del adoptante
        socioeconomic = ModelSocioeconomic.get_by_id(db, current_user.id)
        if not socioeconomic:
            flash("Socioeconomic study not found", "danger")
            return redirect(url_for('ruta_study'))
        
        # Construir el cuerpo del mensaje
        subject = "Adoption Request for Your Pet"
        body = f"""
        Hello {owner.username},

        Your pet "{adoption.name}" has been requested for adoption by {adopter.username}.
        
        Adopter's details:
        - Username: {adopter.username}
        - Email: {adopter.mail}
        - Phone: {adopter.phone}
        - Description: {adopter.description}

        Socioeconomic Details of the Adopter:
        - Monthly Budget: {socioeconomic.pregunta1}  
        - Available Space: {socioeconomic.pregunta2}
        - Walking Frequency: {socioeconomic.pregunta3}
        - Time Dedication: {socioeconomic.pregunta4}
        - Agreement: {socioeconomic.pregunta5}
        - Additional Comments: {socioeconomic.pregunta6}

        Please contact the adopter to coordinate the adoption process.

        Best regards,
        Perfect Pawls Team
        """

        # Enviar el correo al dueño
        if send_email(subject, [owner.mail], body):
            flash("The owner has been notified via email.", "success")
        else:
            flash("Failed to send the email. Please try again later.", "danger")

        # Redirigir al usuario a una página de confirmación o lista de adopciones
        return redirect(url_for('ruta_cat'))
    except Exception as ex:
        flash(f"Error: {str(ex)}", "danger")
        return redirect(url_for('ruta_cat'))

@app.route('/vets')
def ruta_vets():
    return render_template('Vets.html')

@app.route('/Tips&CaresDogs')
def ruta_tipsdogs():
    return render_template('Tips&CaresDogs.html')

@app.route('/conditions')
def ruta_conditions():
    return render_template('conditions.html')

@app.route('/Privacy')
def ruta_privacy():
    return render_template('Privacy.html')

@app.route('/Problem')
def ruta_problem():
    return render_template('Problem.html')

@app.route('/Tips&CaresCats')
def ruta_tipscats():
    return render_template('Tips&CaresCats.html')

@app.route('/forgotpass')
def ruta_reset():
    return render_template('forgotpass.html')

def status_401(error):
    return redirect(url_for('ruta_login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>",404

@app.route('/test')
def ruta_test():
    return render_template('test.html')

#activar el modo debug unicamente desarrollo/pruebas NO PRODUCCION 
if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404,status_404)
    app.run()




