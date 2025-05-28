
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import base64

# ---------- ESTILO VISUAL Y FONDO ----------
def set_background_image(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    encoded_image = base64.b64encode(image_data).decode()
    st.markdown(f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_image}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }}
    label, .stSelectbox label, .stMultiselect label, .stSlider label, .stTextInput label {{
        font-weight: bold !important;
        font-size: 130% !important;
        color: white !important;
    }}
    .stTextInput > div > input,
    .stNumberInput input,
    .stSelectbox > div,
    .stMultiselect > div,
    .stSlider > div {{
        background-color: rgba(0, 0, 0, 0.15) !important;
        color: white !important;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 6px;
    }}
    .stButton > button {{
        background-color: rgba(255, 255, 255, 0.15);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: 1px solid white;
    }}
    </style>
    ''', unsafe_allow_html=True)

# Asume que tienes una imagen llamada 'fondo_moderno.jpg' en el mismo directorio
set_background_image("fondo_moderno.jpg")

# ---------- CONFIGURACIÓN DE CORREO ----------
EMAIL = "pablo@dubist.io"
PASSWORD = "@5zdY$0M7ntV"  # Usa contraseña de aplicación

# ---------- CARGA DE DATOS ----------
df = pd.read_excel("Matriz_Tareas_Empresa_Ventas_IA.xlsx")

# ---------- INTERFAZ DE USUARIO ----------
st.title("Calculadora de Ahorro con IA")

edad = st.selectbox("¿Cuál es tu rango de edad?", ["18-25", "26-35", "36-45", "46-60", "60+"])
funciones = st.multiselect("¿En qué funciones deseas automatizar?", ["Ventas", "Marketing", "Administración", "Atención al cliente", "Gestión de proyectos"])
tareas = st.multiselect("Selecciona tareas:", df["Tarea"].tolist())
frecuencia = st.slider("Frecuencia mensual de cada tarea:", 1, 60, 4)
costo_hora = st.number_input("Costo promedio por hora:", 0, 100000, 10000, step=1000)
email_usuario = st.text_input("Tu correo electrónico para recibir el resultado:")

# ---------- CÁLCULOS Y RESULTADOS ----------
if tareas and funciones and edad and email_usuario:
    df_sel = df[df["Tarea"].isin(tareas)].copy()
    df_sel["Total sin IA (hrs/mes)"] = (df_sel["Tiempo estimado sin IA (min/vez)"] * frecuencia) / 60
    df_sel["Total con IA (hrs/mes)"] = (df_sel["Tiempo estimado con IA (min/vez)"] * frecuencia) / 60
    df_sel["Horas ahorradas (mes)"] = df_sel["Total sin IA (hrs/mes)"] - df_sel["Total con IA (hrs/mes)"]
    df_sel["Ahorro monetario estimado"] = df_sel["Horas ahorradas (mes)"] * costo_hora

    st.dataframe(df_sel)

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Resumen de Ahorro con IA", ln=True)

    pdf.set_font("Arial", '', 12)
    for i, row in df_sel.iterrows():
        pdf.cell(0, 10, f"{row['Tarea']}: {row['Horas ahorradas (mes)']:.2f} hrs | ${int(row['Ahorro monetario estimado']):,} CLP", ln=True)

    mensaje = f"Hola, según tu perfil ({edad}) y enfoque en {' - '.join(funciones)}, te compartimos tu análisis de ahorro potencial."
    pdf.ln(10)
    pdf.multi_cell(0, 10, mensaje)

    pdf_file_path = "Resumen_Ahorro_IA.pdf"
    pdf.output(pdf_file_path)

    if st.button("Enviar resumen por correo a ti y a eduardo@dubist.io"):
        try:
            msg = EmailMessage()
            msg['Subject'] = "Resumen de Ahorro con IA"
            msg['From'] = EMAIL
            msg['To'] = [email_usuario, "eduardo@dubist.io"]
            msg.set_content(mensaje)

            with open(pdf_file_path, 'rb') as f:
                file_data = f.read()
                msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=pdf_file_path)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL, PASSWORD)
                smtp.send_message(msg)

            st.success("Correo enviado exitosamente.")
        except Exception as e:
            st.error(f"Error al enviar el correo: {e}")
