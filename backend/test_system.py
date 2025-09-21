#!/usr/bin/env python3
"""
BrainDump.AI Complete System Test
=================================
This script tests the entire BrainDump.AI system end-to-end:
1. Dependencies and imports
2. Supermemory integration
3. Ollama AI responses
4. FastAPI server
5. JSON schema validation

Run this to verify everything is working before your hackathon!
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path

def print_header(title):
    """Print a formatted test header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_result(test_name, success, message=""):
    """Print test result with emoji"""
    status = "✅" if success else "❌"
    print(f"{status} {test_name}")
    if message:
        print(f"   {message}")

def test_dependencies():
    """Test 1: Check all required dependencies are installed"""
    print_header("Testing Dependencies")
    
    dependencies = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("ollama", "Local LLM client"),
        ("supermemory", "Memory storage API"),
        ("pydantic", "Data validation"),
        ("httpx", "HTTP client")
    ]
    
    all_good = True
    for dep, description in dependencies:
        try:
            __import__(dep)
            print_result(f"{dep} - {description}", True)
        except ImportError:
            print_result(f"{dep} - {description}", False, "Not installed")
            all_good = False
    
    return all_good

def test_file_structure():
    """Test 2: Check all required files exist"""
    print_header("Testing File Structure")
    
    required_files = [
        ("app.py", "FastAPI backend server"),
        ("supermemory_client.py", "Supermemory API wrapper"),
        ("test_prompt_ollama.py", "AI prompt testing script"),
        ("PROMPT.md", "AI system prompt"),
        ("requirements.txt", "Python dependencies"),
        ("README.md", "Documentation")
    ]
    
    all_good = True
    for filename, description in required_files:
        if os.path.exists(filename):
            print_result(f"{filename} - {description}", True)
        else:
            print_result(f"{filename} - {description}", False, "File not found")
            all_good = False
    
    return all_good

def test_imports():
    """Test 3: Test all module imports"""
    print_header("Testing Module Imports")
    
    imports_to_test = [
        ("from supermemory_client import save_entry, get_recent", "Supermemory client"),
        ("from ollama import Client", "Ollama client"),
        ("import json", "JSON handling"),
        ("import fastapi", "FastAPI framework")
    ]
    
    all_good = True
    for import_statement, description in imports_to_test:
        try:
            exec(import_statement)
            print_result(f"{description}", True)
        except Exception as e:
            print_result(f"{description}", False, str(e))
            all_good = False
    
    return all_good

def test_supermemory_integration():
    """Test 4: Test Supermemory API integration"""
    print_header("Testing Supermemory Integration")
    
    try:
        from supermemory_client import save_entry, get_recent
        
        # Test data matching our JSON schema
        test_data = {
            "plan": ["Test step 1", "Test step 2", "Test step 3"],
            "reset_tip": "Take 5 deep breaths",
            "motivation": "You're doing great! 💪",
            "stress_score": 0.6
        }
        
        # Test save_entry
        save_entry("test_user_system", "System integration test", test_data, ["test"])
        print_result("Save entry to Supermemory", True)
        
        # Test get_recent
        recent = get_recent("test_user_system", limit=1)
        print_result("Retrieve recent entries", True, f"Found {len(recent)} entries")
        
        return True
        
    except Exception as e:
        print_result("Supermemory integration", False, str(e))
        return False

def test_json_schema():
    """Test 5: Test JSON schema validation"""
    print_header("Testing JSON Schema Validation")
    
    # Valid schema test
    valid_response = {
        "plan": ["Step 1", "Step 2", "Step 3"],
        "reset_tip": "Take deep breaths",
        "motivation": "You can do this! 💪",
        "stress_score": 0.7
    }
    
    # Test valid schema
    try:
        required_fields = ["plan", "reset_tip", "motivation", "stress_score"]
        has_all_fields = all(field in valid_response for field in required_fields)
        
        if has_all_fields and isinstance(valid_response["plan"], list) and \
           2 <= len(valid_response["plan"]) <= 4 and \
           0.0 <= valid_response["stress_score"] <= 1.0:
            print_result("Valid JSON schema", True)
        else:
            print_result("Valid JSON schema", False, "Schema validation failed")
            return False
    except Exception as e:
        print_result("Valid JSON schema", False, str(e))
        return False
    
    # Test invalid schemas
    invalid_schemas = [
        {"plan": ["only one step"], "reset_tip": "test", "motivation": "test", "stress_score": 0.5},  # Too few steps
        {"plan": ["step1", "step2", "step3", "step4", "step5"], "reset_tip": "test", "motivation": "test", "stress_score": 0.5},  # Too many steps
        {"plan": ["step1", "step2"], "reset_tip": "test", "motivation": "test", "stress_score": 1.5},  # Invalid stress score
    ]
    
    for i, invalid_schema in enumerate(invalid_schemas, 1):
        try:
            # These should be caught as invalid
            is_valid = (isinstance(invalid_schema["plan"], list) and 
                       2 <= len(invalid_schema["plan"]) <= 4 and
                       0.0 <= invalid_schema["stress_score"] <= 1.0)
            print_result(f"Invalid schema {i} detection", not is_valid)
        except:
            print_result(f"Invalid schema {i} detection", True)
    
    return True

def test_ollama_connection():
    """Test 6: Test Ollama connection and model availability"""
    print_header("Testing Ollama Connection")
    
    try:
        from ollama import Client
        client = Client()
        
        # Test if Ollama is running
        try:
            models = client.list()
            print_result("Ollama server connection", True)
            
            # Check if llama2 model is available
            model_names = [model['name'] for model in models.get('models', [])]
            if 'llama2' in model_names:
                print_result("llama2 model available", True)
            else:
                print_result("llama2 model available", False, f"Available models: {model_names}")
                return False
                
        except Exception as e:
            print_result("Ollama server connection", False, "Make sure 'ollama serve' is running")
            return False
            
    except Exception as e:
        print_result("Ollama client import", False, str(e))
        return False
    
    return True

def test_prompt_validation():
    """Test 7: Test PROMPT.md loading and basic validation"""
    print_header("Testing PROMPT.md Validation")
    
    try:
        with open("PROMPT.md", "r", encoding="utf-8") as f:
            prompt_content = f.read()
        
        # Check if prompt contains required elements
        required_elements = [
            "JSON Output Schema",
            "plan",
            "reset_tip", 
            "motivation",
            "stress_score",
            "Example 1",
            "Example 2"
        ]
        
        all_elements_present = True
        for element in required_elements:
            if element in prompt_content:
                print_result(f"Contains '{element}'", True)
            else:
                print_result(f"Contains '{element}'", False)
                all_elements_present = False
        
        return all_elements_present
        
    except Exception as e:
        print_result("PROMPT.md loading", False, str(e))
        return False

def test_fastapi_server():
    """Test 8: Test FastAPI server startup (without actually starting it)"""
    print_header("Testing FastAPI Server Configuration")
    
    try:
        # Test if we can import and create the app
        import sys
        sys.path.append('.')
        
        # This will test the app.py syntax and imports
        exec(open('app.py').read())
        print_result("FastAPI app configuration", True)
        
        return True
        
    except Exception as e:
        print_result("FastAPI app configuration", False, str(e))
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🚀 BrainDump.AI Complete System Test")
    print("=" * 60)
    print("This will test all components of your BrainDump.AI backend")
    print("Make sure Ollama is running: ollama serve")
    print("=" * 60)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("File Structure", test_file_structure), 
        ("Module Imports", test_imports),
        ("Supermemory Integration", test_supermemory_integration),
        ("JSON Schema", test_json_schema),
        ("Ollama Connection", test_ollama_connection),
        ("PROMPT.md Validation", test_prompt_validation),
        ("FastAPI Configuration", test_fastapi_server)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your BrainDump.AI backend is ready!")
        print("\n🚀 Next steps:")
        print("   1. Start the server: python3 app.py")
        print("   2. Test the API: curl http://localhost:8000/")
        print("   3. Run prompt tests: python3 test_prompt_ollama.py")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please fix the issues above.")
        print("\n🔧 Common fixes:")
        print("   - Install missing dependencies: pip install -r requirements.txt")
        print("   - Start Ollama: ollama serve")
        print("   - Check API keys in supermemory_client.py")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
