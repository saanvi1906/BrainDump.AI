#!/usr/bin/env python3
"""
BrainDump.AI Quick Test (No Ollama Required)
============================================
This script tests the core components that don't require Ollama to be running.
Use this to verify your setup before installing Ollama.
"""

import sys
import os
import json

def print_header(title):
    """Print a formatted test header"""
    print(f"\n{'='*50}")
    print(f"🧪 {title}")
    print(f"{'='*50}")

def print_result(test_name, success, message=""):
    """Print test result with emoji"""
    status = "✅" if success else "❌"
    print(f"{status} {test_name}")
    if message:
        print(f"   {message}")

def test_core_dependencies():
    """Test core dependencies (excluding Ollama)"""
    print_header("Testing Core Dependencies")
    
    dependencies = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
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
    """Test all required files exist"""
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
    """Test all module imports"""
    print_header("Testing Module Imports")
    
    imports_to_test = [
        ("from supermemory_client import save_entry, get_recent", "Supermemory client"),
        ("import json", "JSON handling"),
        ("import fastapi", "FastAPI framework"),
        ("from pydantic import BaseModel", "Pydantic models")
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
    """Test Supermemory API integration"""
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
        save_entry("quick_test_user", "Quick system test", test_data, ["test"])
        print_result("Save entry to Supermemory", True)
        
        # Test get_recent
        recent = get_recent("quick_test_user", limit=1)
        print_result("Retrieve recent entries", True, f"Found {len(recent)} entries")
        
        return True
        
    except Exception as e:
        print_result("Supermemory integration", False, str(e))
        return False

def test_json_schema():
    """Test JSON schema validation"""
    print_header("Testing JSON Schema Validation")
    
    # Valid schema test
    valid_response = {
        "plan": ["Step 1", "Step 2", "Step 3"],
        "reset_tip": "Take deep breaths",
        "motivation": "You can do this! 💪",
        "stress_score": 0.7
    }
    
    try:
        required_fields = ["plan", "reset_tip", "motivation", "stress_score"]
        has_all_fields = all(field in valid_response for field in required_fields)
        
        if has_all_fields and isinstance(valid_response["plan"], list) and \
           2 <= len(valid_response["plan"]) <= 4 and \
           0.0 <= valid_response["stress_score"] <= 1.0:
            print_result("Valid JSON schema", True)
            return True
        else:
            print_result("Valid JSON schema", False, "Schema validation failed")
            return False
    except Exception as e:
        print_result("Valid JSON schema", False, str(e))
        return False

def test_prompt_file():
    """Test PROMPT.md content"""
    print_header("Testing PROMPT.md Content")
    
    try:
        with open("PROMPT.md", "r", encoding="utf-8") as f:
            prompt_content = f.read()
        
        required_elements = [
            "JSON Output Schema",
            "plan",
            "reset_tip", 
            "motivation",
            "stress_score"
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

def test_fastapi_config():
    """Test FastAPI configuration"""
    print_header("Testing FastAPI Configuration")
    
    try:
        # Test if we can import the app components
        from fastapi import FastAPI
        from pydantic import BaseModel
        
        # Test creating a simple app
        app = FastAPI()
        print_result("FastAPI app creation", True)
        
        # Test Pydantic model
        class TestModel(BaseModel):
            test_field: str
        
        model = TestModel(test_field="test")
        print_result("Pydantic model validation", True)
        
        return True
        
    except Exception as e:
        print_result("FastAPI configuration", False, str(e))
        return False

def run_quick_test():
    """Run quick tests that don't require Ollama"""
    print("🚀 BrainDump.AI Quick Test (No Ollama Required)")
    print("=" * 60)
    print("This tests core components without requiring Ollama to be running")
    print("=" * 60)
    
    tests = [
        ("Core Dependencies", test_core_dependencies),
        ("File Structure", test_file_structure), 
        ("Module Imports", test_imports),
        ("Supermemory Integration", test_supermemory_integration),
        ("JSON Schema", test_json_schema),
        ("PROMPT.md Content", test_prompt_file),
        ("FastAPI Configuration", test_fastapi_config)
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
        print("\n🎉 ALL CORE TESTS PASSED!")
        print("\n📋 Next steps to complete setup:")
        print("   1. Install Ollama: https://ollama.ai")
        print("   2. Start Ollama: ollama serve")
        print("   3. Pull model: ollama pull llama2")
        print("   4. Test AI: python3 test_prompt_ollama.py")
        print("   5. Start server: python3 app.py")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_quick_test()
    sys.exit(0 if success else 1)
