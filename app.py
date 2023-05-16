from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
from db import db_init, db
from model import Carte, Autor
import os
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)
migrate = Migrate(app, db)


@app.route('/')
@app.route('/home')
def index():
    carti = Carte.query.order_by(Carte.date.desc()).all()
    return render_template("index.html", carti=carti)



@app.route('/about')
def about():
    return render_template("about.html")


UPLOAD_FOLDER = 'static/imagini_carte'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/carti')
def carti():
    carti = Carte.query.order_by(Carte.date.desc()).all()
    return render_template("carti/carte.html", carti=carti)


@app.route('/carti/<int:id>')
def carte(id):
    carti = Carte.query.get_or_404(id)
    return render_template("carti/detali.html", carti=carti)


@app.route('/carti/creare', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        titlu = request.form['titlu']
        descr_carte  = request.form['descriere']
        autor_id = request.form['autor_id']

        # Procesăm imaginea din formular
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(image_path)
                image_path = os.path.relpath(image_path, app.config['UPLOAD_FOLDER'])

        carti = Carte(titlu=titlu, descr_carte=descr_carte, image=image_path, autor_id=autor_id)

        try:
            db.session.add(carti)
            db.session.commit()
            return redirect('/carti')
        except:
            return "A apărut o eroare la adăugarea cărții."
    else:
        autori = Autor.query.all()
        return render_template("carti/creare.html", autori=autori)


@app.route('/carti/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    carte = Carte.query.get_or_404(id)
    if request.method == 'POST':
        carte.titlu = request.form['titlu']
        carte.autor_id = request.form['autor_id']
        carte.descr_carte = request.form['descr_carte']

        new_image = request.files.get('new_image')
        if new_image:
            # Verificăm dacă fișierul încărcat este o imagine
            if new_image.mimetype.startswith('image/'):
                # Generăm un nume unic pentru fișierul imaginii
                image_filename = f"carte_{id}_image.{new_image.filename.split('.')[-1]}"
                # Salvăm imaginea în directorul specificat
                new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                # Actualizăm calea imaginii în obiectul 'carte'
                carte.image = image_filename
            else:
                return "Eroare: Fișierul încărcat nu este o imagine."

        try:
            db.session.commit()
            return redirect('/carti')
        except:
            return "A apărut o eroare la actualizarea cărții."
    else:
        autori = Autor.query.all()
        return render_template("carti/update.html", carte=carte, autori=autori)


@app.route('/carti/<int:id>/delete', methods=['POST'])
def delete(id):
    carte = Carte.query.get_or_404(id)
    try:
        db.session.delete(carte)
        db.session.commit()
        return redirect('/carti')
    except:
        return "A aparut o eroare la stergerea cartii."


@app.route('/autori')
def autori():
    autori = Autor.query.order_by(Autor.nume, Autor.prenume).all()
    return render_template("autor/autori.html", autori=autori)


@app.route('/autor')
def autorii():
    autori = Autor.query.order_by(Autor.nume, Autor.prenume).all()
    return render_template("autor/autor.html", autori=autori)

@app.route('/autori/<int:id>')
def autor(id):
    autor = Autor.query.get_or_404(id)
    return render_template("autor/detalii.html", autor=autor)


@app.route('/autori/create', methods=['GET', 'POST'])
def create_autor():
    if request.method == 'POST':
        nume = request.form['nume']
        prenume = request.form['prenume']

        # Procesăm imaginea din formular
        image_autor_path = None
        if 'imagine' in request.files:
            file = request.files['imagine']
            if file.filename != '':
                filename = secure_filename(file.filename)
                image_autor_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(image_autor_path)
                image_autor_path = os.path.relpath(image_autor_path, app.config['UPLOAD_FOLDER'])

        autor = Autor(nume=nume, prenume=prenume, imagine=image_autor_path)

        try:
            db.session.add(autor)
            db.session.commit()
            return redirect('/autori')
        except:
            return "A apărut o eroare la adăugarea autorului."
    else:
        return render_template("autor/create_autori.html")


@app.route('/autori/<int:id>/update', methods=['GET', 'POST'])
def update_autor(id):
    autor = Autor.query.get_or_404(id)
    if request.method == 'POST':
        autor.nume = request.form['nume']
        autor.prenume = request.form['prenume']
        data_nasterii = request.form['zi_nastere'] + "/" + request.form['luna_nastere'] + "/" + request.form['an_nastere']
        autor.data_nasterii = data_nasterii
        autor.tara = request.form['tara']
        autor.descriere = request.form['descriere']

        new_imagine = request.files.get('new_imagine')
        if new_imagine:
            # Verificăm dacă fișierul încărcat este o imagine
            if new_imagine.mimetype.startswith('image/'):
                # Generăm un nume unic pentru fișierul imaginii
                imagine_filename = f"autor_{id}_imagine.{new_imagine.filename.split('.')[-1]}"
                # Salvăm imaginea în directorul specificat
                new_imagine.save(os.path.join(app.config['UPLOAD_FOLDER'], imagine_filename))
                # Verificăm dacă există deja o imagine asociată autorului și o ștergem
                if autor.imagine:
                    image_autor_path = os.path.join(app.config['UPLOAD_FOLDER'], autor.imagine)
                    if os.path.exists(image_autor_path):
                        os.remove(image_autor_path)
                # Actualizăm calea imaginii în obiectul 'autor'
                autor.imagine = imagine_filename
            else:
                return "Eroare: Fișierul încărcat nu este o imagine."

        try:
            db.session.commit()
            return redirect('/autori')
        except:
            return "A apărut o eroare la actualizarea autorului."
    else:
        return render_template("autor/update_autor.html", autor=autor)


@app.route('/autori/<int:id>/delete', methods=['POST'])
def delete_autor(id):
    autor = Autor.query.get_or_404(id)
    try:
        db.session.delete(autor)
        db.session.commit()
        return redirect('/autori')
    except:
        return "A aparut o eroare la stergerea autorului."


if __name__ == "__main__":
    app.run(debug=True)


