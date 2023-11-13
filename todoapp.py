from flask import Flask, redirect, request, render_template_string

app = Flask(__name__)

class Task:
    def __init__(self, description, email, priority):
        self.description = description
        self.email = email
        self.priority = priority

tasks = [
    Task("Buy Licence", "buy@email.com", "medium"),
    Task("Fix your computer", "you@youremail.com", "Low"),
    Task("Tell all employees to clean", "them@theiremail.com", "High")
]

index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ToDo List</title>
</head>
<body>

<table>
    <tr><th>Description</th><th>Email</th><th>Priority</th></tr>
    {% for task in tasks %}
        <tr><td>{{ task.description }}</td><td>{{ task.email }}</td><td>{{ task.priority }}</td></tr>
    {% endfor %}
</table>

<form action="/submit" method="post">
    <label for="task">Task:</label>
    <input type="text" id="task" name="task" required><br>

    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required><br>

    <label for="priority">Priority:</label>
    <select id="priority" name="priority">
        <option value="Low">Low</option>
        <option value="Medium">Medium</option>
        <option value="High">High</option>
    </select><br>

    <input type="submit" value="Add To Do Item">
</form>

<form action="/clear" method="post">
    <input type="submit" value="Clear">
</form>

{% if error == 'invalid_email' %}
    <p style='color: red;'>Invalid email address.</p>
{% elif error == 'invalid_priority' %}
    <p style='color: red;'>Invalid priority level.</p>
{% endif %}

</body>
</html>
"""

@app.route('/', methods=['GET'])
def tasks_manager():
    return render_template_string(index_html, tasks=tasks)

@app.route('/submit', methods=['POST'])
def submit():
    description = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    if not is_valid_email(email):
        return redirect('/?error=invalid_email')
    if priority not in ['Low', 'Medium', 'High']:
        return redirect('/?error=invalid_priority')

    task = Task(description, email, priority)
    tasks.append(task)

    return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    global tasks
    tasks = []
    return redirect('/')

def is_valid_email(email):
    import re
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email)

if __name__ == '__main__':
    app.run(debug=True)
