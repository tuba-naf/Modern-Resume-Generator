import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

def main():
    st.title("Modern Resume Generator")
    
    # Sidebar for navigation
    st.sidebar.title("Sections")
    section = st.sidebar.radio("Go to", ["Personal Information", "Education", "Experience", "Skills", "Generate PDF"])

    # Initialize session state for data persistence
    if 'personal_info' not in st.session_state:
        st.session_state.personal_info = {}
    if 'education' not in st.session_state:
        st.session_state.education = []
    if 'experience' not in st.session_state:
        st.session_state.experience = []
    if 'skills' not in st.session_state:
        st.session_state.skills = []

    if section == "Personal Information":
        personal_info_section()
    elif section == "Education":
        education_section()
    elif section == "Experience":
        experience_section()
    elif section == "Skills":
        skills_section()
    elif section == "Generate PDF":
        generate_pdf_section()

def personal_info_section():
    st.header("Personal Information")
    
    # Profile Picture Upload
    uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Save image in session state as bytes
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        st.session_state.personal_info['profile_picture'] = buffered.getvalue()
    
    # Display profile picture if it exists in session state
    if 'profile_picture' in st.session_state.personal_info:
        image_bytes = st.session_state.personal_info['profile_picture']
        image = Image.open(BytesIO(image_bytes))
        st.image(image, width=150)

    # Personal Information Form
    st.session_state.personal_info['name'] = st.text_input("Full Name", st.session_state.personal_info.get('name', ''))
    st.session_state.personal_info['email'] = st.text_input("Email", st.session_state.personal_info.get('email', ''))
    st.session_state.personal_info['phone'] = st.text_input("Phone", st.session_state.personal_info.get('phone', ''))
    st.session_state.personal_info['linkedin'] = st.text_input("LinkedIn URL", st.session_state.personal_info.get('linkedin', ''))
    st.session_state.personal_info['summary'] = st.text_area("Professional Summary", st.session_state.personal_info.get('summary', ''))

def education_section():
    st.header("Education")
    
    # Display existing education entries
    for i, edu in enumerate(st.session_state.education):
        st.subheader(f"Education #{i+1}")
        st.write(f"Institution: {edu['institution']}")
        st.write(f"Degree: {edu['degree']}")
        st.write(f"Year: {edu['year']}")
        if st.button(f"Remove Education #{i+1}"):
            st.session_state.education.pop(i)
            st.rerun()

    # Add new education entry
    st.subheader("Add New Education")
    institution = st.text_input("Institution Name")
    degree = st.text_input("Degree/Certificate")
    year = st.text_input("Year")
    
    if st.button("Add Education"):
        st.session_state.education.append({
            "institution": institution,
            "degree": degree,
            "year": year
        })
        st.success("Education added successfully!")
        st.rerun()

def experience_section():
    st.header("Work Experience")
    
    # Display existing experience entries
    for i, exp in enumerate(st.session_state.experience):
        st.subheader(f"Experience #{i+1}")
        st.write(f"Company: {exp['company']}")
        st.write(f"Position: {exp['position']}")
        st.write(f"Duration: {exp['duration']}")
        st.write(f"Description: {exp['description']}")
        if st.button(f"Remove Experience #{i+1}"):
            st.session_state.experience.pop(i)
            st.rerun()

    # Add new experience entry
    st.subheader("Add New Experience")
    company = st.text_input("Company Name")
    position = st.text_input("Position")
    duration = st.text_input("Duration")
    description = st.text_area("Description")
    
    if st.button("Add Experience"):
        st.session_state.experience.append({
            "company": company,
            "position": position,
            "duration": duration,
            "description": description
        })
        st.success("Experience added successfully!")
        st.rerun()

def skills_section():
    st.header("Skills")
    
    # Display existing skills
    for i, skill in enumerate(st.session_state.skills):
        st.write(f"• {skill}")
        if st.button(f"Remove Skill #{i+1}"):
            st.session_state.skills.pop(i)
            st.rerun()

    # Add new skill
    new_skill = st.text_input("Add a new skill")
    if st.button("Add Skill"):
        if new_skill:
            st.session_state.skills.append(new_skill)
            st.success("Skill added successfully!")
            st.rerun()

def generate_pdf_section():
    st.header("Generate Resume PDF")
    
    if st.button("Generate PDF"):
        pdf_buffer = create_pdf()
        st.download_button(
            label="Download Resume PDF",
            data=pdf_buffer,
            file_name="resume.pdf",
            mime="application/pdf"
        )

def create_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add profile picture to PDF if it exists
    if 'profile_picture' in st.session_state.personal_info:
        image_bytes = st.session_state.personal_info['profile_picture']
        img = Image.open(BytesIO(image_bytes))
        # Resize image for PDF if needed
        img = img.resize((100, 100))  # Adjust size as needed
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Create reportlab Image object
        from reportlab.platypus import Image as RLImage
        img = RLImage(img_buffer, width=100, height=100)  # Adjust size as needed
        story.append(img)
        story.append(Spacer(1, 12))

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12
    )
    normal_style = styles['Normal']

    # Personal Information
    story.append(Paragraph(st.session_state.personal_info.get('name', ''), title_style))
    story.append(Paragraph(f"Email: {st.session_state.personal_info.get('email', '')}", normal_style))
    story.append(Paragraph(f"Phone: {st.session_state.personal_info.get('phone', '')}", normal_style))
    story.append(Paragraph(f"LinkedIn: {st.session_state.personal_info.get('linkedin', '')}", normal_style))
    story.append(Spacer(1, 12))

    # Summary
    if st.session_state.personal_info.get('summary'):
        story.append(Paragraph("Professional Summary", heading_style))
        story.append(Paragraph(st.session_state.personal_info['summary'], normal_style))
        story.append(Spacer(1, 12))

    # Education
    if st.session_state.education:
        story.append(Paragraph("Education", heading_style))
        for edu in st.session_state.education:
            story.append(Paragraph(f"{edu['institution']}", normal_style))
            story.append(Paragraph(f"{edu['degree']} - {edu['year']}", normal_style))
        story.append(Spacer(1, 12))

    # Experience
    if st.session_state.experience:
        story.append(Paragraph("Work Experience", heading_style))
        for exp in st.session_state.experience:
            story.append(Paragraph(f"{exp['company']} - {exp['position']}", normal_style))
            story.append(Paragraph(f"{exp['duration']}", normal_style))
            story.append(Paragraph(f"{exp['description']}", normal_style))
            story.append(Spacer(1, 12))

    # Skills
    if st.session_state.skills:
        story.append(Paragraph("Skills", heading_style))
        skills_text = ", ".join(st.session_state.skills)
        story.append(Paragraph(skills_text, normal_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

if __name__ == "__main__":
    st.set_page_config(page_title="Resume Generator", layout="wide")
    main()
