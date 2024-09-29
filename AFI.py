from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    hospital_no = db.Column(db.String(50), nullable=False)
    date_of_admission = db.Column(db.String(20), nullable=False)
    # Add other fields as required


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        hospital_no = request.form.get('hospital_no')
        date_of_admission = request.form.get('date_of_admission')
        # Retrieve other form fields here

        new_patient = Patient(name=name, age=age, gender=gender, hospital_no=hospital_no,
                              date_of_admission=date_of_admission)
        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_patient.html')


if __name__ == '__main__':
    app.run(debug=True)
