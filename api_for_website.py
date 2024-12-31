from bson import ObjectId
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from groq import Groq
from database_module import save_user_data, get_user_data

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Required for session management
CORS(app)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def prepare_data(data):
    if isinstance(data, dict):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in data.items()}
    return data

@app.route('/login', methods=['POST'])
def login():
    pass  # Placeholder for the login functionality

@app.route('/submit_health_data', methods=['POST'])
def submit_health_data():
    data = request.get_json()  # Fetch data from the request
    serialized_data = prepare_data(data)
    save_user_data(serialized_data)
    session['user_data'] = serialized_data  # Store initial data in session
    return "Data saved successfully"  # Ensure this `return` is within the function

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    symptoms = request.json.get('symptoms')  # Get symptoms from the request JSON
    user_data = session.get('user_data', {})  # Retrieve user data from session
    user_data = prepare_data(user_data)  # Ensure user_data is serializable

    input_data = {
        'name': user_data.get('name'),
        'age': user_data.get('age'),
        'weight': user_data.get('weight'),
        'height': user_data.get('height'),
        'issues': user_data.get('issues'),
    }

    prompt = f"""
    Based on the following data: {input_data},and now suggest the  medecine that i have {symptoms} and accroding my data suggest me 3 medicine and 3 exersice    """

    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt
        }],
        model="llama3-8b-8192"
    )
    # Extract and format suggestions
    raw_suggestions = chat_completion.choices[0].message.content.strip()
    suggestions_lines = raw_suggestions.split('\n')
    formatted_suggestions = "\n".join(
        line for line in suggestions_lines if line.strip() and not line.strip().startswith(('Based on', 'Only provide'))
    )
    return jsonify({'suggestions': formatted_suggestions})  # Ensure this `return` is within the function


if __name__ == '__main__':
    app.run(debug=True)

