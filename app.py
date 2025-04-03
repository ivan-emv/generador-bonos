import streamlit as st
from datetime import datetime
from docx import Document
import re  # Importar la librería para las expresiones regulares

# Función para generar el bono en formato Word (.docx)
def generar_bono_word(datos):
    # Crear un objeto Document a partir del archivo de Word original (bono.docx)
    doc = Document("bono.docx")  # Usamos el nombre correcto del archivo

    # Buscar y reemplazar los campos en el documento
    for paragraph in doc.paragraphs:
        if "(NUMEROREFERENCIA)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(NUMEROREFERENCIA)", datos['numero_referencia'])
        if "(FECHA)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(FECHA)", str(datos['fecha']))
        if "(INSERTEA)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(INSERTEA)", datos['dirigido_a'])
        if "(INSERTENOMBRE)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(INSERTENOMBRE)", datos['nombre'])
        if "(INSERTENUMEROPERSONAS)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(INSERTENUMEROPERSONAS)", str(datos['numero_personas']))
        if "(FECHA1)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(FECHA1)", str(datos['fecha1']))
        if "(SERVICIOS1)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(SERVICIOS1)", datos['servicios1'])
        if "(FECHA2)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(FECHA2)", str(datos['fecha2']) if datos['fecha2'] else "")
        if "(SERVICIOS2)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(SERVICIOS2)", datos['servicios2'] if datos['servicios2'] else "")
        if "(FECHA3)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(FECHA3)", str(datos['fecha3']) if datos['fecha3'] else "")
        if "(SERVICIOS3)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(SERVICIOS3)", datos['servicios3'] if datos['servicios3'] else "")
        if "(OBSERVACIONES)" in paragraph.text:
            paragraph.text = paragraph.text.replace("(OBSERVACIONES)", datos['observaciones'])

    # Guardar el documento modificado
    path = "/mnt/data/bono_generado.docx"
    doc.save(path)
    return path

# Función para validar el formato de la fecha
def validar_fecha(fecha):
    # Expresión regular para el formato DD/MM/YYYY
    regex = r'^\d{2}/\d{2}/\d{4}$'
    if re.match(regex, fecha):
        try:
            # Intentar convertir la fecha a un objeto datetime para verificar su validez
            datetime.strptime(fecha, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    return False

# Interfaz de la app
def app():
    st.title("Generador de Bonos de Incidencias")

    # Campos para información principal
    fecha = st.text_input("Fecha de emisión del Bono (DD/MM/YYYY)")
    if fecha and not validar_fecha(fecha):
        st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")

    numero_referencia = st.text_input("Número de Referencia")
    dirigido_a = st.text_input("Dirigido A")
    nombre = st.text_input("Nombre")
    numero_personas = st.number_input("Número de Personas", min_value=1)

    # Campos para los eventos (Acontecimientos)
    fecha1 = st.text_input("Fecha 1 (DD/MM/YYYY)")
    if fecha1 and not validar_fecha(fecha1):
        st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")
    
    servicios1 = st.text_area("Servicios 1")

    # Permitir añadir más eventos con botones con nombre único
    fecha2, servicios2, fecha3, servicios3 = None, None, None, None
    if st.button("Cargar Fecha 2", key="cargar_fecha_2"):
        fecha2 = st.text_input("Fecha 2 (DD/MM/YYYY)")
        if fecha2 and not validar_fecha(fecha2):
            st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")
        servicios2 = st.text_area("Servicios 2")
    
    if st.button("Cargar Fecha 3", key="cargar_fecha_3"):
        fecha3 = st.text_input("Fecha 3 (DD/MM/YYYY)")
        if fecha3 and not validar_fecha(fecha3):
            st.error("Error en la Fecha, recuerda que el formato es DD/MM/AAAA.")
        servicios3 = st.text_area("Servicios 3")

    # Campo de Observaciones
    observaciones = st.text_area("Observaciones")

    # Botón para generar el bono
    if st.button("Generar Bono"):
        # Crear el diccionario con los datos
        datos = {
            "fecha": fecha,
            "numero_referencia": numero_referencia,
            "dirigido_a": dirigido_a,
            "nombre": nombre,
            "numero_personas": numero_personas,
            "fecha1": fecha1,
            "servicios1": servicios1,
            "fecha2": fecha2 or "",
            "servicios2": servicios2 or "",
            "fecha3": fecha3 or "",
            "servicios3": servicios3 or "",
            "observaciones": observaciones
        }

        # Generar el archivo Word
        path = generar_bono_word(datos)

        # Opción para descargar el bono como archivo Word (.docx)
        st.download_button("Descargar Bono como Word", path)

if __name__ == "__main__":
    app()
