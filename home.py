from flask import Flask,render_template
file = ''
app = Flask(__name__,template_folder=file)

@app.route('/')
def index():
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True,port=5000)