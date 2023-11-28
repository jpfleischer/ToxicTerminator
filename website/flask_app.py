from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        forward_message = "your mom..."
        message_content = request.form.get('message-contents')
        print(message_content)
        print('we got it :)')
        return render_template('solution.html', forward_message=forward_message);
    else:
        return render_template('solution.html')


