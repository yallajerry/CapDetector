from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

# api key
client = genai.Client(api_key=os.getenv("API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_statement():
    try:
        data = request.json
        statement = data.get('statement', '')
        context = data.get('context', '')
        
        if not statement:
            return jsonify({'error': 'Statement is required'}), 400
        
        if context == "":
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=f"Is this statement true? '{statement}'. Its not about you, please don't use bold letters or italic letters as it will screw the text up, you are currently being used as a machine for a web app. Additionally, don't use true or false, use cap or not cap in a funny way. Try your best as the user didn't give any context."
            )
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=f"Is this statement true? '{statement}'. Its not about you, please don't use bold letters or italic letters as it will screw the text up, you are currently being used as a machine for a web app. Additionally, don't use true or false, use cap or not cap in a funny way. Use this context: {context}"
            )
        
        return jsonify({'result': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

