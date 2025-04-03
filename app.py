import streamlit as st
from datetime import datetime
from docx import Document
import re
import tempfile
import shutil

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

# Reemplazo en párrafos y en tablas
def reemplazar_texto(doc, marcador, valor):
    # Párrafos normales
    for paragraph in doc.paragraphs:
        if marcador in paragraph.text:
            paragraph.text = paragraph.text.replace(marcador, valor)

    # Dentro de tablas
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if marcador in cell.text:
                    cell.text = cell.text.replace(marcador, valor)

# Función para generar el bono Word sin corromperlo
def generar_bono_word(datos):
    doc_path = "bono.docx"
    doc = Document(doc_path)

    reemplazar_texto(doc, "(NUMEROREFERENCIA)", datos['numero_referencia'])
    reemplazar_texto(doc, "(FECHA)", datos['fecha'])
    reemplazar_texto(doc, "(INSERTEA)", datos['dirigido_a'])
    reemplazar_texto(doc, "(INSERTENOMBRE)", datos['nombre'])
    reemplazar_texto(doc, "(INSERTENUMEROPERSONAS)", str(datos['numero_personas']))
    reemplazar_texto(doc, "(FECHA1)", datos['fecha1'])
    reemplazar_texto(doc, "(SERVICIOS1)", datos['servicios1'])
    reemplazar_texto(doc, "(FECHA2)", datos['fecha2'] if datos['fecha2'] else "")
    reemplazar_texto(doc, "(SERVICIOS2)", datos['servicios2'] if datos['servicios2'] else "")
    reemplazar_texto(doc, "(FECHA3)", datos['fecha3'] if datos['fecha3'] else "")
    reemplazar_texto(doc, "(SERVICIOS3)", datos['servicios3'] if datos['servicios3'] else "")
    reemplazar_texto(doc, "(OBSERVACIONES)", datos['observaciones'])

    # Guardar de forma segura
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp_file.name)
    return tmp_file.name

# Aplicación principal
def app():
    st.title("Generador de Bonos de Incidencias")

    fecha = st.text_input("Fecha de emisión del Bono (DD/MM/AAAA)")
    if fecha and not validar_fecha(fecha):
        st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")

    numero_referencia = st.text_input("Número de Referencia")
    dirigido_a = st.text_input("Dirigido A")
    nombre = st.text_input("Nombre")
    numero_personas = st.number_input("Número de Personas", min_value=1)

    fecha1 = st.text_input("Fecha 1 (DD/MM/AAAA)")
    if fecha1 and not validar_fecha(fecha1):
        st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")
    servicios1 = st.text_area("Servicios 1")

    fecha2 = servicios2 = fecha3 = servicios3 = ""

    if st.checkbox("Cargar Fecha 2"):
        fecha2 = st.text_input("Fecha 2 (DD/MM/AAAA)")
        if fecha2 and not validar_fecha(fecha2):
            st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")
        servicios2 = st.text_area("Servicios 2")

    if st.checkbox("Cargar Fecha 3"):
        fecha3 = st.text_input("Fecha 3 (DD/MM/AAAA)")
        if fecha3 and not validar_fecha(fecha3):
            st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")
        servicios3 = st.text_area("Servicios 3")

    observaciones = st.text_area("Observaciones")

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
