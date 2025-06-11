import tempfile
import streamlit as st

from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_garden_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Image Upload
    with col1:
        st.subheader("📷 Upload Your Garden Photo")
        uploaded_image = st.file_uploader(
            "Upload a clear photo of your backyard or garden area",
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Site Preferences
    with col2:
        st.subheader("🌿 Site Conditions")

        lighting_conditions = st.selectbox(
            "What is the lighting like in your garden?",
            [
                "Full sun", "Partial sun", "Dappled light", "Mostly shaded"
            ]
        )

        climate_zone = st.selectbox(
            "Which climate best describes your area?",
            [
                "Tropical", "Subtropical", "Temperate", 
                "Arid/Desert", "Mountainous", "Coastal", "Not sure"
            ]
        )

    # Column 3: Design Intentions
    with col3:
        st.subheader("🎯 Garden Goals")

        garden_use = st.selectbox(
            "How do you want to use your garden?",
            [
                "Relaxation/sitting area", "Food growing (herbs/vegetables)",
                "Kids or pet play area", "Entertaining guests", "Multi-purpose"
            ]
        )

        watering_pref = st.selectbox(
            "How much watering are you comfortable with?",
            ["Low (drought-tolerant)", "Moderate", "High (lush garden)"]
        )

    return {
        "uploaded_image": uploaded_image,
        "lighting_conditions": lighting_conditions,
        "climate_zone": climate_zone,
        "garden_use": garden_use,
        "watering_pref": watering_pref
    }

def generate_garden_report(user_garden_preferences):
    uploaded_image = user_garden_preferences["uploaded_image"]
    lighting_conditions = user_garden_preferences["lighting_conditions"]
    climate_zone = user_garden_preferences["climate_zone"]
    garden_use = user_garden_preferences["garden_use"]
    watering_pref = user_garden_preferences["watering_pref"]

    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_image.getvalue())
        image_path = tmp.name

    # Step 1: Landscape Visual Analyzer Agent
    landscape_analyzer = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Landscape Visual Analyzer",
        role="Analyzes a garden photo to detect landscape type, sun exposure, vegetation pattern, and layout opportunities.",
        description=dedent("""
            You are a landscape analysis assistant. Review the uploaded garden photo to identify:
            - General landscape type (e.g., tropical, shaded, arid, mixed)
            - Sunlight exposure level and shadows
            - Soil visibility, slope, and planting density
            - Space division (open lawn, patio, beds, etc.)
            Your task is to produce a detailed visual assessment for planning a suitable garden layout.
        """),
        instructions=[
            "Inspect the garden image carefully.",
            "Identify the dominant landscape type and notable features (e.g., shaded corners, dry patches).",
            "Mention any visible planting opportunities or constraints (e.g., slope, crowded areas, paved zones).",
            "Avoid giving specific plant suggestions here—focus purely on visual interpretation.",
        ],
        markdown=True
    )

    visual_insights = landscape_analyzer.run(
        "Analyze this garden photo to assess the landscape and layout features.",
        images=[Image(filepath=image_path)]
    ).content

    garden_search_agent = Agent(
        name="Garden Research Assistant",
        role="Finds suitable plants, design layouts, and inspiration resources based on garden type and user preferences.",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        description="Generates targeted search prompts and uses SerpAPI to find plants and layout examples suitable for the user's garden environment.",
        instructions=[
            "Use the user's lighting conditions, climate, garden usage, and watering preference.",
            "Generate a focused Google search prompt (e.g., 'low-maintenance drought-tolerant plants for full sun arid backyard').",
            "Use SerpAPI to fetch 5–7 relevant gardening links (plant lists, layout ideas, blog posts, etc.).",
            "Return links in Markdown format with clear titles.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        markdown=True
    )

    # Construct the search prompt
    search_prompt = f"""
    Lighting Conditions: {lighting_conditions}
    Climate Zone: {climate_zone}
    Garden Use: {garden_use}
    Watering Preference: {watering_pref}
    
    Visual Landscape Insights:
    {visual_insights}

    Based on these inputs, generate a relevant Google search and return high-quality garden layout and planting inspiration links.
    """

    research_links = garden_search_agent.run(search_prompt).content

    report_generator = Agent(
        name="Garden Report Generator",
        model=OpenAIChat(id="o3-mini", api_key=st.session_state.openai_api_key),
        role="Generates a structured garden design recommendation report using visual insights and curated web links.",
        description=dedent("""
            You are a garden planning assistant. You are given:
            1. A visual analysis of a user's garden space.
            2. A set of garden preferences (sunlight, zone, goals, watering).
            3. Curated links to plant suggestions and layout ideas.

            Your job is to generate a detailed markdown report with helpful recommendations, layout suggestions, and linked inspiration sources.
        """),
        instructions=[
            "Start the report with: ## 🌿 Personalized Garden Design Report",
            "",
            "### 🖼️ Visual Landscape Insights",
            "- Describe the visual elements identified from the uploaded photo: surface condition, planting density, structures, lighting.",
            "- Mention soil, slope, layout zones, or shaded/open areas.",
            "- Embed hyperlinks to relevant garden layout styles if helpful (e.g., [sun-loving raised beds](https://...), [dry-climate lawn alternatives](https://...)).",
            "",
            "### 🌞 Environmental & Layout Context",
            "- Explain how the climate zone, lighting, and watering preferences affect layout design.",
            "- Recommend layout types or hardscaping approaches (e.g., xeriscaping, drip irrigation).",
            "- Embed helpful design inspiration links (e.g., [xeriscaping tips](https://...), [shaded patio layout](https://...)).",
            "",
            "### 🎯 Garden Usage Strategy",
            "- Provide layout ideas aligned with the intended use (e.g., seating corners, edible beds, play zones).",
            "- Mention functional flow: where seating could go, where herbs need sun, etc.",
            "- Embed examples or layout plans (e.g., [backyard seating nooks](https://...), [modular herb bed layout](https://...)).",
            "",
            "### 🌱 Planting Recommendations",
            "- Suggest general plant types suitable for the environment (e.g., succulents, native flowers, herbs).",
            "- Provide planting layout styles or plant combinations (e.g., layered borders, wildlife-attracting zones).",
            "- Embed plant guides or curated plant list links (e.g., [drought-tolerant plants list](https://...), [low-maintenance edible garden](https://...)).",
            "",
            "### 🔗 Curated Inspiration Resources",
            "- List the web-sourced links clearly with meaningful titles (e.g., [Backyard Layouts for Full Sun](https://...)).",
            "- Group them by theme if relevant (e.g., design, planting, sustainability).",
            "",
            "**Important:** Embed helpful, relevant hyperlinks throughout the report—not just in the final section. Aim for at least 1–2 embedded links per section.",
            "",
            "Write in a confident, positive, and user-friendly tone.",
            "Use markdown headings, bullet points, and short paragraphs.",
            "Return only the markdown-formatted report — no explanation or metadata."
        ],
        markdown=True,
        add_datetime_to_instructions=True
    )

    final_prompt = f"""
    Visual Analysis:
    {visual_insights}

    Web-Based Inspiration Links:
    {research_links}

    Generate a markdown-formatted garden recommendation report.
    """

    final_report = report_generator.run(final_prompt).content

    return final_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Garden Designer Bot", page_icon="🌿", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🌿 Garden Designer Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Garden Designer Bot — a smart Streamlit tool that analyzes your backyard photo, identifies the landscape type, and delivers a tailored planting plan with optimal layout suggestions for a beautiful, thriving green space.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_garden_preferences = render_garden_preferences()

    st.markdown("---")

    # Call the report generation method when the user clicks the button
    if st.button("🌿 Generate Garden Design Report"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        elif "uploaded_image" not in user_garden_preferences or not user_garden_preferences["uploaded_image"]:
            st.error("Please upload a garden photo before generating the report.")
        else:
            with st.spinner("Analyzing your garden and creating a personalized design report..."):
                report = generate_garden_report(user_garden_preferences)

                st.session_state.garden_report = report
                st.session_state.garden_image = user_garden_preferences["uploaded_image"]

    # Display and download
    if "garden_report" in st.session_state:
        st.markdown("## 🌱 Uploaded Garden Photo")
        st.image(st.session_state.garden_image, use_container_width=False)

        st.markdown(st.session_state.garden_report, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Garden Report",
            data=st.session_state.garden_report,
            file_name="garden_design_recommendation.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()
