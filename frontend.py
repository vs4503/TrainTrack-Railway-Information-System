from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)

messages = [{'start_station': 'Washington DC',
             'destination': 'New York'}]

result = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        start_station = request.form['start_station']
        destination = request.form['destination']
        if not start_station:
            flash('Start Station is required!')
        elif not destination:
            flash('Destination is required!')
        else:
            messages.append({'start_station': start_station, 'destination': destination})
            result.append(messages)
            return redirect(url_for('index'))
    return render_template('create.html')

def start():
    app.run(debug = False)

start()