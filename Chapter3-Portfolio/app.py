from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

projects = [
    {
        "Name":"Task Management",
        "Description":"A sample task management app.",
        "GithubLink" : "https://github.com/PedramPourhakim/PythonCourse/tree/main/Final-Project"
    },
    {
        "Name":"Calculator",
        "Description":"A simple calculator app with kiwi.",
        "GithubLink":"https://github.com/PedramPourhakim/MasterPythonTasks/tree/master/Chapter-2-Calculator"
    },
    {
        "Name":"Countdown",
        "Description":"A simple countdown app.",
        "GithubLink":"https://github.com/PedramPourhakim/MasterPythonTasks/tree/master/Chapter2-CountDown"
    }
]
skills = ["Python","Django","Fast Api"]

Me = {
    "fullname": "Pedram Pourhakim",
    "description":"A motivated programmer junior python developer",
    "image": "tel.jpg"
}
def is_htmx_request():
    return request.headers.get('HX-Request') == 'true'

@app.get('/')
@app.get('/home')
def home():
    if is_htmx_request():
        return render_template('partials/home.html', person=Me)
    return render_template('index.html', person=Me)

@app.get('/skills')
def skills_page():
    if is_htmx_request():
        return render_template('partials/skills.html', skills=skills)
    return render_template('index.html', person=Me)

@app.get('/projects')
def projects_page():
    if is_htmx_request():
        return render_template('partials/projects.html', projects=projects)
    return render_template('index.html', person=Me)

if __name__ == '__main__':
    app.run(debug=True)



