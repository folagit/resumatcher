from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack

app = Flask(__name__)     
     
@app.route('/')
def handle_index():     
    return render_template('index.html')

if __name__ == '__main__':
    
    app.run( host='0.0.0.0',  debug=True)
