from document_processor import DocumentProcessor
import os


def test_document_processor():
    """Test the document processor with all sample files"""
    processor = DocumentProcessor()

    test_files = [
        "sample_resume.pdf",
        "sample_resume.docx",
        "sample_transcript.pdf",
        "sample_transcript.docx"
    ]

    print("🧪 Testing Document Processor with Sample Files")
    print("=" * 60)

    for file in test_files:
        if os.path.exists(file):
            print(f"\n📋 Processing: {file}")
            print("-" * 40)

            result = processor.analyze_document(file)

            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue

            print(f"✅ Text extracted: {result['raw_text_length']} characters")
            print(f"📊 Word count: {result['word_count']}")
            print(f"📄 Estimated pages: {result['estimated_pages']}")

            # Skills
            skills = result['skills']
            print(f"🔧 Technical skills found: {len(skills['technical'])}")
            if skills['technical']:
                print(f"   {', '.join(skills['technical'][:8])}")

            print(f"💬 Soft skills found: {len(skills['soft'])}")
            if skills['soft']:
                print(f"   {', '.join(skills['soft'][:5])}")

            print(f"🛠️ Tools found: {len(skills['tools'])}")
            if skills['tools']:
                print(f"   {', '.join(skills['tools'][:5])}")

            # Experience
            exp = result['experience']
            print(f"🏢 Companies found: {len(exp['companies'])}")
            if exp['companies']:
                print(f"   {', '.join(exp['companies'][:3])}")

            print(f"💼 Positions found: {len(exp['positions'])}")
            if exp['positions']:
                print(f"   {', '.join(exp['positions'][:3])}")

            # Education
            edu = result['education']
            print(f"🎓 Degrees found: {len(edu['degrees'])}")
            if edu['degrees']:
                print(f"   {', '.join(edu['degrees'][:3])}")

            print(f"🏫 Institutions found: {len(edu['institutions'])}")
            if edu['institutions']:
                print(f"   {', '.join(edu['institutions'][:3])}")

            # Contact Info
            contact = result['contact_info']
            print(f"📧 Email: {contact['email']}")
            print(f"📞 Phone: {contact['phone']}")
            print(f"📍 Location: {contact['location']}")

            print(f"\n📝 Text sample: {result['sample_text'][:200]}...")

        else:
            print(f"❌ File not found: {file}")

    print("\n" + "=" * 60)
    print("🎉 Document processor testing completed!")


def test_skill_extraction():
    """Test skill extraction with various text samples"""
    processor = DocumentProcessor()

    test_texts = [
        "I have experience with Python, JavaScript, and React. Also worked with AWS and Docker.",
        "My skills include Java, Spring Boot, MySQL, and I have strong communication and leadership abilities.",
        "Proficient in C++, Python, machine learning, and have excellent problem-solving skills."
    ]

    print("\n🔧 Testing Skill Extraction")
    print("=" * 40)

    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}: {text}")
        skills = processor.extract_skills(text)

        print(f"  Technical: {skills['technical']}")
        print(f"  Soft: {skills['soft']}")
        print(f"  Tools: {skills['tools']}")


if __name__ == "__main__":
    # First check if sample files exist
    required_files = ["sample_resume.pdf", "sample_transcript.pdf"]
    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print("❌ Missing sample files. Please run create_test_documents.py first.")
        print("Missing files:", missing_files)
    else:
        test_document_processor()
        test_skill_extraction()