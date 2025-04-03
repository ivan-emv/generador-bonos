import streamlit as st
from datetime import datetime
from docx import Document
import re
import tempfile

# Función para validar el formato de la fecha
def validar_fecha(fecha):
    regex = r'^\d{2}/\d{2}/\d{4}$'
    if re.match(regex, fecha):
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    return False

# Función para generar el bono Word sin corromper el archivo
def generar_bono_word(datos):
    doc_path = "bono.docx"
    doc = Document(doc_path)

    for paragraph in doc.paragraphs:
        if "(NUMEROREFERENCIA)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(NUMEROREFERENCIA)", datos['numero_referencia'])
        if "(FECHA)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(FECHA)", datos['fecha'])
        if "(INSERTEA)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(INSERTEA)", datos['dirigido_a'])
        if "(INSERTENOMBRE)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(INSERTENOMBRE)", datos['nombre'])
        if "(INSERTENUMEROPERSONAS)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(INSERTENUMEROPERSONAS)", str(datos['numero_personas']))
        if "(FECHA1)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(FECHA1)", datos['fecha1'])
        if "(SERVICIOS1)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(SERVICIOS1)", datos['servicios1'])
        if "(FECHA2)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(FECHA2)", datos['fecha2'] if datos['fecha2'] else "")
        if "(SERVICIOS2)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(SERVICIOS2)", datos['servicios2'] if datos['servicios2'] else "")
        if "(FECHA3)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(FECHA3)", datos['fecha3'] if datos['fecha3'] else "")
        if "(SERVICIOS3)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(SERVICIOS3)", datos['servicios3'] if datos['servicios3'] else "")
        if "(OBSERVACIONES)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(OBSERVACIONES)", datos['observaciones'])

    # Guardar en archivo temporal de forma segura
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp_path = tmp.name
    doc.save(tmp_path)
    return tmp_path

# Aplicación principal
def app():
    st.title("Generador de Bonos de Incidencias")

    # Información general
    fecha = st.text_input("Fecha de emisión del Bono (DD/MM/AAAA)")
    if fecha and not validar_fecha(fecha):
        st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")

    numero_referencia = st.text_input("Número de Referencia")
    dirigido_a = st.text_input("Dirigido A")
    nombre = st.text_input("Nombre")
    numero_personas = st.number_input("Número de Personas", min_value=1)

    # Primer acontecimiento
    fecha1 = st.text_input("Fecha 1 (DD/MM/AAAA)")
    if fecha1 and not validar_fecha(fecha1):
        st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")
    servicios1 = st.text_area("Servicios 1")

    # Variables para eventos adicionales
    fecha2 = servicios2 = fecha3 = servicios3 = ""

    # Segundo acontecimiento
    if st.checkbox("Cargar Fecha 2"):
        fecha2 = st.text_input("Fecha 2 (DD/MM/AAAA)")
        if fecha2 and not validar_fecha(fecha2):
            st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")
        servicios2 = st.text_area("Servicios 2")

    # Tercer acontecimiento
    if st.checkbox("Cargar Fecha 3"):
        fecha3 = st.text_input("Fecha 3 (DD/MM/AAAA)")
        if fecha3 and not validar_fecha(fecha3):
            st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")
        servicios3 = st.text_area("Servicios 3")

    # Observaciones
    observaciones = st.text_area("Observaciones")

    # Generar bono
    if st.button("Generar Bono"):
        if not all([fecha, fecha1, numero_referencia, nombre]) or \
           not validar_fecha(fecha) or not validar_fecha(fecha1):
            st.error("Completa los campos obligatorios y asegúrate del formato de fechas.")
            return

        datos = {
            "fecha": fecha,
            "numero_referencia": numero_referencia,
            "dirigido_a": dirigido_a,
            "nombre": nombre,
            "numero_personas": numero_personas,
            "fecha1": fecha1,
            "servicios1": servicios1,
            "fecha2": fecha2,
            "servicios2": servicios2,
            "fecha3": fecha3,
            "servicios3": servicios3,
            "observaciones": observaciones
        }

        path = generar_bono_word(datos)
        st.success("¡Bono generado correctamente!")
        st.download_button("Descargar Bono como Word", path, file_name="bono_generado.docx")

if __name__ == "__main__":
    app()
