import pdfplumber
import re
import os


class DocumentProcessor:
    def __init__(self):
        self.skill_keywords = {
            'programming': ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'sql', 'html', 'css', 'react',
                            'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'aws', 'azure', 'docker',
                            'kubernetes', 'git', 'mongodb', 'mysql', 'postgresql', 'redis'],
            'soft_skills': ['communication', 'leadership', 'teamwork', 'problem solving', 'time management',
                            'adaptability', 'creativity', 'critical thinking', 'emotional intelligence',
                            'conflict resolution', 'project management', 'analytical skills', 'presentation'],
            'tools': ['excel', 'word', 'powerpoint', 'jira', 'confluence', 'slack', 'teams', 'trello', 'asana']
        }

    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF with detailed parsing"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract text
                    page_text = page.extract_text() or ""
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"

                    # Try to extract tables
                    tables = page.extract_tables()
                    for table_num, table in enumerate(tables):
                        if table:
                            text += f"\n--- Table {table_num + 1} ---\n"
                            for row in table:
                                text += " | ".join(str(cell) for cell in row if cell) + "\n"

            return self.clean_text(text)
        except Exception as e:
            print(f"Error extracting from PDF {file_path}: {e}")
            return ""

    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX files"""
        try:
            import docx2txt
            text = docx2txt.process(file_path)
            return self.clean_text(text)
        except ImportError:
            return "DOCX processing not available"
        except Exception as e:
            print(f"Error extracting from DOCX {file_path}: {e}")
            return ""

    def clean_text(self, text):
        """Clean and normalize extracted text"""
        # Remove excessive whitespace but preserve line breaks for structure
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n +', '\n', text)
        return text.strip()

    def extract_skills(self, text):
        """Extract skills from text"""
        found_skills = {
            'technical': [],
            'soft': [],
            'tools': []
        }

        text_lower = text.lower()

        # Extract technical skills
        for skill in self.skill_keywords['programming']:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills['technical'].append(skill.title())

        # Extract soft skills
        for skill in self.skill_keywords['soft_skills']:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills['soft'].append(skill.title())

        # Extract tools
        for tool in self.skill_keywords['tools']:
            if re.search(r'\b' + re.escape(tool) + r'\b', text_lower):
                found_skills['tools'].append(tool.title())

        return found_skills

    def extract_experience(self, text):
        """Extract work experience information"""
        experience_info = {
            'companies': [],
            'positions': [],
            'durations': []
        }

        # Improved company patterns
        company_patterns = [
            r'(?:at|with|from)\s+([A-Z][a-zA-Z0-9\s&.,-]+(?:Inc|LLC|Corp|Corporation|Company|Ltd|Group))',
            r'([A-Z][a-zA-Z0-9\s&.,-]+(?:Inc|LLC|Corp|Corporation|Company|Ltd|Group))\s',
        ]

        # Improved position patterns
        position_patterns = [
            r'(?:as\s+)?([A-Z][a-zA-Z\s]+(?:Engineer|Developer|Manager|Analyst|Specialist|Consultant|Director|Architect))',
            r'([A-Z][a-zA-Z\s]+(?:Engineer|Developer|Manager|Analyst|Specialist|Consultant|Director|Architect))\s',
        ]

        # Improved duration patterns
        duration_patterns = [
            r'(\d{4}\s*[-–]\s*(?:\d{4}|present|current|now))',
            r'(\d+\s+(?:years?|months?))',
        ]

        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            experience_info['companies'].extend([m.strip() for m in matches])

        for pattern in position_patterns:
            matches = re.findall(pattern, text)
            experience_info['positions'].extend([m.strip() for m in matches])

        for pattern in duration_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            experience_info['durations'].extend(matches)

        # Remove duplicates and empty strings
        for key in experience_info:
            experience_info[key] = list(set([item for item in experience_info[key] if item and len(item) > 2]))

        return experience_info

    def extract_education(self, text):
        """Extract education information"""
        education_info = {
            'degrees': [],
            'institutions': [],
            'years': []
        }

        # Improved degree patterns
        degree_patterns = [
            r'\b(Bachelor|B\.?S\.?|B\.?A\.?|Master|M\.?S\.?|M\.?A\.?|PhD|Doctorate)\b',
            r'\b(Associate|Diploma|Certificate)\b'
        ]

        # Improved institution patterns
        institution_patterns = [
            r'(?:University|College|Institute|School)\s+of\s+[A-Z][a-zA-Z\s]+',
            r'[A-Z][a-zA-Z\s]+(?:University|College|Institute|School)'
        ]

        # Year patterns
        year_patterns = [
            r'\b(?:19|20)\d{2}\b',
        ]

        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education_info['degrees'].extend(matches)

        for pattern in institution_patterns:
            matches = re.findall(pattern, text)
            education_info['institutions'].extend(matches)

        for pattern in year_patterns:
            matches = re.findall(pattern, text)
            education_info['years'].extend(matches)

        # Remove duplicates and empty strings
        for key in education_info:
            education_info[key] = list(set([item for item in education_info[key] if item]))

        return education_info

    def extract_contact_info(self, text):
        """Extract contact information with improved patterns"""
        contact_info = {
            'email': '',
            'phone': '',
            'location': ''
        }

        # Improved email pattern
        email_patterns = [
            r'[Ee]mail\s*:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        ]

        for pattern in email_patterns:
            email_match = re.search(pattern, text)
            if email_match:
                contact_info['email'] = email_match.group(1) if email_match.groups() else email_match.group()
                break

        # Improved phone patterns
        phone_patterns = [
            r'[Pp]hone\s*:\s*([+]?[\d\s\-().]+)',
            r'[Tt]el\s*:\s*([+]?[\d\s\-().]+)',
            r'([+]?[\d\s\-().]{10,})'
        ]

        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                phone_number = phone_match.group(1) if phone_match.groups() else phone_match.group()
                # Clean up the phone number
                phone_number = re.sub(r'[^\d+]', '', phone_number)
                if len(phone_number) >= 10:  # Valid phone number
                    contact_info['phone'] = phone_number
                    break

        # Improved location patterns
        location_patterns = [
            r'[Ll]ocation\s*:\s*([A-Z][a-zA-Z\s,]+)',
            r'[Aa]ddress\s*:\s*([A-Z][a-zA-Z\s,]+)',
            r'(?:based in|located in|from)\s+([A-Z][a-zA-Z\s,]+)',
        ]

        for pattern in location_patterns:
            location_match = re.search(pattern, text, re.IGNORECASE)
            if location_match:
                contact_info['location'] = location_match.group(1).strip()
                break

        return contact_info

    def analyze_document(self, file_path):
        """Comprehensive document analysis"""
        if not os.path.exists(file_path):
            return {"error": "File not found"}

        # Extract text based on file type
        ext = file_path.lower().split('.')[-1]
        if ext == 'pdf':
            text = self.extract_text_from_pdf(file_path)
        elif ext in ['doc', 'docx']:
            text = self.extract_text_from_docx(file_path)
        else:
            return {"error": f"Unsupported file type: {ext}"}

        if not text or len(text.strip()) < 10:
            return {"error": "No text extracted from document"}

        # Perform various analyses
        analysis = {
            'raw_text_length': len(text),
            'sample_text': text[:500] + "..." if len(text) > 500 else text,
            'skills': self.extract_skills(text),
            'experience': self.extract_experience(text),
            'education': self.extract_education(text),
            'contact_info': self.extract_contact_info(text),
            'word_count': len(text.split()),
            'estimated_pages': len(text) // 1500 + 1
        }

        return analysis


# Test the document processor
if __name__ == "__main__":
    processor = DocumentProcessor()

    # Test with a sample file if available
    test_files = [f for f in os.listdir('.') if f.lower().endswith(('.pdf', '.doc', '.docx'))]

    if test_files:
        print("Testing document processor with:", test_files[0])
        result = processor.analyze_document(test_files[0])
        print("\n" + "=" * 60)
        print("DOCUMENT ANALYSIS RESULTS:")
        print("=" * 60)
        print(f"Text length: {result['raw_text_length']} characters")
        print(f"Word count: {result['word_count']}")
        print(f"Estimated pages: {result['estimated_pages']}")
        print(f"\nSkills found:")
        print(f"  Technical: {', '.join(result['skills']['technical'][:10])}")
        print(f"  Soft: {', '.join(result['skills']['soft'][:10])}")
        print(f"  Tools: {', '.join(result['skills']['tools'][:10])}")
        print(f"\nCompanies found: {', '.join(result['experience']['companies'][:5])}")
        print(f"Positions found: {', '.join(result['experience']['positions'][:5])}")
        print(f"Degrees found: {', '.join(result['education']['degrees'][:5])}")
        print(f"Institutions found: {', '.join(result['education']['institutions'][:5])}")
        print(f"\nContact Info:")
        print(f"  Email: {result['contact_info']['email']}")
        print(f"  Phone: {result['contact_info']['phone']}")
        print(f"  Location: {result['contact_info']['location']}")
        print(f"\nText sample: {result['sample_text']}")
    else:
        print("No PDF or DOCX files found for testing.")