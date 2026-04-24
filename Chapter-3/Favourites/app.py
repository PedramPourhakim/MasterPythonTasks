from flask import Flask,render_template,request,redirect,url_for,flash


app = Flask(__name__,
            template_folder='templates',
            static_folder='statics')

favourites = []
@app.route('/')
def index():
    return render_template('index.html',favourites=favourites)

@app.post('/create')
def create():
    if request.form.get('name') == '':
        flash('Please enter a name.','danger')
        return redirect(url_for('index'))

    favourites.append({"name":request.form.get("name"),
                       "age":request.form.get("age"),
                       "interest":request.form.get("interest"),
                       "amount":request.form.get("amount"),
                       "description":request.form.get("description")})
    return redirect(url_for('index'))


# if __name__ == "__main__":
#     app.run()

