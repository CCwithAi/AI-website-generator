from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from main import make_changes_and_push
from statistics import mean
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

processing_times = []

def calculate_average_time():
    if not processing_times:
        return 115
    return mean(processing_times)

@app.route('/generate', methods=['POST'])
def generate():
    start_time = time.time()
    input_text = request.form['input_text']
    try:
        make_changes_and_push(input_text, style='Bootstrap')
        processing_time = time.time() - start_time
        processing_times.append(processing_time)
        return jsonify({
            "status": "success", 
            "message": "HTML content generated and pushed to GitHub successfully!<br>The content has been deployed on Vercel. <br><br>GitHub Repository: <a href='https://github.com/CCwithAi/AI-website-generator' target='_blank'>https://github.com/CCwithAi/AI-website-generator</a> <br>Vercel URL: <a href='https://ai-website-generator-ccwithai.vercel.app/' target='_blank'>https://ai-website-generator-ccwithai.vercel.app/</a>"
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"})

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form["input_text"]
        try:
            make_changes_and_push(input_text, style='Bootstrap')
            return redirect(url_for("success"))
        except Exception as e:
            print(f"Error: {str(e)}")
            return f"An error occurred: {str(e)}"
    avg_time = calculate_average_time()
    return render_template("index.html", avg_time=avg_time)

@app.route("/success")
def success():
    return "HTML content generated and pushed to GitHub successfully!<br>The content has been deployed on Vercel. <br><br>GitHub Repository: <a href='https://github.com/CCwithAi/AI-website-generator' target='_blank'>https://github.com/CCwithAi/AI-website-generator</a> <br>Vercel URL: <a href='https://ai-website-generator-ccwithai.vercel.app/' target='_blank'>https://ai-website-generator-ccwithai.vercel.app/</a>"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
