# app.py

import streamlit as st
# from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
# from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY")


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Condense SEO Blog Generator",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: white;
}

# .stTextInput input,
# .stTextArea textarea {
#     background-color: #1e293b;
#     color: white;
#     border-radius: 10px;
#     border: 1px solid #334155;
# }

.stTextInput input,
.stTextArea textarea {
    background-color: white !important;
    color: black !important;
    border-radius: 10px;
    border: 2px solid #d1d5db;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #6b7280 !important;
}
.stButton button {
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 1.5rem;
    font-weight: bold;
}

.stDownloadButton button {
    background-color: #22c55e;
    color: white;
    border-radius: 10px;
}

.blog-box {
    background-color: white;
    color: black;
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid #d1d5db;
    margin-top: 2rem;
    line-height: 1.8;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------

st.title("🚀 Condense SEO Blog Generator")
st.caption("Generate human-like SEO optimized blogs with Condense context")

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:
    st.header("⚙️ Blog Settings")

    model_name = st.selectbox(
        "Select LLM",
        ["gemini-3-flash-preview", "gemini-3.1-flash-lite","gemini-2.5-flash"]
    )

    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.8
    )

# -----------------------------------
# INPUT FORM
# -----------------------------------

with st.form("blog_form"):

    blog_title = st.text_input(
        "📝 Blog Title",
        placeholder="Example: How Real-Time Streaming Changes IoT"
    )

    keywords = st.text_area(
        "🔍 SEO Keywords(optional)",
        placeholder="real-time streaming, kafka alternative, event streaming"
    )

    condense_points = st.text_area(
        "⚡ Condense Related Points",
        placeholder="Kafka-native, no-code pipelines, real-time dashboards"
    )

    success_story = st.text_area(
        "🏆 Condense Success Story",
        placeholder="Example: Reduced latency by 40% for a logistics company"
    )

    generate = st.form_submit_button("✨ Generate Blog")

# -----------------------------------
# PROMPT TEMPLATE
# -----------------------------------

BLOG_PROMPT = '''
You are an expert SEO blog writer for Condense.

Generate a highly engaging, SEO optimized, human-like article.

========================
USER INPUTS
========================

Blog Title:
{blog_title}

Keywords:
{keywords}

IMPORTANT:
- If keywords are not provided, intelligently generate SEO keywords from the blog title.
- Maintain proper keyword density naturally.

Condense Related Points:
{condense_points}

Condense Success Story:
{success_story}

========================
RULES
========================

- H1: 60-70 characters
- 1500+ words
- Add TL;DR
- First paragraph must answer the topic directly
- Meta Title: 60-70 chars
- Meta Description: 140-160 chars
- SEO friendly URL
- Short paragraphs
- Human-like tone
- Use keywords 6-8 times naturally
- Add FAQs
- Add "How Condense Helps"
- Add CTA
- Use H2 and H3 headings

Generate the complete blog now.
'''
# -----------------------------------
# GENERATE BLOG
# -----------------------------------

if generate:

    if not blog_title:
        st.error("Please enter Blog Title and Keywords")
    else:

        with st.spinner("Generating SEO optimized blog..."):

            prompt = PromptTemplate(
                input_variables=[
                    "blog_title",
                    "keywords",
                    "condense_points",
                    "success_story"
                ],
                template=BLOG_PROMPT
            )

            final_prompt = prompt.format(
                blog_title=blog_title,
                keywords=keywords,
                condense_points=condense_points,
                success_story=success_story
            )

            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature
            )

            response = llm.invoke(final_prompt)

            blog_output = response.content
            st.success("✅ Blog Generated Successfully")

            st.markdown(
                f"""
                <div class="blog-box">
                {blog_output}
                </div>
                """,
                unsafe_allow_html=True
            )

            # -----------------------------------
            # DOWNLOAD BUTTON
            # -----------------------------------

            st.download_button(
                label="📥 Download Blog",
                data=blog_output,
                file_name="condense_blog.md",
                mime="text/markdown"
            )