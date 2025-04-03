import streamlit as st
from datetime import datetime
from docx import Document
import os

# Función para generar el bono en formato Word (.docx)
def generar_bono_word(datos):
    doc = Document()

    # Título del bono
    doc.add_heading('Bono', 0)

    # Información de contacto
    doc.add_paragraph("García de Paredes 55-1º / 28010 / Madrid\n"
                      "CIF: B-81742421\n"
                      "Tel: +34 91 758 92 00 / Fax: +34 91 548 74 33\n"
                      "E-Mail:\nadministración.proveedores@europamundo.com\n"
                      "contratacion@europamundo.com\ngruposope@europamundo.com\n")

    # Detalles del bono
    doc.add_paragraph(f"Nº de Referencia: {datos['numero_referencia']}")
    doc.add_paragraph(f"FECHA: {datos['fecha']}")
    doc.add_paragraph(f"A: {datos['dirigido_a']}")
    doc.add_paragraph(f"Nombre: {datos['nombre']}   Nº de Personas: {datos['numero_personas']}")
    doc.add_paragraph("FECHAS:")
    doc.add_paragraph(datos['fecha1'])
    doc.add_paragraph(datos['fecha2'] if datos['fecha2'] else "")
    doc.add_paragraph(datos['fecha3'] if datos['fecha3'] else "")
    doc.add_paragraph("SERVICIOS:")
    doc.add_paragraph(datos['servicios1'])
    doc.add_paragraph(datos['servicios2'] if datos['servicios2'] else "")
    doc.add_paragraph(datos['servicios3'] if datos['servicios3'] else "")
    doc.add_paragraph("OBSERVACIONES:")
    doc.add_paragraph(datos['observaciones'])

    # Firma
    doc.add_paragraph("FIRMA")

    # Guardar el documento
    path = "/mnt/data/bono_generado.docx"
    doc.save(path)
    return path

# Interfaz de la app
def app():
    st.title("Generador de Bonos de Incidencias")

    # Campos para información principal
    fecha = st.date_input("Fecha de emisión del Bono", datetime.today())
    numero_referencia = st.text_input("Número de Referencia")
    dirigido_a = st.text_input("Dirigido A")
    nombre = st.text_input("Nombre")
    numero_personas = st.number_input("Número de Personas", min_value=1)

    # Campos para los eventos (Acontecimientos)
    fecha1 = st.date_input("Fecha 1", datetime.today())
    servicios1 = st.text_area("Servicios 1")

    # Permitir añadir más eventos
    fecha2, servicios2, fecha3, servicios3 = None, None, None, None
    if st.button("Cargar Otro"):
        fecha2 = st.date_input("Fecha 2", datetime.today())
        servicios2 = st.text_area("Servicios 2")
    if st.button("Cargar Otro"):
        fecha3 = st.date_input("Fecha 3", datetime.today())
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
