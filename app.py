import webbrowser
from flask import Flask
app=Flask(__name__)
@app.route('/')
def hello():
    return "Hellooooo"

if __name__=='__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)
