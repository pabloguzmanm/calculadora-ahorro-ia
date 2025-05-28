
import streamlit as st
import pandas as pd
import base64
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

# ---------- FONDO Y ESTILOS ----------
def set_background_image(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    encoded_image = base64.b64encode(image_data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_image}");
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }}

    label, .stSelectbox label, .stSlider label, .stTextInput label {{
        font-weight: bold;
        color: white;
    }}

    .stSelectbox, .stSlider, .stTextInput {{
        background-color: rgba(0, 0, 0, 0.4) !important;
        border-radius: 8px;
        padding: 8px;
    }}

    .stButton button {{
        background-color: rgba(255, 255, 255, 0.15);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        margin-right: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# Usa tu imagen oceánica aquí
set_background_image("WhatsApp Image 2025-05-28 at 12.46.11.jpeg")

# ---------- CONFIGURACIÓN ----------
EMAIL = "pablocorporativa@gmail.com"
PASSWORD = "F@ntomas21"  # Usa una contraseña de aplicación de Gmail

# ---------- CARGA DE DATOS ----------
df = pd.read_excel("Matriz_Tareas_Empresa_Ventas_IA.xlsx")

# ---------- INTERFAZ ----------
st.markdown("### <span style='color:white'>**Edad del usuario:**</span>", unsafe_allow_html=True)
edad = st.selectbox("", ["18-25", "26-35", "36-45", "46-60", "60+"])

st.markdown("### <span style='color:white'>Selecciona funciones principales:</span>", unsafe_allow_html=True)
funcion = st.selectbox("", ["Ventas", "Marketing", "Administración", "Atención al cliente", "Gestión de proyectos"])

st.markdown("### <span style='color:white'>Selecciona tareas que <strong>realizas frecuentemente</strong>:</span>", unsafe_allow_html=True)
tarea = st.selectbox("", df["Tarea"].tolist())

st.markdown("### <span style='color:white'>Frecuencia mensual de <strong>cada tarea seleccionada</strong>:</span>", unsafe_allow_html=True)
frecuencia = st.slider("", 1, 60, 4)

st.markdown("### <span style='color:white'>Costo promedio por hora (CLP):</span>", unsafe_allow_html=True)
costo_hora = st.number_input("", 0, 100000, 10000, step=1000)

st.markdown("### <span style='color:white'>Tu correo electrónico para recibir el resumen:</span>", unsafe_allow_html=True)
email_usuario = st.text_input("")

# ---------- LÓGICA Y RESULTADOS ----------
if st.button("Calcular"):
    if tarea and funcion and edad:
        df_sel = df[df["Tarea"] == tarea].copy()
        df_sel["Total sin IA (hrs/mes)"] = (df_sel["Tiempo estimado sin IA (min/vez)"] * frecuencia) / 60
        df_sel["Total con IA (hrs/mes)"] = (df_sel["Tiempo estimado con IA (min/vez)"] * frecuencia) / 60
        df_sel["Horas ahorradas (mes)"] = df_sel["Total sin IA (hrs/mes)"] - df_sel["Total con IA (hrs/mes)"]
        df_sel["Ahorro monetario estimado"] = df_sel["Horas ahorradas (mes)"] * costo_hora

        st.dataframe(df_sel)

        # ---------- CREAR PDF ----------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Resumen de Ahorro con IA", ln=True)

        pdf.set_font("Arial", '', 12)
        for i, row in df_sel.iterrows():
            pdf.cell(0, 10, f"{row['Tarea']}: {row['Horas ahorradas (mes)']:.2f} hrs | ${int(row['Ahorro monetario estimado']):,} CLP", ln=True)

        mensaje = f"Hola, según tu perfil ({edad}) y enfoque en {funcion}, te compartimos tu análisis de ahorro potencial."
        pdf.ln(10)
        pdf.multi_cell(0, 10, mensaje)

        pdf_file_path = "Resumen_Ahorro_IA.pdf"
        pdf.output(pdf_file_path)

        st.success("Resumen generado. Ahora puedes enviarlo por correo.")

        # ---------- ENVÍO DE CORREO ----------
        if st.button("Enviar por correo"):
            if email_usuario:
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
            else:
                st.warning("Por favor, ingresa tu correo antes de enviar.")
