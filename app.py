import streamlit as st
from datetime import datetime
from docxtpl import DocxTemplate
import re
import tempfile
import os

# Validar formato de fecha DD/MM/AAAA
def validar_fecha(fecha):
    pattern = r'^\d{2}/\d{2}/\d{4}$'
    if re.match(pattern, fecha):
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    return False

# Generar bono con docxtpl
def generar_bono_docx(contexto):
    tpl = DocxTemplate("bono_tpl.docx")
    tpl.render(contexto)

    tmp_path = os.path.join(tempfile.gettempdir(), "bono_generado.docx")
    tpl.save(tmp_path)
    return tmp_path

# Interfaz Streamlit
def app():
    st.title("Generador de Bonos de Incidencias")

    # Datos principales
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

    # Segundo y tercer acontecimiento (opcionales)
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

    # Botón para generar
    if st.button("Generar Bono"):
        if not all([fecha, fecha1, numero_referencia, nombre]) or \
           not validar_fecha(fecha) or not validar_fecha(fecha1):
            st.error("Por favor, completa los campos obligatorios y verifica el formato de fechas.")
            return

        contexto = {
            "FECHA": fecha,
            "NUMEROREFERENCIA": numero_referencia,
            "INSERTEA": dirigido_a,
            "INSERTENOMBRE": nombre,
            "INSERTENUMEROPERSONAS": numero_personas,
            "FECHA1": fecha1,
            "SERVICIOS1": servicios1,
            "FECHA2": fecha2,
            "SERVICIOS2": servicios2,
            "FECHA3": fecha3,
            "SERVICIOS3": servicios3,
            "OBSERVACIONES": observaciones
        }

        output_path = generar_bono_docx(contexto)
        st.success("¡Bono generado correctamente!")
        st.download_button("Descargar Bono como Word", output_path, file_name="bono_generado.docx")

if __name__ == "__main__":
    app()
