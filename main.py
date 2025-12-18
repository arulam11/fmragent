import os
from flask import Flask, request, jsonify
from fmr_agent.agent import root_agent
from datetime import date

app = Flask(__name__)

@app.route("/invoke_agent", methods=["POST"])
def invoke_agent():
    """
    Endpoint to receive a user question and return the agent's response,
    as JSON.
    """
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    question = data["question"]
    print(f"Received question: {question}")

    try:
        # Provide the current date as part of the initial session state for this specific run.
        # This ensures the new session created for the execution contains the necessary variable.
        current_date_str = date.today().strftime("%Y-%m-%d")
        result = root_agent.run(
            question, session_state={"current_date": current_date_str}
        )
        return jsonify({"response": result})
    except Exception as e:
        print(f"Error during agent execution: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))