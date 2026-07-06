import streamlit as st
from google import genai

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide"
)

# -------------------------------
# CAREER DATA
# -------------------------------

CAREERS = {
    "AI Engineer": {
        "skills": ["python", "machine learning", "ai", "tensorflow", "pytorch"],
        "interests": ["artificial intelligence", "ai", "data", "automation"],
        "demand": "Very High",
        "missing_skills": ["PyTorch", "Vector Databases", "MLOps"]
    },

    "Backend Engineer": {
        "skills": ["python", "java", "fastapi", "api", "sql"],
        "interests": ["backend", "systems", "software development"],
        "demand": "High",
        "missing_skills": ["System Design", "Redis", "Docker"]
    },

    "Data Engineer": {
        "skills": ["python", "sql", "data", "spark"],
        "interests": ["data", "analytics", "databases"],
        "demand": "Very High",
        "missing_skills": ["Apache Spark", "Airflow", "Data Warehousing"]
    },

    "Cloud Engineer": {
        "skills": ["aws", "gcp", "cloud", "docker"],
        "interests": ["cloud", "infrastructure", "systems"],
        "demand": "High",
        "missing_skills": ["Kubernetes", "Terraform", "Cloud Security"]
    },

    "Cybersecurity Analyst": {
        "skills": ["networking", "linux", "security", "python"],
        "interests": ["cybersecurity", "security", "networks"],
        "demand": "Very High",
        "missing_skills": ["SIEM", "Ethical Hacking", "Threat Analysis"]
    },

    "Product Manager": {
        "skills": ["communication", "leadership", "management", "analytics"],
        "interests": ["business", "products", "leadership"],
        "demand": "High",
        "missing_skills": ["Product Analytics", "Market Research", "Roadmapping"]
    }
}


# -------------------------------
# CAREER SCORING ENGINE
# -------------------------------

def calculate_career_scores(skills, interests, cgpa):
    skills = skills.lower()
    interests = interests.lower()

    results = []

    for career, data in CAREERS.items():

        skill_matches = sum(
            1 for skill in data["skills"]
            if skill in skills
        )

        interest_matches = sum(
            1 for interest in data["interests"]
            if interest in interests
        )

        skill_score = (
            skill_matches / len(data["skills"])
        ) * 50

        interest_score = (
            interest_matches / len(data["interests"])
        ) * 35

        academic_score = min(cgpa / 10, 1) * 15

        total_score = round(
            skill_score +
            interest_score +
            academic_score
        )

        results.append({
            "career": career,
            "score": total_score,
            "demand": data["demand"],
            "missing_skills": data["missing_skills"]
        })

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )


# -------------------------------
# GEMINI AI
# -------------------------------

def generate_ai_analysis(
    api_key,
    name,
    degree,
    cgpa,
    skills,
    interests,
    work_style,
    top_career,
    missing_skills
):

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert AI career decision advisor.

Analyze the following student profile.

Student Name: {name}
Degree: {degree}
CGPA: {cgpa}
Skills: {skills}
Interests: {interests}
Preferred Work Style: {work_style}

The career matching engine ranked:
{top_career}

Current identified skill gaps:
{", ".join(missing_skills)}

Generate a personalized career decision report.

Use exactly these headings:

WHY THIS CAREER MATCHES

SKILL GAP ANALYSIS

90-DAY CAREER ACCELERATION ROADMAP

3 PORTFOLIO PROJECT IDEAS

CAREER DECISION SUMMARY

Keep the response concise, practical and personalized.
Do not use generic motivational language.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# -------------------------------
# USER INTERFACE
# -------------------------------

st.title("🎯 CareerLens AI")

st.subheader(
    "AI-Powered Career Decision Intelligence"
)

st.write(
    """
CareerLens AI analyzes your skills, interests and
academic profile to identify your strongest career
paths and generate a personalized acceleration roadmap.
"""
)

st.divider()

# Gemini API key loaded securely from Streamlit Secrets
api_key = st.secrets["GEMINI_API_KEY"]


st.header("👤 Student Profile")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Student Name"
    )

    degree = st.text_input(
        "Degree",
        placeholder="Example: B.Tech CSE"
    )

    cgpa = st.slider(
        "CGPA",
        0.0,
        10.0,
        8.0,
        0.1
    )


with col2:

    skills = st.text_area(
        "Technical and Professional Skills",
        placeholder="Python, FastAPI, AWS, Communication"
    )

    interests = st.text_area(
        "Career Interests",
        placeholder="Artificial Intelligence, Data, Backend Systems"
    )

    work_style = st.selectbox(
        "Preferred Work Style",
        [
            "Problem solving and building systems",
            "Working with data and analytics",
            "Leading teams and products",
            "Research and experimentation",
            "Security and investigation"
        ]
    )


st.divider()


# -------------------------------
# ANALYSIS
# -------------------------------

if st.button(
    "🚀 Analyze My Career Path",
    type="primary",
    use_container_width=True
):

    if not name or not degree or not skills or not interests:

        st.error(
            "Please complete all student profile fields."
        )

    else:

        with st.spinner(
            "Analyzing your career profile..."
        ):

            results = calculate_career_scores(
                skills,
                interests,
                cgpa
            )

            top_three = results[:3]

        st.success(
            "Career analysis completed."
        )

        st.header("🏆 Top Career Matches")

        cols = st.columns(3)

        for index, result in enumerate(top_three):

            with cols[index]:

                st.subheader(
                    f"#{index + 1} {result['career']}"
                )

                st.metric(
                    "Career Match Score",
                    f"{result['score']}%"
                )

                st.write(
                    f"📈 Future Demand: **{result['demand']}**"
                )


        st.divider()

        top_career = top_three[0]

        st.header("🎯 Recommended Career Decision")

        st.info(
            f"""
Your strongest career alignment is
**{top_career['career']}**
with a **{top_career['score']}% match score**.
"""
        )


        st.subheader("🧩 Identified Skill Gaps")

        for skill in top_career["missing_skills"]:

            st.write(f"❌ {skill}")


        st.divider()

        st.header("🤖 Gemini Career Intelligence Report")

        if api_key:

            try:

                ai_report = generate_ai_analysis(
                    api_key,
                    name,
                    degree,
                    cgpa,
                    skills,
                    interests,
                    work_style,
                    top_career["career"],
                    top_career["missing_skills"]
                )

                st.markdown(ai_report)

            except Exception as error:

                st.error(
                    f"Gemini analysis failed: {error}"
                )

        else:

            st.warning(
                """
Add your Gemini API key in the sidebar
to generate the personalized AI career roadmap.
"""
            )


st.divider()

st.caption(
    "CareerLens AI • AI-Powered Career Decision Intelligence"
)
