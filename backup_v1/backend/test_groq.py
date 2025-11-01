"""
Test script to verify Groq API is working
==========================================
This script tests if Groq API is properly configured and responding.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

def test_groq_import():
    """Test if Groq package is installed"""
    try:
        from groq import Groq
        print("[OK] Groq package imported successfully")
        return True, Groq
    except ImportError as e:
        print(f"[FAIL] Groq package not installed: {e}")
        print("   Install with: pip install groq")
        return False, None

def test_api_key():
    """Test if API key is configured"""
    api_key = os.environ.get('GROQ_API_KEY')
    if api_key:
        # Mask the key for display (show first 10 chars)
        masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
        print(f"[OK] GROQ_API_KEY found: {masked_key}")
        return True, api_key
    else:
        print("[FAIL] GROQ_API_KEY not found in environment variables")
        print("   Add it to .env file: GROQ_API_KEY=your_key_here")
        return False, None

def test_groq_client(api_key, Groq):
    """Test if Groq client can be initialized"""
    try:
        client = Groq(api_key=api_key)
        print("[OK] Groq client initialized successfully")
        return True, client
    except Exception as e:
        print(f"[FAIL] Failed to initialize Groq client: {e}")
        return False, None

def test_groq_api_call(client):
    """Test if Groq API responds correctly"""
    try:
        print("\n[TEST] Testing Groq API call...")
        print("   This may take a few seconds...")
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for legal documents."
                },
                {
                    "role": "user",
                    "content": "Generate a friendly question to ask for a company name field. Keep it concise (one sentence)."
                }
            ],
            temperature=0.3,
            max_tokens=100,
            top_p=0.9
        )
        
        answer = response.choices[0].message.content
        print(f"[OK] Groq API responded successfully!")
        print(f"\n[AI Response]:")
        print(f"   '{answer}'")
        print(f"\n[OK] Model used: llama-3.3-70b-versatile")
        print(f"[OK] Response length: {len(answer)} characters")
        return True
        
    except Exception as e:
        print(f"[FAIL] Groq API call failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        if "401" in str(e) or "unauthorized" in str(e).lower():
            print("   → Check if your API key is correct")
        elif "429" in str(e) or "rate limit" in str(e).lower():
            print("   → Rate limit exceeded, try again later")
        elif "model" in str(e).lower():
            print("   → Model name might be incorrect")
        return False

def test_question_generation(client):
    """Test question generation for different field types"""
    print("\n[TEST] Testing question generation for different field types...")
    
    test_cases = [
        ("Company Name", "company"),
        ("Purchase Amount", "amount"),
        ("Date of Incorporation", "date"),
        ("Valuation Cap", "amount"),
    ]
    
    results = []
    for field_name, field_type in test_cases:
        try:
            prompt = f"""Generate a friendly, professional question to ask for filling the field "{field_name}" which is of type "{field_type}".

Guidelines:
- Be concise (one sentence)
- Be friendly and professional
- Provide format examples if needed
- Don't be overly verbose

Return ONLY the question, no prefixes or extra text."""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful legal document assistant. Generate conversational questions for document fields."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100,
                top_p=0.9
            )
            
            answer = response.choices[0].message.content.strip()
            results.append((field_name, True, answer))
            print(f"   [OK] {field_name}: '{answer}'")
            
        except Exception as e:
            results.append((field_name, False, str(e)))
            print(f"   [FAIL] {field_name}: {e}")
    
    return results

def main():
    """Run all tests"""
    print("=" * 60)
    print("Groq API Test Script")
    print("=" * 60)
    print()
    
    # Test 1: Import
    import_success, Groq = test_groq_import()
    if not import_success:
        print("\n[FAIL] Cannot proceed without Groq package")
        return False
    
    # Test 2: API Key
    key_success, api_key = test_api_key()
    if not key_success:
        print("\n[FAIL] Cannot proceed without API key")
        print("\n[INFO] To fix:")
        print("   1. Get API key from https://console.groq.com")
        print("   2. Add to backend/.env file: GROQ_API_KEY=your_key_here")
        return False
    
    # Test 3: Client initialization
    client_success, client = test_groq_client(api_key, Groq)
    if not client_success:
        print("\n[FAIL] Cannot proceed without valid client")
        return False
    
    # Test 4: API call
    api_success = test_groq_api_call(client)
    if not api_success:
        print("\n[FAIL] Groq API is not responding correctly")
        return False
    
    # Test 5: Question generation
    print("\n" + "=" * 60)
    question_results = test_question_generation(client)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"[OK] Package Import: {'PASS' if import_success else 'FAIL'}")
    print(f"[OK] API Key Config: {'PASS' if key_success else 'FAIL'}")
    print(f"[OK] Client Init: {'PASS' if client_success else 'FAIL'}")
    print(f"[OK] API Call: {'PASS' if api_success else 'FAIL'}")
    
    successful_questions = sum(1 for _, success, _ in question_results if success)
    print(f"[OK] Question Generation: {successful_questions}/{len(question_results)} PASS")
    
    if all([import_success, key_success, client_success, api_success]):
        print("\n[SUCCESS] All critical tests passed! Groq API is working correctly.")
        print("\n[INFO] Your AI service should be using Groq for:")
        print("   - Generating contextual questions")
        print("   - Enhanced error messages")
        print("   - Field analysis")
        return True
    else:
        print("\n[WARNING] Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

