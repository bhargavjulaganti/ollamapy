import os
from flask import Flask, render_template, render_template_string, request
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = openai.OpenAI(
    api_key = os.environ.get("your_api_key"), 
    base_url= os.environ.get("LLM_ENNDPOINT")
)

@app.route('/', methods=['GET', 'POST'])
def index():
    poem = None
    if request.method == 'POST':
        try:
            prompt = request.form["input"]
            response = client.chat.completions.create(
                model="llava",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates poems."},
                    {"role": "user", "content": prompt}
                ]
            )
            poem = response.choices[0].message.content
        except Exception as e:
            poem = f"Error: {str(e)}"   
            poem = "Error generating poem."    
    return render_template('string_display.html', poem=poem)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host="0.0.0.0", port=port, debug=True)