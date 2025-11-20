from flask import Flask, render_template
from blueprints.exp1 import exp1_bp
from blueprints.exp2 import exp2_bp
from blueprints.exp3 import exp3_bp
from blueprints.exp4 import exp4_bp
from blueprints.exp5 import exp5_bp
from blueprints.exp6 import exp6_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Register Blueprints
app.register_blueprint(exp1_bp, url_prefix='/exp1')
app.register_blueprint(exp2_bp, url_prefix='/exp2')
app.register_blueprint(exp3_bp, url_prefix='/exp3')
app.register_blueprint(exp4_bp, url_prefix='/exp4')
app.register_blueprint(exp5_bp, url_prefix='/exp5')
app.register_blueprint(exp6_bp, url_prefix='/exp6')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
