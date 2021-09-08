from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column (db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'To Do' + str(self.id)

@app.route ('/', methods=['GET', 'POST'])
def post():

    if request.method == 'POST':
        to_do_title = request.form['title']
        new_to_do = ToDo(title=to_do_title)
        db.session.add(new_to_do)
        db.session.commit()
        return redirect ('/')
    else:
        all_to_dos = ToDo.query.order_by(ToDo.date_posted).all()
        return render_template('todo.html', todos=all_to_dos)
   
@app.route('/delete/<int:id>')
def delete(id):
    todo= ToDo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods= ['GET', 'POST'])
def edit(id):
    todo= ToDo.query.get_or_404(id)
    if request.method == 'POST':
        todo.title = request.form['title']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', todo=todo)

if __name__ == "__main__":
    app.run(debug=True)   