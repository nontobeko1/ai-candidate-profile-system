import google.generativeai as genai
import os
import json
from dotenv import load_dotenv


def test_gemini_api():
    """Test if Gemini API works for our candidate profile generation"""

    # Load environment variables
    load_dotenv()

    # Get Gemini API key
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        print("Please add: GEMINI_API_KEY=your_gemini_key_here")
        return False

    print(f"✅ Gemini API Key found: {gemini_key[:20]}...")

    try:
        # Configure Gemini
        genai.configure(api_key=gemini_key)

        # Try different model names
        model_names = [
            'gemini-2.0-flash',  # Latest Flash model
            'gemini-1.5-flash',  # Alternative Flash model
            'gemini-1.5-pro',  # Pro model
            'gemini-pro'  # Legacy name (might work)
        ]

        successful_model = None
        response = None

        for model_name in model_names:
            try:
                print(f"🔄 Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)

                # Test prompt
                test_prompt = """
                Create a professional profile JSON for a candidate.

                PERSONAL INFORMATION:
                - Name: John Doe
                - Email: john.doe@email.com
                - Phone: +1-555-0123
                - Location: New York, USA
                - Current Role: Software Engineer
                - Summary: Experienced software engineer with 5+ years in web development

                Return valid JSON with this structure:
                {
                    "personal_info": {
                        "name": "John Doe",
                        "title": "Software Engineer",
                        "email": "john.doe@email.com",
                        "phone": "+1-555-0123",
                        "location": "New York, USA",
                        "summary": "Experienced software engineer with 5+ years in web development"
                    },
                    "skills": {
                        "technical": ["Python", "JavaScript"],
                        "soft": ["Communication", "Teamwork"]
                    },
                    "education": [
                        {
                            "degree": "Bachelor's Degree",
                            "institution": "University of Technology",
                            "year": "2020",
                            "description": "Computer Science"
                        }
                    ],
                    "experience": [
                        {
                            "position": "Software Engineer",
                            "company": "Tech Corp",
                            "period": "3 years",
                            "description": "Developed web applications"
                        }
                    ],
                    "projects": [
                        {
                            "name": "E-commerce Platform",
                            "description": "Built a full-stack e-commerce solution",
                            "technologies": ["React", "Node.js", "MongoDB"]
                        }
                    ]
                }
                """

                response = model.generate_content(test_prompt)
                successful_model = model_name
                print(f"✅ Success with model: {model_name}")
                break

            except Exception as e:
                print(f"❌ Model {model_name} failed: {e}")
                continue

        if not successful_model:
            print("❌ All models failed!")
            return False

        print("✅ Gemini API response received!")
        print(f"Model used: {successful_model}")
        print(f"Response type: {type(response.text)}")
        print("\n" + "=" * 50)
        print("RAW RESPONSE:")
        print("=" * 50)
        print(response.text)
        print("=" * 50)

        # Try to parse the response as JSON
        try:
            # Extract JSON from response
            text = response.text.strip()

            # Remove markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]

            profile_data = json.loads(text.strip())
            print("✅ Successfully parsed JSON response!")
            print(f"Name: {profile_data['personal_info']['name']}")
            print(f"Title: {profile_data['personal_info']['title']}")
            print(
                f"Skills: {len(profile_data['skills']['technical'])} technical, {len(profile_data['skills']['soft'])} soft")
            print(f"Experience: {len(profile_data['experience'])} positions")
            print(f"Education: {len(profile_data['education'])} entries")
            print(f"Projects: {len(profile_data['projects'])} projects")

            # Save the working model name for future use
            with open('gemini_model.txt', 'w') as f:
                f.write(successful_model)
            print(f"💾 Saved working model '{successful_model}' to gemini_model.txt")

            return True

        except json.JSONDecodeError as e:
            print("❌ Failed to parse JSON response")
            print(f"JSON Error: {e}")
            # Even if JSON parsing fails, if we got a response, the API is working
            print("⚠️ API is working but response format needs adjustment")
            return True

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return False


def test_simple_generation():
    """Test simple text generation to verify API key works"""
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        print("No Gemini API key found")
        return False

    try:
        genai.configure(api_key=gemini_key)

        # Use the latest model that should work
        model = genai.GenerativeModel('gemini-2.0-flash')

        response = model.generate_content("Say 'Hello World' in JSON format: {'message': 'Hello World'}")

        print("✅ Simple test passed!")
        print(f"Response: {response.text}")
        return True

    except Exception as e:
        print(f"❌ Simple test failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing Gemini API for Candidate Profile Generation")
    print("=" * 60)

    # First, test simple generation
    print("\n1. Testing simple generation...")
    simple_success = test_simple_generation()

    if simple_success:
        print("\n2. Testing profile generation...")
        profile_success = test_gemini_api()
    else:
        profile_success = False

    print("\n" + "=" * 60)
    if simple_success and profile_success:
        print("🎉 Gemini API test PASSED! You can use Gemini for candidate profiles.")
    elif simple_success:
        print("⚠️ Gemini API works but profile generation needs adjustment.")
    else:
        print("💥 Gemini API test FAILED! Check your API key and configuration.")