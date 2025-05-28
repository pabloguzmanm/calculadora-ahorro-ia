    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/gif;base64,{encoded_gif}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }}

    /* Etiquetas (labels) */
    label, .stSelectbox label, .stSlider label, .stTextInput label {{
        font-weight: bold !important;
        font-size: 130% !important;
        color: white !important;
    }}

    /* Entradas: inputs, selectbox, multiselect, slider */
    .stTextInput > div > input,
    .stNumberInput input,
    .stSelectbox > div,
    .stMultiselect > div,
    .stSlider > div,
    .stTextArea > div > textarea {{
        background-color: rgba(0, 0, 0, 0.15) !important;
        color: white !important;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 6px;
    }}

    /* Botón */
    .stButton > button {{
        background-color: rgba(255, 255, 255, 0.15);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid white;
    }}
    </style>
    """, unsafe_allow_html=True)

