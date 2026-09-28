import textwrap

import streamlit as st
from PIL import Image

from disease_info import DISEASE_KNOWLEDGE
from model_utils import predict_leaf


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FungiScan AI",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "initial_scan" not in st.session_state:
    st.session_state.initial_scan = None

if "final_result" not in st.session_state:
    st.session_state.final_result = None

if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

if "last_image_key" not in st.session_state:
    st.session_state.last_image_key = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def render_html(markup):
    st.html(
        textwrap.dedent(markup)
    )


def change_page(page):
    st.session_state.active_tab = page
    st.rerun()


def reset_scan():
    st.session_state.initial_scan = None
    st.session_state.final_result = None


def prettify(text):
    return text.replace("_", " ").strip().title()


# ============================================================
# CROP INFORMATION
# ============================================================

CROP_INFO = {
    "Apple": {
        "scientific": "Malus domestica",
        "icon": "🍎",
    },
    "Cherry": {
        "scientific": "Prunus avium / Prunus cerasus",
        "icon": "🍒",
    },
    "Corn": {
        "scientific": "Zea mays",
        "icon": "🌽",
    },
    "Grape": {
        "scientific": "Vitis vinifera",
        "icon": "🍇",
    },
    "Potato": {
        "scientific": "Solanum tuberosum",
        "icon": "🥔",
    },
    "Squash": {
        "scientific": "Cucurbita spp.",
        "icon": "🎃",
    },
    "Strawberry": {
        "scientific": "Fragaria × ananassa",
        "icon": "🍓",
    },
    "Tomato": {
        "scientific": "Solanum lycopersicum",
        "icon": "🍅",
    },
}

SUPPORTED_CROPS = list(CROP_INFO.keys())


# ============================================================
# MODEL-CONDITION → KNOWLEDGE-BASE MAPPING
# ============================================================

CONDITION_ALIASES = {
    "Healthy": "Healthy Foliage",
    "Early Blight": "Early Blight",
    "Powdery Mildew": "Powdery Mildew",
    "Septoria Leaf Spot": "Septoria Leaf Spot",
    "Apple Scab": "Apple Scab",
    "Cercospora Leaf Spot": "Cercospora Leaf Spot",
    "Common Rust": "Leaf Rust",
}


# ============================================================
# EXTRA FUNGAL PROFILES
# These cover model classes not present in disease_info.py
# ============================================================

EXTRA_DISEASE_INFO = {
    "Black Rot": {
        "scientific_name": "Guignardia bidwellii",
        "category": "Ascomycete Fungus",
        "urgency": "Moderate to High",
        "symptoms": [
            "Small reddish-brown foliar lesions that enlarge and develop dark margins",
            "Tiny black fungal fruiting bodies may develop within lesions",
            "Fruit can shrivel into dark, hard mummified berries",
        ],
        "prevention": [
            "Remove infected leaves and mummified fruit from the growing area",
            "Improve canopy airflow through pruning and plant spacing",
            "Avoid prolonged leaf wetness and unnecessary overhead irrigation",
        ],
        "treatment": (
            "Use locally approved fungicidal or biological management "
            "according to crop-specific agricultural recommendations."
        ),
    },

    "Cedar Apple Rust": {
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "category": "Basidiomycete Rust Fungus",
        "urgency": "Moderate",
        "symptoms": [
            "Bright yellow-orange spots on the upper leaf surface",
            "Small dark fruiting structures may appear within lesions",
            "Severe infection can cause premature leaf drop",
        ],
        "prevention": [
            "Use resistant apple cultivars where available",
            "Reduce nearby infected juniper hosts when practical",
            "Improve canopy ventilation and remove heavily infected foliage",
        ],
        "treatment": (
            "Use appropriate rust-management practices and locally approved "
            "fungicides where disease pressure is significant."
        ),
    },

    "Northern Leaf Blight": {
        "scientific_name": "Exserohilum turcicum",
        "category": "Ascomycete Fungus",
        "urgency": "Moderate to High",
        "symptoms": [
            "Long cigar-shaped gray-green or tan lesions on corn leaves",
            "Lesions enlarge and may merge under severe disease pressure",
            "Large affected areas reduce photosynthetic leaf surface",
        ],
        "prevention": [
            "Select resistant corn hybrids",
            "Rotate crops and manage infected crop residues",
            "Maintain appropriate spacing and field sanitation",
        ],
        "treatment": (
            "Fungicide application may be considered when disease pressure "
            "and crop stage justify treatment."
        ),
    },

    "Esca Black Measles": {
        "scientific_name": "Phaeomoniella chlamydospora / Phaeoacremonium spp.",
        "category": "Grapevine Trunk Disease Complex",
        "urgency": "High",
        "symptoms": [
            "Interveinal leaf discoloration producing tiger-stripe patterns",
            "Dark spotting can occur on berries",
            "Chronic infections may contribute to vine decline",
        ],
        "prevention": [
            "Use clean planting material",
            "Protect pruning wounds and disinfect tools",
            "Remove severely affected woody material",
        ],
        "treatment": (
            "Management mainly relies on sanitation, pruning-wound protection "
            "and removal of badly affected vine tissues."
        ),
    },

    "Leaf Blight": {
        "scientific_name": "Pseudocercospora vitis / Isariopsis clavispora",
        "category": "Fungal Leaf Spot / Blight",
        "urgency": "Moderate",
        "symptoms": [
            "Irregular brown lesions developing on grape leaves",
            "Lesions may expand and produce scorched-looking foliage",
            "Severe infections can cause premature defoliation",
        ],
        "prevention": [
            "Remove infected foliage and crop debris",
            "Improve airflow within the vine canopy",
            "Avoid unnecessary prolonged leaf wetness",
        ],
        "treatment": (
            "Use suitable crop-specific fungal disease management where needed."
        ),
    },

    "Leaf Scorch": {
        "scientific_name": "Diplocarpon earlianum",
        "category": "Ascomycete Fungus",
        "urgency": "Moderate",
        "symptoms": [
            "Small purple to reddish spots on strawberry foliage",
            "Spots may merge and give leaves a scorched appearance",
            "Severe infections can reduce healthy photosynthetic tissue",
        ],
        "prevention": [
            "Remove infected foliage and old plant debris",
            "Maintain adequate plant spacing",
            "Keep foliage dry when possible",
        ],
        "treatment": (
            "Use appropriate strawberry disease-management practices "
            "and locally approved fungicides when required."
        ),
    },

    "Leaf Mold": {
        "scientific_name": "Passalora fulva",
        "category": "Ascomycete Fungus",
        "urgency": "Moderate",
        "symptoms": [
            "Pale yellow patches develop on upper tomato leaf surfaces",
            "Olive-green to brown velvety fungal growth forms underneath leaves",
            "Severe infections can lead to leaf curling and premature decline",
        ],
        "prevention": [
            "Reduce greenhouse humidity and improve ventilation",
            "Space plants to promote airflow",
            "Avoid wetting foliage during irrigation",
        ],
        "treatment": (
            "Remove heavily affected leaves and use appropriate crop-specific "
            "fungal management where necessary."
        ),
    },

    "Target Spot": {
        "scientific_name": "Corynespora cassiicola",
        "category": "Ascomycete Fungus",
        "urgency": "Moderate",
        "symptoms": [
            "Brown circular lesions often showing concentric rings",
            "Lesions may develop yellow halos",
            "Severe infection can cause premature defoliation",
        ],
        "prevention": [
            "Increase airflow around tomato foliage",
            "Remove infected leaves and crop debris",
            "Avoid prolonged moisture on leaf surfaces",
        ],
        "treatment": (
            "Use integrated crop sanitation and locally recommended "
            "fungal disease-management measures."
        ),
    },
}


def get_disease_info(condition, crop=None):

    # Crop-specific Black Rot handling
    if crop == "Apple" and condition == "Black Rot":
        return {
            "scientific_name": "Botryosphaeria obtusa",
            "category": "Ascomycete Fungus",
            "urgency": "Moderate to High",
            "symptoms": [
                "Purple flecks on leaves that enlarge into brown lesions",
                "Frog-eye leaf spots with tan centers and dark purple margins",
                "Dark sunken fruit lesions that expand into black rot",
                "Infected fruit may shrivel and remain attached as mummies",
            ],
            "prevention": [
                "Remove dead wood, mummified fruit and infected plant debris",
                "Prune cankers and damaged branches",
                "Maintain good orchard airflow",
                "Sanitize pruning equipment between trees",
            ],
            "treatment": (
                "Use appropriate orchard sanitation and locally approved "
                "fungicidal management according to apple disease recommendations."
            ),
        }

    if crop == "Grape" and condition == "Black Rot":
        return {
            "scientific_name": "Guignardia bidwellii",
            "category": "Ascomycete Fungus",
            "urgency": "Moderate to High",
            "symptoms": [
                "Small reddish-brown lesions develop on grape leaves",
                "Dark fungal fruiting bodies may appear inside lesions",
                "Berries develop brown spots and eventually shrivel",
                "Severely infected fruit becomes hard black mummies",
            ],
            "prevention": [
                "Remove infected leaves and mummified berries",
                "Prune vines to improve canopy airflow",
                "Reduce prolonged leaf wetness",
                "Maintain vineyard sanitation",
            ],
            "treatment": (
                "Use integrated vineyard sanitation and locally approved "
                "fungal disease-management measures."
            ),
        }

    # Existing knowledge-base aliases
    key = CONDITION_ALIASES.get(condition)

    if key and key in DISEASE_KNOWLEDGE:
        return DISEASE_KNOWLEDGE[key]

    return EXTRA_DISEASE_INFO.get(condition)

# ============================================================
# THEME
# ============================================================

theme_toggle = st.toggle(
    "🌙 Dark mode",
    value=st.session_state.theme == "Dark",
)

st.session_state.theme = "Dark" if theme_toggle else "Light"

dark = st.session_state.theme == "Dark"


if dark:
    COLORS = {
        "bg": "#08130e",
        "surface": "#102219",
        "surface2": "#152b20",
        "text": "#eef8f1",
        "muted": "#a9c0b1",
        "primary": "#77d49a",
        "primary_dark": "#174b31",
        "border": "#294638",
        "soft": "#193124",
        "warning": "#382f14",
    }
else:
    COLORS = {
        "bg": "#f5f8f3",
        "surface": "#ffffff",
        "surface2": "#eef4ed",
        "text": "#123425",
        "muted": "#687d70",
        "primary": "#1e7148",
        "primary_dark": "#0b3824",
        "border": "#dce7de",
        "soft": "#e8f2e9",
        "warning": "#fff8d8",
    }


# ============================================================
# GLOBAL CSS
# ============================================================

render_html(
    f"""
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,500..700;1,6..72,500..700&display=swap'
    );

    :root {{
        --bg: {COLORS["bg"]};
        --surface: {COLORS["surface"]};
        --surface2: {COLORS["surface2"]};
        --text: {COLORS["text"]};
        --muted: {COLORS["muted"]};
        --primary: {COLORS["primary"]};
        --primary-dark: {COLORS["primary_dark"]};
        --border: {COLORS["border"]};
        --soft: {COLORS["soft"]};
    }}

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(
                circle at top right,
                rgba(70, 150, 100, 0.12),
                transparent 30%
            ),
            var(--bg);
        color: var(--text);
    }}

    #MainMenu,
    header,
    footer {{
        visibility: hidden;
    }}

    .block-container {{
        max-width: 880px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3, h4, h5 {{
        color: var(--text) !important;
    }}

    p, span, label {{
        color: inherit;
    }}

    .brand-header {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 18px 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 8px 0 18px 0;
        box-shadow: 0 10px 35px rgba(20, 70, 45, 0.08);
    }}

    .brand-title {{
        font-family: 'Newsreader', serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text);
        line-height: 1;
    }}

    .brand-sub {{
        margin-top: 6px;
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }}

    .brand-icon {{
        font-size: 1.8rem;
    }}

    .hero-card {{
        background:
            linear-gradient(
                145deg,
                var(--surface),
                var(--surface2)
            );
        border: 1px solid var(--border);
        border-radius: 30px;
        padding: 34px 30px;
        text-align: center;
        margin: 8px 0 20px 0;
        box-shadow: 0 18px 50px rgba(16, 72, 44, 0.10);
    }}

    .hero-kicker {{
        display: inline-block;
        border-radius: 999px;
        padding: 7px 13px;
        background: var(--soft);
        color: var(--primary);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 18px;
    }}

    .hero-title {{
        font-family: 'Newsreader', serif;
        color: var(--text);
        font-size: 2.7rem;
        line-height: 1.05;
        font-weight: 700;
        margin-bottom: 14px;
    }}

    .hero-copy {{
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.7;
        max-width: 600px;
        margin: 0 auto;
    }}

    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 20px 0;
    }}

    .mini-card {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 17px;
        text-align: center;
    }}

    .mini-icon {{
        font-size: 1.55rem;
        margin-bottom: 8px;
    }}

    .mini-title {{
        font-weight: 700;
        color: var(--text);
        margin-bottom: 4px;
    }}

    .mini-copy {{
        color: var(--muted);
        font-size: 0.78rem;
        line-height: 1.45;
    }}

    .section-card {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 22px;
        margin: 12px 0;
    }}

    .result-card {{
        background:
            linear-gradient(
                140deg,
                var(--surface),
                var(--surface2)
            );
        border: 1px solid var(--border);
        border-radius: 26px;
        padding: 24px;
        margin: 18px 0;
        box-shadow: 0 14px 40px rgba(20, 70, 45, 0.10);
    }}

    .result-label {{
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }}

    .result-main {{
        font-family: 'Newsreader', serif;
        font-size: 2rem;
        color: var(--text);
        font-weight: 700;
        margin: 5px 0;
    }}

    .result-scientific {{
        color: var(--muted);
        font-style: italic;
        margin-bottom: 15px;
    }}

    .confidence-high {{
        color: #228653;
        font-weight: 700;
    }}

    .confidence-moderate {{
        color: #b7791f;
        font-weight: 700;
    }}

    .confidence-low {{
        color: #c54b47;
        font-weight: 700;
    }}

    .tag {{
        display: inline-block;
        background: var(--soft);
        color: var(--primary);
        border-radius: 999px;
        padding: 6px 11px;
        font-size: 0.72rem;
        font-weight: 700;
        margin: 3px;
    }}

    .metric-note {{
        color: var(--muted);
        font-size: 0.78rem;
        line-height: 1.5;
        margin-top: 8px;
    }}

    div.stButton > button {{
        width: 100%;
        border-radius: 14px !important;
        min-height: 46px;
        font-weight: 700 !important;
        border: 1px solid var(--border) !important;
    }}

    div.stButton > button[kind="primary"] {{
        background: var(--primary-dark) !important;
        color: white !important;
    }}

    div[data-testid="stFileUploader"],
    div[data-testid="stCameraInput"] {{
        background: var(--surface);
        border-radius: 18px;
        border: 1px solid var(--border);
        padding: 8px;
    }}

    div[data-testid="stExpander"] {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        overflow: hidden;
    }}

    [data-testid="stMetric"] {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 17px;
        padding: 14px;
    }}

    .footer-note {{
        text-align: center;
        color: var(--muted);
        font-size: 0.75rem;
        margin-top: 28px;
        line-height: 1.6;
    }}

    @media (max-width: 650px) {{
        .feature-grid {{
            grid-template-columns: 1fr;
        }}

        .hero-title {{
            font-size: 2.15rem;
        }}

        .hero-card {{
            padding: 26px 20px;
        }}
    }}
    </style>
    """
)


# ============================================================
# HEADER
# ============================================================

render_html(
    """
    <div class="brand-header">
        <div>
            <div class="brand-title">FungiScan AI</div>
            <div class="brand-sub">Botany × Data Science</div>
        </div>
        <div class="brand-icon">🌿 🔬</div>
    </div>
    """
)


# ============================================================
# NAVIGATION
# ============================================================

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    if st.button("🏡 Home", use_container_width=True):
        change_page("Home")

with nav2:
    if st.button("📷 Analyze", use_container_width=True):
        change_page("Analyze")

with nav3:
    if st.button("📖 Guide", use_container_width=True):
        change_page("Guide")

with nav4:
    if st.button("📊 Research", use_container_width=True):
        change_page("Research")


# ============================================================
# PAGE 1 — HOME
# ============================================================

if st.session_state.active_tab == "Home":

    render_html(
        """
        <div class="hero-card">
            <div class="hero-kicker">
                AI-assisted foliar screening
            </div>

            <div style="font-size:4.8rem; margin-bottom:10px;">
                🍃
            </div>

            <div class="hero-title">
                Where Botany meets
                artificial intelligence.
            </div>

            <div class="hero-copy">
                FungiScan AI combines plant pathology,
                MobileNetV2 transfer learning and botanical
                knowledge to screen foliar images for fungal
                disease patterns.
            </div>
        </div>

        <div class="feature-grid">

            <div class="mini-card">
                <div class="mini-icon">📷</div>
                <div class="mini-title">Scan a leaf</div>
                <div class="mini-copy">
                    Upload an image or capture one directly
                    with the camera.
                </div>
            </div>

            <div class="mini-card">
                <div class="mini-icon">🍄</div>
                <div class="mini-title">Screen disease</div>
                <div class="mini-copy">
                    Compare foliar visual features with
                    supported fungal conditions.
                </div>
            </div>

            <div class="mini-card">
                <div class="mini-icon">🧬</div>
                <div class="mini-title">Explore pathology</div>
                <div class="mini-copy">
                    Review symptoms, pathogen information
                    and preventive management.
                </div>
            </div>

        </div>
        """
    )

    if st.button(
        "🔬 Start Foliar Screening",
        type="primary",
        use_container_width=True,
    ):
        change_page("Analyze")

    st.markdown("### Supported crops")

    render_html(
        """
        <div style="text-align:center;">
            <span class="tag">🍎 Apple</span>
            <span class="tag">🍒 Cherry</span>
            <span class="tag">🌽 Corn</span>
            <span class="tag">🍇 Grape</span>
            <span class="tag">🥔 Potato</span>
            <span class="tag">🎃 Squash</span>
            <span class="tag">🍓 Strawberry</span>
            <span class="tag">🍅 Tomato</span>
        </div>
        """
    )

    render_html(
        """
        <div class="footer-note">
            Educational research prototype.
            AI predictions should be interpreted alongside
            botanical observation and, where needed,
            laboratory or expert confirmation.
        </div>
        """
    )


# ============================================================
# PAGE 2 — ANALYZE
# ============================================================

elif st.session_state.active_tab == "Analyze":

    st.markdown("## 🔬 Analyze Leaf Specimen")

    st.caption(
        "Capture or upload a clear leaf image for AI-assisted fungal screening."
    )

    render_html(
        """
        <div style="margin:10px 0 18px 0;">
            <span class="tag">MobileNetV2</span>
            <span class="tag">Transfer Learning</span>
            <span class="tag">24 Crop–Condition Classes</span>
        </div>
        """
    )

    st.info(
        "📸 For best results: use one clearly visible leaf, "
        "good natural lighting, minimal background clutter "
        "and keep the affected region in focus."
    )

    scan_method = st.radio(
        "Image source",
        ["Upload Photo", "Take Photo"],
        horizontal=True,
    )

    img_file = None

    if scan_method == "Upload Photo":
        img_file = st.file_uploader(
            "Upload Leaf Photo",
            type=["jpg", "jpeg", "png"],
        )

    else:
        img_file = st.camera_input(
            "Take a clear photograph of the leaf"
        )

    image = None

    if img_file is not None:

        image_bytes = img_file.getvalue()
        current_image_key = hash(image_bytes)

        if current_image_key != st.session_state.last_image_key:
            st.session_state.last_image_key = current_image_key
            reset_scan()

        image = Image.open(img_file).convert("RGB")

        st.image(
            image,
            caption="Leaf specimen ready for screening",
            use_container_width=True,
        )

        render_html(
            """
            <div class="section-card">
                <strong>🌿 Specimen loaded successfully</strong>
                <div style="
                    color:var(--muted);
                    font-size:0.82rem;
                    margin-top:5px;
                ">
                    Step 1 identifies the most likely crop.
                    You can confirm or correct it before the
                    fungal-condition screening.
                </div>
            </div>
            """
        )

        if st.button(
            "🌿 Step 1 — Detect Crop",
            type="primary",
            use_container_width=True,
        ):

            with st.spinner(
                "FungiScan AI is examining botanical features..."
            ):
                st.session_state.initial_scan = predict_leaf(image)

            st.session_state.final_result = None


    # --------------------------------------------------------
    # CROP CONFIRMATION
    # --------------------------------------------------------

    if (
        image is not None
        and st.session_state.initial_scan is not None
    ):

        initial_result = st.session_state.initial_scan

        detected_crop = initial_result["crop"]
        detected_crop_confidence = initial_result.get(
            "crop_confidence",
            initial_result["confidence"],
        )

        crop_meta = CROP_INFO.get(
            detected_crop,
            {
                "scientific": "Unknown",
                "icon": "🌱",
            },
        )

        render_html(
            f"""
            <div class="result-card">

                <div class="result-label">
                    AI crop suggestion
                </div>

                <div class="result-main">
                    {crop_meta["icon"]} {detected_crop}
                </div>

                <div class="result-scientific">
                    {crop_meta["scientific"]}
                </div>

                <div>
                    Raw crop confidence:
                    <strong>
                        {detected_crop_confidence:.2f}%
                    </strong>
                </div>

            </div>
            """
        )

        st.caption(
            "Confirm the crop before disease screening. "
            "Correct it if the AI crop suggestion is wrong."
        )

        if detected_crop in SUPPORTED_CROPS:
            crop_index = SUPPORTED_CROPS.index(detected_crop)
        else:
            crop_index = 0

        selected_crop = st.selectbox(
            "Confirm or correct crop",
            SUPPORTED_CROPS,
            index=crop_index,
        )

        if selected_crop != detected_crop:
            st.info(
                f"Human-in-the-loop correction: "
                f"AI suggested **{detected_crop}**, "
                f"you selected **{selected_crop}**."
            )

        if st.button(
            "🍄 Step 2 — Analyze Fungal Condition",
            type="primary",
            use_container_width=True,
        ):

            with st.spinner(
                f"Screening {selected_crop} foliage "
                f"for fungal disease patterns..."
            ):

                result = predict_leaf(
                    image,
                    forced_crop=selected_crop,
                )

            st.session_state.final_result = result

            history_item = {
                "crop": result["crop"],
                "condition": result["condition"],
                "confidence": result["confidence"],
            }

            st.session_state.scan_history.insert(
                0,
                history_item,
            )

            st.session_state.scan_history = (
                st.session_state.scan_history[:5]
            )


    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    if (
        image is not None
        and st.session_state.final_result is not None
    ):

        result = st.session_state.final_result

        crop = result["crop"]
        condition = result["condition"]
        confidence = result["confidence"]
        confidence_level = result["confidence_level"]

        crop_confidence = result.get(
            "crop_confidence",
            0,
        )

        condition_confidence = result.get(
            "condition_confidence",
            confidence,
        )

        crop_meta = CROP_INFO.get(
            crop,
            {
                "scientific": "Unknown",
                "icon": "🌱",
            },
        )

        disease_info = get_disease_info(
    condition,
    crop
)

        if confidence_level == "High":
            confidence_class = "confidence-high"
            confidence_icon = "🟢"

        elif confidence_level == "Moderate":
            confidence_class = "confidence-moderate"
            confidence_icon = "🟡"

        else:
            confidence_class = "confidence-low"
            confidence_icon = "🔴"

        if condition.lower() == "healthy":

            disease_scientific = "No fungal pathogen detected"
            disease_category = "Healthy Foliar Baseline"

        elif disease_info:

            disease_scientific = disease_info.get(
                "scientific_name",
                "Not available",
            )

            disease_category = disease_info.get(
                "category",
                "Fungal Condition",
            )

        else:

            disease_scientific = "Reference profile pending"
            disease_category = "Fungal Condition"

        render_html(
            f"""
            <div class="result-card">

                <div class="result-label">
                    Final screening result
                </div>

                <div class="result-main">
                    {crop_meta["icon"]} {crop}
                </div>

                <div class="result-scientific">
                    {crop_meta["scientific"]}
                </div>

                <hr style="
                    border:none;
                    border-top:1px solid var(--border);
                    margin:18px 0;
                ">

                <div class="result-label">
                    Foliar condition
                </div>

                <div class="result-main">
                    {"🌱" if condition.lower() == "healthy" else "🍄"}
                    {condition}
                </div>

                <div class="result-scientific">
                    {disease_scientific}
                </div>

                <div style="margin-top:12px;">
                    <strong>{disease_category}</strong>
                </div>

                <div style="margin-top:15px;"
                     class="{confidence_class}">

                    {confidence_icon}
                    {confidence_level} confidence —
                    {confidence:.2f}%

                </div>

            </div>
            """
        )

        st.progress(
            min(
                max(confidence / 100, 0.0),
                1.0,
            )
        )

        metric1, metric2 = st.columns(2)

        metric1.metric(
            "Crop evidence",
            f"{crop_confidence:.1f}%",
        )

        metric2.metric(
            "Condition confidence",
            f"{condition_confidence:.1f}%",
        )

        if confidence < 60:

            st.warning(
                "⚠️ Low-confidence screening. "
                "Retake the image with one leaf filling most "
                "of the frame and use natural, even lighting."
            )

        elif confidence < 80:

            st.info(
                "ℹ️ Moderate-confidence screening. "
                "Consider a second image before drawing conclusions."
            )

        else:

            st.success(
                "✅ Strong visual match within the confirmed crop."
            )
        
        with st.expander("🧠 Why can AI results vary?"):
            st.write(
        "Fungal diseases can produce visually similar foliar symptoms. "
        "Lighting, background, leaf angle, disease stage and image quality "
        "can also affect prediction. FungiScan therefore combines AI screening "
        "with crop confirmation and confidence reporting."
    )
            

        # ----------------------------------------------------
        # DIFFERENTIAL PREDICTIONS
        # ----------------------------------------------------

        with st.expander(
            "🔎 View differential predictions",
            expanded=False,
        ):

            for rank, prediction in enumerate(
                result["top_predictions"],
                start=1,
            ):

                st.write(
                    f"**{rank}. "
                    f"{prediction['crop']} — "
                    f"{prediction['condition']}** "
                    f"— {prediction['confidence']:.2f}%"
                )


        # ----------------------------------------------------
        # PATHOLOGY INFORMATION
        # ----------------------------------------------------

        if disease_info:

            st.markdown("### 🔍 Characteristic symptoms")

            for symptom in disease_info.get(
                "symptoms",
                [],
            ):
                st.markdown(f"- {symptom}")

            st.markdown("### 🛡️ Prevention")

            for prevention in disease_info.get(
                "prevention",
                [],
            ):
                st.markdown(f"- {prevention}")

            st.markdown("### 💊 Management")

            st.info(
                disease_info.get(
                    "treatment",
                    "No management information available.",
                )
            )

            urgency = disease_info.get(
                "urgency",
                "Not specified",
            )

            st.caption(
                f"Reference urgency: {urgency}"
            )


        # ----------------------------------------------------
        # NEW SCAN
        # ----------------------------------------------------

        if st.button(
            "🔄 Scan Another Leaf",
            use_container_width=True,
        ):
            reset_scan()
            st.session_state.last_image_key = None
            st.rerun()


    # --------------------------------------------------------
    # SCAN HISTORY
    # --------------------------------------------------------

    if st.session_state.scan_history:

        st.markdown("### 🕘 Recent scans")

        for scan in st.session_state.scan_history:

            st.write(
                f"🌿 **{scan['crop']}** — "
                f"{scan['condition']} "
                f"({scan['confidence']:.1f}%)"
            )


# ============================================================
# PAGE 3 — DISEASE GUIDE
# ============================================================

elif st.session_state.active_tab == "Guide":

    st.markdown("## 📖 Fungal Disease Guide")

    st.caption(
        "Botanical reference profiles used to support "
        "FungiScan screening results."
    )

    search = st.text_input(
        "🔎 Search disease or host plant",
        placeholder="Example: blight, tomato, rust...",
    )

    combined_guide = {}

    for disease_name, details in DISEASE_KNOWLEDGE.items():
        combined_guide[disease_name] = details

    for disease_name, details in EXTRA_DISEASE_INFO.items():
        if disease_name not in combined_guide:
            combined_guide[disease_name] = details


    visible_count = 0

    for disease_name, details in combined_guide.items():

        searchable = (
            disease_name
            + " "
            + details.get("scientific_name", "")
            + " "
            + details.get("species", "")
        ).lower()

        if search and search.lower() not in searchable:
            continue

        visible_count += 1

        with st.expander(
            f"🍄 {disease_name} — "
            f"{details.get('scientific_name', 'Unknown pathogen')}"
        ):

            st.write(
                f"**Category:** "
                f"{details.get('category', 'Fungal Condition')}"
            )

            if "species" in details:
                st.write(
                    f"**Host plants:** {details['species']}"
                )

            st.write(
                f"**Urgency:** "
                f"{details.get('urgency', 'Not specified')}"
            )

            st.markdown("**Symptoms**")

            for symptom in details.get("symptoms", []):
                st.markdown(f"- {symptom}")

            st.markdown("**Prevention**")

            for prevention in details.get("prevention", []):
                st.markdown(f"- {prevention}")

            st.markdown("**Management**")

            st.write(
                details.get(
                    "treatment",
                    "Management information unavailable.",
                )
            )

    if visible_count == 0:
        st.warning(
            "No disease profile matched your search."
        )


# ============================================================
# PAGE 4 — RESEARCH DASHBOARD
# ============================================================

elif st.session_state.active_tab == "Research":

    st.markdown("## 📊 Research & Model Dashboard")

    st.caption(
        "Actual metrics recorded during FungiScan development."
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "PlantVillage Validation",
        "94.13%",
    )

    col2.metric(
        "Fine-tuned Validation",
        "93.44%",
    )

    col3, col4 = st.columns(2)

    col3.metric(
        "External PlantDoc",
        "52.48%",
        delta="+23.40 pts",
    )

    col4.metric(
        "External Test Images",
        "141",
    )

    col5, col6 = st.columns(2)

    col5.metric(
        "Training Images",
        "25,692",
    )

    col6.metric(
        "Model Classes",
        "24",
    )

    render_html(
        """
        <div class="section-card">
            <div class="result-label">
                Model architecture
            </div>

            <h3 style="margin-bottom:8px;">
                MobileNetV2 Transfer Learning
            </h3>

            <div style="color:var(--muted); line-height:1.7;">
                The first model was trained using a fungal-only
                subset of PlantVillage. A second fine-tuning stage
                added PlantDoc training images and unlocked the
                upper MobileNetV2 layers using a low learning rate
                to improve real-world image robustness.
            </div>
        </div>
        """
    )

    st.markdown("### Training progression")

    st.write(
        "**Initial fungal dataset:** "
        "24,261 PlantVillage images"
    )

    st.write(
        "**PlantDoc training images added:** "
        "1,431"
    )

    st.write(
        "**Fine-tuning dataset:** "
        "25,692 total images"
    )

    st.write(
        "**Independent PlantDoc external test:** "
        "141 images"
    )

    st.markdown("### External performance improvement")

    st.write(
        "Original model: **29.08%** "
        "on the independent PlantDoc test subset."
    )

    st.write(
        "Fine-tuned model: **52.48%** "
        "on the same external subset."
    )

    st.success(
        "Fine-tuning improved external accuracy "
        "by 23.40 percentage points."
    )

    st.markdown("### Current limitations")

    st.markdown(
        """
        - Crop identification can still be unreliable on photographs
          that differ substantially from the training datasets.
        - Fungal symptoms can visually overlap between diseases.
        - External performance is lower than controlled-dataset
          validation performance.
        - The application therefore uses **human-in-the-loop crop
          confirmation** before final disease screening.
        """
    )

    st.markdown("### Supported crop groups")

    render_html(
        """
        <div style="text-align:left;">
            <span class="tag">Apple</span>
            <span class="tag">Cherry</span>
            <span class="tag">Corn</span>
            <span class="tag">Grape</span>
            <span class="tag">Potato</span>
            <span class="tag">Squash</span>
            <span class="tag">Strawberry</span>
            <span class="tag">Tomato</span>
        </div>
        """
    )

    render_html(
        """
        <div class="footer-note">
            FungiScan AI is a student research prototype
            combining botany, plant pathology and data science.
            Validation accuracy should not be interpreted as
            universal field-diagnostic accuracy.
        </div>
        """
    )