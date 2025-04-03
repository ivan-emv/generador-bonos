import streamlit as st
from datetime import datetime
import os

# Función para generar el bono
def generar_bono(datos):
    bono_template = f"""
    Bono

    García de Paredes 55-1º / 28010 / Madrid
    CIF: B-81742421
    Tel: +34 91 758 92 00 / Fax: +34 91 548 74 33
    E-Mail:
    administración.proveedores@europamundo.com
    contratacion@europamundo.com
    gruposope@europamundo.com

    Nº de Referencia: {datos['numero_referencia']}
    FECHA: {datos['fecha']}

    A: {datos['dirigido_a']}
    Nombre: {datos['nombre']}   Nº de Personas: {datos['numero_personas']}

    FECHAS:
    {datos['fecha1']}
    {datos['fecha2']}
    {datos['fecha3']}

    SERVICIOS:
    {datos['servicios1']}
    {datos['servicios2']}
    {datos['servicios3']}

    OBSERVACIONES:
    {datos['observaciones']}
    
    FIRMA
    """

    return bono_template

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

        bono = generar_bono(datos)

        # Mostrar el bono generado
        st.text_area("Bono Generado", bono, height=300)

        # Opción para descargar el bono como archivo .txt
        if st.button("Descargar Bono"):
            path = "/mnt/data/bono_generado.txt"
            with open(path, "w") as f:
                f.write(bono)
            st.download_button("Descargar", path)

if __name__ == "__main__":
    app()
