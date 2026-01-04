"""Test registration endpoint"""
import requests
import json

API_URL = "http://localhost:8000"

def test_register():
    """Test registration endpoint"""
    url = f"{API_URL}/api/auth/register"
    
    test_data = {
        "email": "test@example.com",
        "password": "TestPassword123"
    }
    
    print(f"Testing registration endpoint: {url}")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        try:
            response_json = response.json()
            print(f"Response JSON: {json.dumps(response_json, indent=2)}")
        except:
            print("Response is not valid JSON")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to backend at {API_URL}")
        print("Make sure the backend server is running:")
        print("  cd backend && python -m uvicorn app.main:app --reload --port 8000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_register()

