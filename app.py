# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 09:12:44 2020

@author: chinm
"""
from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content = request.form['content']
        task_priority = request.form['priority']
        new_task = Todo(content=task_content,priority=task_priority)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task!"
    else:
        tasks = Todo.query.order_by(Todo.priority.desc()).all()
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a probelm deleting that task!"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method=='POST':
        task_to_update.content = request.form['content']
        task_to_update.priority = request.form['priority']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a probelm updating that task!"
    else:
        return render_template('update.html', task=task_to_update)

if __name__ == "__main__":
    app.run(debug=True)