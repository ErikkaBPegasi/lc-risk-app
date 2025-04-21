import streamlit as st
from datetime import datetime

# Título
st.title("Evaluación para Tamizaje de Cáncer de Pulmón (LATAM)")
st.markdown("Esta herramienta está basada en criterios del consenso latinoamericano (Respirar 2024) y recoge factores adicionales de riesgo para apoyar la evaluación clínica.")

# Sección: Datos personales
st.header("1. Datos personales")
dob = st.date_input("Fecha de nacimiento", value=None, min_value=datetime(1900, 1, 1), max_value=datetime.today())
sexo = st.radio("Sexo biológico asignado al nacer (dato estadístico, no afecta la recomendación):", ["Femenino", "Masculino"])

# Peso y talla
altura_str = st.text_input("¿Cuál es tu talla (cm)?", placeholder="Ejemplo: 165")
peso_str = st.text_input("¿Cuál es tu peso actual (kg)?", placeholder="Ejemplo: 70")

# Calcular edad
edad = None
if dob:
    hoy = datetime.today()
    edad = hoy.year - dob.year - ((hoy.month, hoy.day) < (dob.month, dob.day))
    st.markdown(f"**Edad:** {edad} años")

# Calcular IMC
imc = None
if altura_str and peso_str:
    try:
        altura_m = float(altura_str) / 100
        peso = float(peso_str)
        imc = round(peso / (altura_m ** 2), 1)
        st.markdown(f"**IMC:** {imc}")
        if imc >= 25:
            st.markdown(f"**Nota:** IMC elevado ({imc}): factor de riesgo adicional (no afecta la recomendación actual). El IMC saludable recomendado está entre 18.5 y 24.9.")
    except:
        st.error("Por favor, ingresa valores válidos para talla y peso.")

# Sección: Tabaquismo
st.header("2. Historial de consumo de tabaco")
fuma_actualmente = st.radio("¿Fumas actualmente?", ["Selecciona una opción", "Sí", "No"], index=0)
fumador_anterior = st.radio("¿Has fumado anteriormente al menos un cigarrillo al día durante un año o más?", ["Selecciona una opción", "Sí", "No"], index=0)

pack_years = 0
if fuma_actualmente in ["Sí"] or fumador_anterior in ["Sí"]:
    pack_years = st.number_input("¿Cuántos paquetes por año has consumido? (1 paquete = 20 cigarrillos/día por 1 año)", min_value=0, value=0)

anios_cessacion = 0
if fuma_actualmente == "No" and fumador_anterior == "Sí":
    anios_cessacion = st.number_input("¿Cuántos años hace que dejaste de fumar?", min_value=0, value=0)

# Sección: Exposición y comorbilidades
st.header("3. Exposición y condiciones clínicas")
biomasa = st.checkbox("¿Has estado expuesto(a) con frecuencia al humo de leña, carbón u otra biomasa en tu casa?", help="El humo de biomasa ha sido asociado a riesgo incrementado de enfermedades pulmonares crónicas y cáncer.")
ocupacional = st.checkbox("¿Has trabajado con exposición a sustancias como asbesto, sílice u otros agentes cancerígenos?", help="Sustancias como el asbesto o la sílice son carcinógenos conocidos para pulmón.")
familiar = st.checkbox("¿Tienes familiares cercanos con diagnóstico de cáncer de pulmón?", help="Incluye padre, madre, hermanos/as, o hijos/as con diagnóstico de cáncer de pulmón.")
copd = st.checkbox("¿Tienes diagnóstico de EPOC, enfisema u otra enfermedad pulmonar crónica?", help="Estas condiciones respiratorias aumentan el riesgo de desarrollar cáncer pulmonar.")
cancer_previo = st.checkbox("¿Has tenido algún otro tipo de cáncer en el pasado?", help="Algunos cánceres previos pueden estar relacionados con un mayor riesgo de cáncer de pulmón.")

# Sección: Síntomas
sintomas = st.checkbox("¿Tenés sangrado por recto, cambios en el ritmo intestinal o pérdida de peso sin explicación?", help="Estos síntomas no forman parte del tamizaje de pulmón pero pueden ser indicativos de otras patologías.")

# Evaluación de elegibilidad para LDCT
st.header("Resultado de la evaluación")
eligible = False
if edad and 50 <= edad <= 74:
    if (fuma_actualmente == "Sí" or fumador_anterior == "Sí") and pack_years >= 30:
        mensaje_adicional = ""
        if fuma_actualmente == "Sí" or anios_cessacion <= 15:
            eligible = True
            st.success("**Cumples con los criterios para tamizaje con Tomografía de Baja Dosis (LDCT)**")
            if 20 <= pack_years < 30:
                st.info("Como tienes un historial de tabaquismo de 20–29 paquetes/año, puedes ser elegible para tamizaje según recomendaciones ampliadas de las guías RESPIRAR LATAM. Deberías considerar hablar con tu médico sobre si el tamizaje con tomografía podría seguir siendo una buena opción para ti.")
            st.markdown("Recomendación: Realizar una tomografía de baja dosis una vez al año, de acuerdo al consenso latinoamericano.")

# Si no es elegible pero tiene factores
if not eligible:
    if 50 <= edad <= 74 and (fuma_actualmente == "Sí" or fumador_anterior == "Sí") and 20 <= pack_years < 30:
        st.info("Como tienes un historial de tabaquismo de 20–29 paquetes/año, puedes ser elegible para tamizaje según recomendaciones ampliadas de las guías RESPIRAR LATAM. Deberías considerar hablar con tu médico sobre si el tamizaje con tomografía podría seguir siendo una buena opción para ti.")
    st.warning("**No cumples con los criterios tradicionales de tamizaje. Consulta con tu médico.**")
    if biomasa or ocupacional or familiar or copd or cancer_previo:
        st.markdown("### ⚠️ Se detectaron factores de riesgo adicionales:")
        if biomasa:
            st.markdown("- Exposición a biomasa (leña, carbón, etc.)")
            st.info("Has reportado exposición frecuente a biomasa (como leña o carbón). Aunque no existen guías validadas para este riesgo, estudios indican una posible relación con enfermedades pulmonares. Consulta con tu médico para evaluar si se justifica tamizaje individualizado.")
        if ocupacional:
            st.markdown("- Exposición ocupacional a sustancias cancerígenas")
            st.info("Tu historial laboral incluye exposición a agentes cancerígenos conocidos. En estos casos, podría ser útil discutir con tu médico la posibilidad de estudios por imágenes aunque no se cumplan todos los criterios clásicos.")
        if familiar:
            st.markdown("- Antecedente familiar de cáncer de pulmón")
            st.info("Tener familiares con cáncer de pulmón puede aumentar tu riesgo. Aunque este factor no es parte de los criterios estándar de tamizaje, se recomienda discutirlo con tu médico.")
        if copd:
            st.markdown("- Enfermedad pulmonar crónica (EPOC, enfisema, etc.)")
            st.info("La EPOC y otras enfermedades pulmonares crónicas se asocian con mayor riesgo de cáncer de pulmón. Consulta con tu médico si puede ser apropiado realizar un control más frecuente.")
        if cancer_previo:
            st.markdown("- Antecedente de otro tipo de cáncer")
            st.info("Antecedentes personales de cáncer pueden ser relevantes al evaluar tu riesgo global. Considera hablar con tu médico para una evaluación individualizada.")
        st.markdown("**🔎 Nota para profesionales de salud:** Los factores seleccionados arriba fueron identificados como relevantes para evaluación individualizada en consenso clínico, aunque no forman parte de los criterios estándar de tamizaje. Su presencia puede justificar discusión médica caso por caso.")
        st.info("Actualmente no existen guías validadas para tamizaje con estos factores. Te recomendamos consultar con tu médico para una evaluación más detallada.")
    else:
        st.markdown("No se identificaron factores adicionales de riesgo.")

# Aviso final
disclaimer = """
---
**Aviso:** Esta herramienta tiene fines educativos. No reemplaza la consulta médica ni constituye una recomendación personalizada. Las decisiones deben ser tomadas junto con un profesional de salud.
"""
st.markdown(disclaimer)
