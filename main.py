from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def generate_code_snippet(prompt):
    system_prompt = f"""
You are a professional game developer AI assistant.

Given this original code:

Instruction:
"{prompt}"

Your task:
- Provide only the minimal Python code snippet necessary to implement the instruction.
- Focus solely on the section of code that includes the change.
- Do NOT include any explanations, comments, or the full program code.

Format your answer exactly as:

```python
# minimal code snippet here
"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "codellama", "prompt": system_prompt, "stream": False}
        )
        response.raise_for_status()
        response_text = response.json().get("response", "")

        # Extract only the code snippet
        if "```python" in response_text:
            updated_code = response_text.split("```python")[1].split("```")[0].strip()
        else:
            updated_code = response_text

        return updated_code
    except requests.exceptions.RequestException as e:
        return f"Error generating code snippet: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/suggest", methods=["POST"])
def suggest():
    code = request.form.get("code", "").strip()
    prompt = request.form.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    updated_code = generate_code_snippet(prompt)
    return jsonify({"updated_code": updated_code})

if __name__ == "__main__":
    app.run(debug=True)
