import streamlit as st

def apply_custom_styles() -> None:
    """
    Injects custom CSS to give Streamlit a modern AI SaaS design.
    Features: Rounded cards, sleek shadows, modern fonts, custom sidebar styling,
    and responsive medical-themed UI components.
    """
    custom_css = """
    <style>
        /* Import Modern Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #F8FAFC;
            color: #0F172A;
        }

        /* Hide Streamlit default header/footer elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Main Container Padding */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }

        /* Metric Card Container Styling */
        .stat-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease-in-out;
        }
        .stat-card:hover {
            box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.08);
            border-color: #CBD5E1;
        }
        .stat-title {
            font-size: 13px;
            font-weight: 600;
            color: #64748B;
            margin-bottom: 6px;
        }
        .stat-value {
            font-size: 28px;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.2;
        }
        .stat-[#10B981] {
            color: #10B981;
            font-size: 12px;
            font-weight: 700;
        }

        /* Banner Cards */
        .banner-blue {
            background: linear-gradient(135deg, #0055D4 0%, #0044AB 100%);
            color: #FFFFFF;
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 85, 212, 0.25);
        }
        .banner-teal {
            background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%);
            color: #FFFFFF;
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 10px 25px -5px rgba(13, 148, 136, 0.25);
        }

        /* Medical Paper Sheet Document Viewer */
        .document-paper {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
        }

        /* Status Badge Pills */
        .badge-success {
            background-color: #ECFDF5;
            color: #047857;
            border: 1px solid #A7F3D0;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 700;
        }
        .badge-warning {
            background-color: #FEF3C7;
            color: #B45309;
            border: 1px solid #FDE68A;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 700;
        }
        .badge-danger {
            background-color: #FFE4E6;
            color: #BE123C;
            border: 1px solid #FECDD3;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 700;
        }

        /* Primary Custom Button Override */
        .stButton>button {
            border-radius: 12px;
            font-weight: 700;
            font-size: 14px;
            padding: 10px 20px;
            background-color: #0055D4;
            color: #FFFFFF;
            border: none;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #0044AB;
            box-shadow: 0 4px 12px rgba(0, 85, 212, 0.3);
            color: #FFFFFF;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
