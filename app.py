import streamlit as st
from datetime import datetime
from docx import Document
import re
import tempfile

# Validación de formato DD/MM/AAAA
def validar_fecha(fecha):
    regex = r'^\d{2}/\d{2}/\d{4}$'
    if re.match(regex, fecha):
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    return False

# Reemplazo robusto en párrafos y tablas, preservando estilos
def reemplazar_texto_en_runs(runs, marcador, valor):
    for run in runs:
        if marcador in run.text:
            run.text = run.text.replace(marcador, valor)

def reemplazar_en_documento(doc, marcador, valor):
    # Párrafos normales
    for paragraph in doc.paragraphs:
        reemplazar_texto_en_runs(paragraph.runs, marcador, valor)

    # Dentro de cada celda de tabla
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    reemplazar_texto_en_runs(paragraph.runs, marcador, valor)

# Generar el bono Word desde plantilla
def generar_bono_word(datos):
    doc = Document("bono_nuevo.docx")

    campos = {
        "(NUMEROREFERENCIA)": datos['numero_referencia'],
        "(FECHA)": datos['fecha'],
        "(INSERTEA)": datos['dirigido_a'],
        "(INSERTENOMBRE)": datos['nombre'],
        "(INSERTENUMEROPERSONAS)": str(datos['numero_personas']),
        "(FECHA1)": datos['fecha1'],
        "(SERVICIOS1)": datos['servicios1'],
        "(FECHA2)": datos['fecha2'] or "",
        "(SERVICIOS2)": datos['servicios2'] or "",
        "(FECHA3)": datos['fecha3'] or "",
        "(SERVICIOS3)": datos['servicios3'] or "",
        "(OBSERVACIONES)": datos['observaciones']
    }

    for marcador, valor in campos.items():
        reemplazar_en_documento(doc, marcador, valor)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp.name)
    return tmp.name

# Interfaz Streamlit
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
