from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import uuid
import json
from datetime import datetime
import os
import pandas as pd
from werkzeug.utils import secure_filename
import secrets

app = Flask(__name__,
            template_folder='templates')

app.secret_key = secrets.token_hex(24)

DATA_FILE = 'tasks.json'
ALLOWED_EXTENSIONS = {'xlsx'}

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r',encoding='utf-8') as f:
            tasks = json.load(f)
            #Make sure we always return a list
            if isinstance(tasks, list):
                return tasks
            else:
                return []
    except (json.decoder.JSONDecodeError, Exception):
        return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w',encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#The . rsplit() method in Python is a string method that splits a string into a
#list of substrings from the right end of the string based on a specified delimiter
@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html',tasks=tasks)

@app.post('/create_task')
def create_task():
    new_task = {
        'id': str(uuid.uuid4()),
        'title': request.form.get('title','').strip(),
        'description': request.form.get('description','').strip(),
        'state': request.form.get('state','Pending'),
        'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.post('/edit/<task_id>')
def edit_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = request.form.get('title',task['title']).strip()
            task['description'] = request.form.get('description',task['description']).strip()
            task['state'] = request.form.get('state',task['state'])
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.post('/delete/<task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_excel():
    if request.method == 'POST':
        # Check if file part exists
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            try:
                # Read Excel → we don't need to save it to disk
                df = pd.read_excel(file, engine='openpyxl')

                # Normalize column names (case insensitive, strip spaces)
                df.columns = df.columns.str.strip().str.lower()

                # Required columns
                required = {'title', 'description', 'state'}
                if not required.issubset(df.columns):
                    missing = required - set(df.columns)
                    flash(f"Missing columns: {', '.join(missing)}", 'danger')
                    return redirect(url_for('index'))

                tasks = load_tasks()
                added_count = 0
                skipped = 0

                for _, row in df.iterrows():
                    title = str(row['title']).strip()
                    if not title:
                        skipped += 1
                        continue

                    description = str(row.get('description', '')).strip()
                    state = str(row['state']).strip()

                    if state not in ['Pending', 'Completed']:
                        state = 'Pending'  # fallback

                    new_task = {
                        'id': str(uuid.uuid4()),
                        'title': title,
                        'description': description,
                        'state': state,
                        'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    }

                    tasks.append(new_task)
                    added_count += 1

                save_tasks(tasks)

                msg = f"Added {added_count} tasks successfully."
                if skipped > 0:
                    msg += f" Skipped {skipped} rows (empty title)."
                flash(msg, 'success')

            except Exception as e:
                flash(f"Error reading Excel file: {str(e)}", 'danger')

            return redirect(url_for('index'))

        else:
            flash('Only .xlsx files allowed', 'danger')

    # GET → just show the page (or you can redirect to index)
    return redirect(url_for('index'))


@app.route('/export/json')
def export_json():
    tasks = load_tasks()
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'tasks-{today}.json'
    json_data = json.dumps(tasks, indent=2,ensure_ascii=False).encode('utf-8')
    #So when you see indent=2 in code (especially in export/download features), it just means:
    #"Please make the JSON look beautiful and readable for humans."
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


