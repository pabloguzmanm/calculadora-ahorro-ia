
# Instrucciones para incorporar la Calculadora de Ahorro con IA en WordPress

Esta calculadora está construida con **Streamlit** y permite estimar ahorro de tiempo y dinero al automatizar tareas con IA. Se ejecuta como app web y puede integrarse en WordPress de las siguientes formas:

---

## Opción 1: Incrustar vía iframe (con Streamlit Cloud o servidor propio)

1. Despliega la app en [Streamlit Cloud](https://streamlit.io/cloud) o en un servidor propio.
2. Copia el link público generado.
3. En WordPress, crea una nueva página o entrada.
4. Usa el bloque **HTML personalizado** y pega el siguiente código:

```html
<iframe src="TU_LINK_DE_STREAMLIT" width="100%" height="900px" frameborder="0"></iframe>
```

---

## Opción 2: Vincular como botón o banner

1. Puedes subir el archivo `portada_calculadora.png` como imagen destacada.
2. Crea un botón en WordPress con enlace directo al despliegue de la app.

---

## Opción 3: Plugin de iFrame avanzado

1. Instala un plugin como “Advanced iFrame”.
2. Configura el plugin con el enlace de la app y define el alto, ancho, scroll y estilos deseados.

---

## Envío automático por correo

La aplicación incluye envío automático por correo mediante SMTP. Edita el archivo `app.py` para incluir tus credenciales SMTP:

```python
EMAIL = "tu_correo@gmail.com"
PASSWORD = "tu_contraseña"
```

**IMPORTANTE:** Usa contraseñas de aplicaciones si usas Gmail con 2FA.

---

## Archivos incluidos

- `app.py`: Código principal con funcionalidad de envío.
- `Matriz_Tareas_Empresa_Ventas_IA.xlsx`: Base de tareas.
- `requirements.txt`: Dependencias.
- `portada_calculadora.png`: Imagen de fondo.
- `README.md`: Este documento.

---

## Requisitos

- Python 3.8+
- Librerías: streamlit, pandas, matplotlib, openpyxl, fpdf, smtplib, email

---

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

MIT © 2025 Dubist.io
