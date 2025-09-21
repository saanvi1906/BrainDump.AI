#!/usr/bin/env python3
"""
BrainDump.AI Interactive Demo
=============================
Live interactive demo for hackathon presentations.
Allows real-time stress input and shows AI responses.

Usage:
    python3 interactive_demo.py
"""

import requests
import json
import time
from supermemory_client import save_entry, get_recent

API_BASE_URL = "http://localhost:8000"

def print_banner():
    """Print demo banner"""
    print("🎭" + "="*58 + "🎭")
    print("🎯" + " "*20 + "BrainDump.AI" + " "*20 + "🎯")
    print("🎭" + " "*15 + "Interactive Demo" + " "*15 + "🎭")
    print("🎭" + "="*58 + "🎭")
    print("Transform student stress into actionable steps!")
    print("="*60)

def check_server():
    """Check if server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✅ BrainDump.AI server is running!")
            return True
        else:
            print(f"❌ Server error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("   Please run: python3 app.py")
        return False

def simulate_ai_response(user_input):
    """Simulate AI response based on input"""
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ['exam', 'test', 'final']):
        return {
            "plan": [
                "Create a study schedule for each subject",
                "Review key notes for 30 minutes",
                "Practice with sample questions",
                "Get 8 hours of sleep tonight"
            ],
            "reset_tip": "Take 5 deep breaths and stretch",
            "motivation": "You've prepared well! Trust your knowledge 💪",
            "stress_score": 0.8
        }
    elif any(word in input_lower for word in ['homework', 'assignment', 'project']):
        return {
            "plan": [
                "Break work into smaller tasks",
                "Set 25-minute focused work sessions",
                "Take 5-minute breaks between tasks",
                "Prioritize by deadline"
            ],
            "reset_tip": "Drink water and do a quick stretch",
            "motivation": "Small steps lead to big progress! ✨",
            "stress_score": 0.7
        }
    elif any(word in input_lower for word in ['presentation', 'speaking', 'interview']):
        return {
            "plan": [
                "Practice your presentation out loud",
                "Prepare 3 key talking points",
                "Practice deep breathing exercises",
                "Visualize yourself succeeding"
            ],
            "reset_tip": "Practice the 4-7-8 breathing technique",
            "motivation": "You have valuable insights to share! 🌟",
            "stress_score": 0.6
        }
    else:
        return {
            "plan": [
                "Identify the main source of stress",
                "Break it into smaller steps",
                "Take action on the first step",
                "Celebrate small wins"
            ],
            "reset_tip": "Take 3 deep breaths and ground yourself",
            "motivation": "You can handle this! One step at a time 🌱",
            "stress_score": 0.5
        }

def demo_stress_dump(user_input, user_id="demo_user"):
    """Process a stress dump and show the response"""
    print(f"\n📝 Processing: \"{user_input}\"")
    print("🤖 Generating AI response...")
    time.sleep(1)  # Simulate processing time
    
    # Get AI response
    ai_response = simulate_ai_response(user_input)
    
    print("\n🎯 AI Response:")
    print("="*40)
    print("📋 Action Plan:")
    for i, step in enumerate(ai_response['plan'], 1):
        print(f"   {i}. {step}")
    
    print(f"\n💆 Reset Tip: {ai_response['reset_tip']}")
    print(f"💡 Motivation: {ai_response['motivation']}")
    print(f"📊 Stress Score: {ai_response['stress_score']}/1.0")
    
    # Save to Supermemory
    try:
        save_entry(user_id, user_input, ai_response, ['demo'])
        print("\n💾 Saved to Supermemory!")
    except Exception as e:
        print(f"\n❌ Save failed: {e}")
    
    return ai_response

def show_demo_scenarios():
    """Show pre-defined demo scenarios"""
    scenarios = [
        "I have 3 exams next week and I feel completely overwhelmed",
        "I have 5 assignments due tomorrow and I've been procrastinating",
        "I have a big presentation tomorrow and I'm terrified of public speaking",
        "I'm stressed about my job interview next week",
        "I have too much homework and can't focus on anything"
    ]
    
    print("\n🎭 Demo Scenarios:")
    print("="*30)
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario}")
    
    return scenarios

def interactive_mode():
    """Run interactive demo mode"""
    print("\n🎮 Interactive Mode")
    print("="*30)
    print("Enter stress scenarios to see AI responses!")
    print("Type 'quit' to exit, 'scenarios' for examples")
    
    user_id = input("\n👤 Enter your user ID (or press Enter for 'demo_user'): ").strip()
    if not user_id:
        user_id = "demo_user"
    
    while True:
        print(f"\n📝 Enter your stress (user: {user_id}):")
        user_input = input("> ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Thanks for trying BrainDump.AI!")
            break
        elif user_input.lower() == 'scenarios':
            scenarios = show_demo_scenarios()
            try:
                choice = int(input("\nChoose a scenario (1-5): ")) - 1
                if 0 <= choice < len(scenarios):
                    demo_stress_dump(scenarios[choice], user_id)
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Please enter a number")
        elif user_input:
            demo_stress_dump(user_input, user_id)
        else:
            print("❌ Please enter some text")

def quick_demo():
    """Run a quick automated demo"""
    print("\n⚡ Quick Demo")
    print("="*20)
    
    demo_inputs = [
        "I have 3 exams next week and I feel completely overwhelmed",
        "I have too much homework and can't focus",
        "I'm anxious about my presentation tomorrow"
    ]
    
    for i, demo_input in enumerate(demo_inputs, 1):
        print(f"\n--- Demo {i} ---")
        demo_stress_dump(demo_input, f"demo_user_{i}")
        time.sleep(2)

def show_api_demo():
    """Show API endpoints demo"""
    print("\n🌐 API Endpoints Demo")
    print("="*30)
    
    try:
        # Health check
        response = requests.get(f"{API_BASE_URL}/health")
        health_data = response.json()
        print("🏥 Health Check:")
        print(f"   Status: {health_data['status']}")
        print(f"   Dependencies: {health_data['dependencies']}")
        
        # Recent entries
        response = requests.get(f"{API_BASE_URL}/recent/demo_user?limit=3")
        recent_data = response.json()
        print(f"\n📋 Recent Entries: {len(recent_data['entries'])} found")
        
    except Exception as e:
        print(f"❌ API demo failed: {e}")

def main():
    """Main demo function"""
    print_banner()
    
    # Check server
    if not check_server():
        return
    
    print("\n🎯 Choose Demo Mode:")
    print("1. Quick Demo (automated)")
    print("2. Interactive Demo (live input)")
    print("3. API Endpoints Demo")
    print("4. All Demos")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            quick_demo()
        elif choice == "2":
            interactive_mode()
        elif choice == "3":
            show_api_demo()
        elif choice == "4":
            quick_demo()
            show_api_demo()
            print("\n🎮 Starting Interactive Mode...")
            interactive_mode()
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying BrainDump.AI!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    main()
