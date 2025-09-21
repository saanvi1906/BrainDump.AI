"""
test_prompt_ollama.py
====================
Test script to validate PROMPT.md against Ollama before backend integration.

This script:
1. Loads the system prompt from PROMPT.md
2. Tests multiple stress input scenarios
3. Validates JSON responses match our schema
4. Auto-retries with re-prompt if validation fails
5. Saves results to CSV for analysis

Usage:
    python3 test_prompt_ollama.py

Dependencies:
    - ollama: pip install ollama
    - PROMPT.md: Must exist in same directory
"""

import json
import csv
from ollama import Client

# Initialize Ollama client
client = Client()

# Load system prompt from PROMPT.md
try:
    with open("PROMPT.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()
    print("✅ Loaded PROMPT.md successfully")
except FileNotFoundError:
    print("❌ PROMPT.md not found!")
    exit(1)

# Comprehensive test inputs covering different stress levels and scenarios
test_inputs = [
    # Low stress scenarios
    "I feel a bit behind in my reading, but it's not urgent.",
    "I have a small assignment due tomorrow that I haven't started.",
    
    # Moderate stress scenarios  
    "I'm anxious about my coding assignment and don't know where to start.",
    "I feel overwhelmed with homework and can't focus.",
    
    # High stress scenarios
    "I have three exams and two projects due next week. I'm panicking.",
    "I'm stressed about exams and also anxious about my social life.",
    
    # Edge cases
    "I don't know what to do.",  # Very short input
    "I'm having a really bad day and everything seems to be going wrong and I can't concentrate on anything and I feel like I'm failing at everything and I don't know how to fix it.",  # Very long input
]

# CSV file to save results
csv_file = "prompt_test_results.csv"

def validate_json(output):
    """
    Validate AI response matches our JSON schema exactly.
    
    Schema requirements:
    - plan: List of 2-4 strings, each ≤100 characters
    - reset_tip: String ≤80 characters  
    - motivation: String ≤150 characters
    - stress_score: Float between 0.0 and 1.0
    
    Args:
        output: Raw text response from Ollama
        
    Returns:
        (is_valid: bool, error_message: str)
    """
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    
    # Check required fields exist
    required_keys = ["plan", "reset_tip", "motivation", "stress_score"]
    missing_keys = [k for k in required_keys if k not in data]
    if missing_keys:
        return False, f"Missing required fields: {missing_keys}"
    
    # Validate each field according to schema
    try:
        # Plan validation: must be list of 2-4 strings, each ≤100 chars
        if not isinstance(data["plan"], list):
            return False, "Plan must be a list"
        if not (2 <= len(data["plan"]) <= 4):
            return False, f"Plan must have 2-4 steps, got {len(data['plan'])}"
        
        for i, step in enumerate(data["plan"]):
            if not isinstance(step, str):
                return False, f"Plan step {i+1} must be string"
            if len(step) > 100:
                return False, f"Plan step {i+1} too long ({len(step)} > 100 chars)"
        
        # Reset tip validation: string ≤80 chars
        if not isinstance(data["reset_tip"], str):
            return False, "Reset tip must be string"
        if len(data["reset_tip"]) > 80:
            return False, f"Reset tip too long ({len(data['reset_tip'])} > 80 chars)"
        
        # Motivation validation: string ≤150 chars
        if not isinstance(data["motivation"], str):
            return False, "Motivation must be string"
        if len(data["motivation"]) > 150:
            return False, f"Motivation too long ({len(data['motivation'])} > 150 chars)"
        
        # Stress score validation: float between 0.0 and 1.0
        if not isinstance(data["stress_score"], (int, float)):
            return False, "Stress score must be number"
        if not (0.0 <= data["stress_score"] <= 1.0):
            return False, f"Stress score must be 0.0-1.0, got {data['stress_score']}"
        
        return True, "Valid JSON schema"
        
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def run_tests():
    """Run all test inputs and save results to CSV"""
    print(f"\n🧪 Running {len(test_inputs)} test scenarios...")
    print("=" * 60)
    
    # Prepare CSV file
    with open(csv_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["input", "output", "validation", "re_prompted"])
        writer.writeheader()

        # Track statistics
        total_tests = len(test_inputs)
        successful_tests = 0
        re_prompt_count = 0

        # Run each test input
        for i, test_input in enumerate(test_inputs, 1):
            print(f"\n📝 Test {i}/{total_tests}: {test_input[:50]}...")
            re_prompted = False

            try:
                # First AI call with system prompt
                response = client.chat(
                    model="llama2",  # Configure model as needed
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": test_input}
                    ]
                )
                output_text = response['message']['content']

                # Validate JSON response
                is_valid, msg = validate_json(output_text)

                # Auto re-prompt if validation failed
                if not is_valid:
                    re_prompted = True
                    re_prompt_count += 1
                    print(f"   ⚠️  Validation failed: {msg}")
                    print("   🔄 Re-prompting...")
                    
                    re_prompt_text = "Return JSON strictly as per schema: plan, reset_tip, motivation, stress_score."
                    response = client.chat(
                        model="llama2",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": test_input + "\n" + re_prompt_text}
                        ]
                    )
                    output_text = response['message']['content']
                    is_valid, msg = validate_json(output_text)

                # Record results
                if is_valid:
                    successful_tests += 1
                    print(f"   ✅ Success: {msg}")
                else:
                    print(f"   ❌ Failed: {msg}")

                # Write to CSV
                writer.writerow({
                    "input": test_input,
                    "output": output_text,
                    "validation": msg,
                    "re_prompted": re_prompted
                })

            except Exception as e:
                print(f"   💥 Error: {str(e)}")
                writer.writerow({
                    "input": test_input,
                    "output": f"ERROR: {str(e)}",
                    "validation": "Exception occurred",
                    "re_prompted": False
                })

    # Print summary statistics
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success rate: {(successful_tests/total_tests)*100:.1f}%")
    print(f"Re-prompts needed: {re_prompt_count}")
    print(f"Results saved to: {csv_file}")

if __name__ == "__main__":
    run_tests()
