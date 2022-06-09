from flask import Flask
from flask import request
from flask import render_template
import json
import os

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        filename = 'users.txt'
        username = []
        users = {}
        score = 0

        with open(filename, 'r+') as file:
            names = file.read().splitlines()
            names = [name for name in names]
            usernameinput = request.form.get('username')
            for name_one in names:
                name_one = eval(name_one)
                username.append(name_one['username'])
            if usernameinput in username:
                for name_two in names:
                    name_two = eval(name_two)
                    if usernameinput == name_two['username']:
                        score = name_two['score']
            else:
                score = 0
                users['username'] = usernameinput
                users['score'] = str(score)
                users = json.dumps(users, ensure_ascii=False)
                users += f'\n'
                file.write(users)
        return score

    return render_template('login.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        filename = 'users.txt'
        username = []
        score = 0
        users = {}

        with open(filename, 'r+') as file:
            names = file.read().splitlines()
            names = [name for name in names]
            usernameinput = request.form.get('username')
            scoreinput = request.form.get('score')

            for name_one in names:
                name_one = eval(name_one)
                username.append(name_one['username'])
            if usernameinput in username:
                for name_two in names:
                    name_two = eval(name_two)
                    if usernameinput == name_two['username']:
                        # score = int(name_two['score']) + int(scoreinput)
                        score = int(scoreinput)
            else:
                score = int(scoreinput)
                users['username'] = usernameinput
                users['score'] = str(score)
                names.append(str(users))
        os.remove(filename)
        open(filename, 'w').close()
        for name_three in names:
            name_three = eval(name_three)
            if usernameinput == name_three['username']:
                name_three['score'] = str(score)
            name_three = json.dumps(name_three, ensure_ascii=False)
            name_three += f'\n'
            with open(filename, 'a+') as file:
                file.write(name_three)
        return str(score)
    return render_template('submit.html')
