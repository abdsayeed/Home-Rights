#!/usr/bin/env python3
"""Test Ollama integration"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_ollama_connection():
    """Test basic Ollama connection"""
    print("🔍 Testing Ollama connection...")
    try:
        from services.ollama_service import OllamaService
        
        # Test simple query
        response = OllamaService.generate_response(
            "Hello, can you help me?",
            ""
        )
        
        if response and len(response) > 0:
            print("✅ Ollama connection successful!")
            print(f"📝 Response preview: {response[:100]}...")
            return True
        else:
            print("❌ Ollama returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure Ollama is running: ollama serve")
        print("  2. Check if llama3 is installed: ollama list")
        print("  3. Pull the model if needed: ollama pull llama3")
        return False

def test_housing_query():
    """Test housing law query"""
    print("\n🏠 Testing housing law query...")
    try:
        from services.ollama_service import OllamaService
        
        response = OllamaService.generate_response(
            "Can my landlord evict me without giving a reason?",
            ""
        )
        
        if response and len(response) > 50:
            print("✅ Housing query successful!")
            print(f"📝 Response:\n{response}\n")
            return True
        else:
            print("❌ Response too short or empty")
            return False
            
    except Exception as e:
        print(f"❌ Housing query failed: {e}")
        return False

def test_document_analysis():
    """Test document analysis"""
    print("\n📄 Testing document analysis...")
    try:
        from services.ollama_service import OllamaService
        
        sample_clause = """
        The Tenant shall be responsible for all repairs to the Property, 
        including structural repairs, roof repairs, and repairs to the 
        heating system. The Tenant must pay for all repairs within 7 days 
        of notification.
        """
        
        response = OllamaService.generate_document_analysis(
            sample_clause,
            [
                {
                    'issue': 'unfair_repair_responsibility',
                    'explanation': 'Tenant should not be responsible for structural repairs'
                }
            ]
        )
        
        if response and len(response) > 50:
            print("✅ Document analysis successful!")
            print(f"📝 Analysis:\n{response}\n")
            return True
        else:
            print("❌ Analysis too short or empty")
            return False
            
    except Exception as e:
        print(f"❌ Document analysis failed: {e}")
        return False

def test_conversation_context():
    """Test conversation with context"""
    print("\n💬 Testing conversation with context...")
    try:
        from services.ollama_service import OllamaService
        
        # Simulate conversation history
        history = [
            {'role': 'user', 'content': 'What is a Section 21 notice?'},
            {'role': 'assistant', 'content': 'A Section 21 notice was a no-fault eviction notice, but it has been abolished under the Renters Rights Act 2025.'}
        ]
        
        context = OllamaService.build_conversation_context(history)
        
        response = OllamaService.generate_response(
            "So I can ignore it if I receive one?",
            context
        )
        
        if response and len(response) > 30:
            print("✅ Conversation context working!")
            print(f"📝 Response:\n{response}\n")
            return True
        else:
            print("❌ Response too short or empty")
            return False
            
    except Exception as e:
        print(f"❌ Conversation context test failed: {e}")
        return False

def test_chat_service_integration():
    """Test full chat service integration"""
    print("\n🔗 Testing full chat service integration...")
    try:
        from services.chat_service import ChatService
        
        # Test simple query
        result = ChatService.generate_response(
            "Is a non-refundable deposit legal in the UK?"
        )
        
        if result and result.get('response') and len(result['response']) > 50:
            print("✅ Chat service integration successful!")
            print(f"📝 Intent: {result.get('intent')}")
            print(f"📝 Response preview: {result['response'][:150]}...")
            return True
        else:
            print("❌ Chat service returned invalid response")
            return False
            
    except Exception as e:
        print(f"❌ Chat service integration failed: {e}")
        print(f"   Error details: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 HomeRights AI - Ollama Integration Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Housing Query", test_housing_query),
        ("Document Analysis", test_document_analysis),
        ("Conversation Context", test_conversation_context),
        ("Chat Service Integration", test_chat_service_integration)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ollama integration is working correctly.")
        print("\nYou can now start the application:")
        print("  Backend: cd backend && source venv/bin/activate && python wsgi.py")
        print("  Frontend: cd frontend && npm start")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("  1. Start Ollama: ollama serve")
        print("  2. Pull model: ollama pull llama3")
        print("  3. Check dependencies: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
