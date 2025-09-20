import json
import csv
from ollama import Client  # Correct import

# Initialize Ollama client
client = Client()

# Load system prompt
with open("PROMPT.md", "r") as f:
    system_prompt = f.read()

# List of test inputs
test_inputs = [
    "I feel overwhelmed with homework.",
    "I have three exams and two projects due next week. I'm panicking.",
    "I'm stressed about exams and also anxious about my social life."
]

# CSV file to save results
csv_file = "prompt_test_results.csv"

# Function to validate JSON output
def validate_json(output):
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return False, "Invalid JSON"
    
    required_keys = ["plan", "reset_tip", "motivation", "stress_score"]
    missing_keys = [k for k in required_keys if k not in data]
    if missing_keys:
        return False, f"Missing keys: {missing_keys}"
    
    # Check types and length limits
    if not isinstance(data["plan"], list) or not (2 <= len(data["plan"]) <= 4):
        return False, "Plan format invalid"
    if not all(isinstance(step, str) and len(step) <= 100 for step in data["plan"]):
        return False, "Plan step too long"
    if not isinstance(data["reset_tip"], str) or len(data["reset_tip"]) > 80:
        return False, "Reset tip too long"
    if not isinstance(data["motivation"], str) or len(data["motivation"]) > 150:
        return False, "Motivation too long"
    if not isinstance(data["stress_score"], float) or not (0.0 <= data["stress_score"] <= 1.0):
        return False, "Stress score invalid"
    
    return True, "Valid JSON"

# Prepare CSV
with open(csv_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["input", "output", "validation", "re_prompted"])
    writer.writeheader()

    # Run test inputs
    for test_input in test_inputs:
        re_prompted = False

        # First AI call
        response = client.chat(
            model="llama2",  # Updated to use llama2 model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": test_input}
            ]
        )
        output_text = response['message']['content']

        # Validate JSON
        is_valid, msg = validate_json(output_text)

        # Auto re-prompt if invalid
        if not is_valid:
            re_prompted = True
            re_prompt_text = "Return JSON strictly as per schema: plan, reset_tip, motivation, stress_score."
            response = client.chat(
                model="llama2",  # Updated to use llama2 model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": test_input + "\n" + re_prompt_text}
                ]
            )
            output_text = response['message']['content']
            is_valid, msg = validate_json(output_text)

        # Write to CSV
        writer.writerow({
            "input": test_input,
            "output": output_text,
            "validation": msg,
            "re_prompted": re_prompted
        })

        print(f"\nInput: {test_input}")
        print(f"Output: {output_text}")
        print(f"Validation: {msg}")
        if re_prompted:
            print("Re-prompt was applied.")
