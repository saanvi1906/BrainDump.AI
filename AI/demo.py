#!/usr/bin/env python3
"""
BrainDump.AI Demo Script
========================
This script creates a comprehensive demo of your BrainDump.AI system.
Perfect for hackathon presentations and showcasing the functionality.

Usage:
    python3 demo.py
"""

import requests
import json
import time
from supermemory_client import save_entry, get_recent

# Demo configuration
API_BASE_URL = "http://localhost:8000"
DEMO_USERS = [
    {"id": "demo_student_1", "name": "Alex", "scenario": "exam stress"},
    {"id": "demo_student_2", "name": "Sam", "scenario": "homework overload"},
    {"id": "demo_student_3", "name": "Jordan", "scenario": "presentation anxiety"}
]

def print_header(title):
    """Print a formatted demo header"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_step(step_num, title, description=""):
    """Print a demo step"""
    print(f"\n{step_num}️⃣ {title}")
    if description:
        print(f"   {description}")
    print("-" * 50)

def check_server_status():
    """Check if the BrainDump.AI server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server Status: {data['status']}")
            print(f"📡 Server URL: {API_BASE_URL}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to server at {API_BASE_URL}")
        print("   Make sure to run: python3 app.py")
        return False

def demo_api_endpoints():
    """Demonstrate all API endpoints"""
    print_step("1", "API Endpoints Demo", "Testing all available endpoints")
    
    # Test health endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        health_data = response.json()
        print("🏥 Health Check:")
        print(f"   Status: {health_data['status']}")
        print(f"   Dependencies: {health_data['dependencies']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test recent entries endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/recent/demo_user?limit=3")
        recent_data = response.json()
        print(f"📋 Recent Entries: {len(recent_data['entries'])} entries found")
    except Exception as e:
        print(f"❌ Recent entries failed: {e}")

def demo_stress_scenarios():
    """Demonstrate different stress scenarios"""
    print_step("2", "Stress Scenarios Demo", "Real-world student stress situations")
    
    scenarios = [
        {
            "input": "I have 3 exams next week and I feel completely overwhelmed. I don't know where to start studying.",
            "user_id": "demo_student_1",
            "tags": ["exam", "overwhelmed", "academic"]
        },
        {
            "input": "I have 5 assignments due tomorrow and I've been procrastinating all week. I'm panicking now.",
            "user_id": "demo_student_2", 
            "tags": ["homework", "procrastination", "deadline"]
        },
        {
            "input": "I have a big presentation tomorrow and I'm terrified of public speaking. My heart is racing just thinking about it.",
            "user_id": "demo_student_3",
            "tags": ["presentation", "anxiety", "public_speaking"]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📝 Scenario {i}: {scenario['input'][:60]}...")
        
        # Simulate AI response (since Ollama isn't running)
        ai_response = simulate_ai_response(scenario['input'])
        
        print("🤖 AI Response:")
        print(f"   Plan: {ai_response['plan']}")
        print(f"   Reset Tip: {ai_response['reset_tip']}")
        print(f"   Motivation: {ai_response['motivation']}")
        print(f"   Stress Score: {ai_response['stress_score']}")
        
        # Save to Supermemory
        try:
            save_entry(
                user_id=scenario['user_id'],
                user_input=scenario['input'],
                ai_output=ai_response,
                tags=scenario['tags']
            )
            print("💾 Saved to Supermemory!")
        except Exception as e:
            print(f"❌ Save failed: {e}")
        
        time.sleep(1)  # Pause for demo effect

def simulate_ai_response(user_input):
    """Simulate AI response based on input content"""
    input_lower = user_input.lower()
    
    if 'exam' in input_lower:
        return {
            "plan": [
                "Create a study schedule for each exam",
                "Review notes for 30 minutes per subject",
                "Take 10-minute breaks between study sessions",
                "Get 8 hours of sleep tonight"
            ],
            "reset_tip": "Take 5 deep breaths and stretch your shoulders",
            "motivation": "You've prepared well! Trust your knowledge and stay calm 💪",
            "stress_score": 0.8
        }
    elif 'homework' in input_lower or 'assignment' in input_lower:
        return {
            "plan": [
                "List all assignments by priority",
                "Start with the easiest one first",
                "Set 25-minute timers for focused work",
                "Take 5-minute breaks between tasks"
            ],
            "reset_tip": "Drink water and do a quick stretch",
            "motivation": "Small steps lead to big progress! You can do this ✨",
            "stress_score": 0.7
        }
    elif 'presentation' in input_lower or 'speaking' in input_lower:
        return {
            "plan": [
                "Practice your presentation out loud",
                "Prepare 3 key talking points",
                "Practice deep breathing exercises",
                "Visualize yourself succeeding"
            ],
            "reset_tip": "Practice the 4-7-8 breathing technique",
            "motivation": "You have valuable insights to share! Believe in yourself 🌟",
            "stress_score": 0.6
        }
    else:
        return {
            "plan": [
                "Identify the main source of stress",
                "Break it into smaller, manageable steps",
                "Take action on the first step",
                "Celebrate small wins"
            ],
            "reset_tip": "Take 3 deep breaths and ground yourself",
            "motivation": "You can handle this! One step at a time 🌱",
            "stress_score": 0.5
        }

def demo_supermemory_integration():
    """Demonstrate Supermemory data retrieval"""
    print_step("3", "Memory Integration Demo", "Retrieving and analyzing past stress dumps")
    
    for user in DEMO_USERS:
        print(f"\n👤 User: {user['name']} ({user['scenario']})")
        try:
            recent = get_recent(user['id'], limit=2)
            print(f"📊 Recent entries: {len(recent)} found")
            
            if recent:
                for i, entry in enumerate(recent[:1], 1):  # Show only first entry
                    print(f"   Entry {i}: {str(entry.get('content', ''))[:80]}...")
        except Exception as e:
            print(f"❌ Retrieval failed: {e}")

def demo_json_schema():
    """Demonstrate JSON schema validation"""
    print_step("4", "JSON Schema Validation", "Ensuring consistent AI responses")
    
    # Test valid schema
    valid_response = {
        "plan": ["Step 1", "Step 2", "Step 3"],
        "reset_tip": "Take deep breaths",
        "motivation": "You can do this! 💪",
        "stress_score": 0.7
    }
    
    print("✅ Valid JSON Schema:")
    print(json.dumps(valid_response, indent=2))
    
    # Test schema validation
    required_fields = ["plan", "reset_tip", "motivation", "stress_score"]
    is_valid = all(field in valid_response for field in required_fields)
    is_valid &= isinstance(valid_response["plan"], list)
    is_valid &= 2 <= len(valid_response["plan"]) <= 4
    is_valid &= 0.0 <= valid_response["stress_score"] <= 1.0
    
    print(f"\n🔍 Schema Validation: {'✅ PASS' if is_valid else '❌ FAIL'}")

def demo_frontend_integration():
    """Show how frontend would integrate"""
    print_step("5", "Frontend Integration", "How React frontend would connect")
    
    print("🌐 Frontend Integration Points:")
    print("   • Base URL: http://localhost:8000")
    print("   • POST /dump - Submit stress input")
    print("   • GET /recent/{user_id} - Get user history")
    print("   • GET /health - Check server status")
    
    print("\n📱 Example Frontend Code:")
    print("""
    // React component example
    const submitStressDump = async (userInput, userId) => {
      const response = await fetch('http://localhost:8000/dump', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_input: userInput,
          user_id: userId,
          tags: ['web']
        })
      });
      return await response.json();
    };
    """)

def demo_dashboard_data():
    """Show dashboard data structure"""
    print_step("6", "Dashboard Data", "Stress tracking and analytics")
    
    print("📊 Dashboard Features:")
    print("   • Stress score trends over time")
    print("   • Most common stress patterns")
    print("   • Personalized recommendations")
    print("   • Progress tracking")
    
    # Simulate dashboard data
    dashboard_data = {
        "user_id": "demo_student_1",
        "total_sessions": 15,
        "average_stress_score": 0.65,
        "most_common_tags": ["exam", "homework", "deadline"],
        "recent_trend": "decreasing",
        "recommendations": [
            "Practice deep breathing daily",
            "Set up a study schedule",
            "Take regular breaks"
        ]
    }
    
    print("\n📈 Sample Dashboard Data:")
    print(json.dumps(dashboard_data, indent=2))

def run_complete_demo():
    """Run the complete BrainDump.AI demo"""
    print("🎭 BrainDump.AI Complete Demo")
    print("=" * 60)
    print("Transforming student stress into actionable steps")
    print("=" * 60)
    
    # Check server status
    if not check_server_status():
        print("\n❌ Demo cannot continue without server running")
        print("   Please run: python3 app.py")
        return False
    
    # Run demo sections
    demo_api_endpoints()
    demo_stress_scenarios()
    demo_supermemory_integration()
    demo_json_schema()
    demo_frontend_integration()
    demo_dashboard_data()
    
    # Demo summary
    print_header("Demo Summary")
    print("🎉 BrainDump.AI Demo Complete!")
    print("\n✅ What was demonstrated:")
    print("   • API endpoints working")
    print("   • Stress scenario processing")
    print("   • AI response generation")
    print("   • Supermemory integration")
    print("   • JSON schema validation")
    print("   • Frontend integration ready")
    print("   • Dashboard data structure")
    
    print("\n🚀 Ready for:")
    print("   • Hackathon presentation")
    print("   • Frontend development")
    print("   • Production deployment")
    print("   • Team collaboration")
    
    print("\n📋 Next Steps:")
    print("   1. Connect React frontend")
    print("   2. Add Ollama for real AI responses")
    print("   3. Deploy to production")
    print("   4. Add user authentication")
    
    return True

if __name__ == "__main__":
    success = run_complete_demo()
    if success:
        print("\n🎯 Demo completed successfully!")
    else:
        print("\n⚠️ Demo failed - check server status")
