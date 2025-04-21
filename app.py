import streamlit as st
from datetime import datetime

# Título
st.title("Evaluación para Tamizaje de Cáncer de Pulmón (LATAM)")
st.markdown("Esta herramienta está basada en criterios del consenso latinoamericano (Respirar 2024) y recoge factores adicionales de riesgo para apoyar la evaluación clínica.")

# Sección: Datos personales
st.header("1. Datos personales")
dob = st.date_input("Fecha de nacimiento", value=None, min_value=datetime(1900, 1, 1), max_value=datetime.today(), help="Selecciona tu fecha de nacimiento para calcular la edad actual.")
sexo = st.radio("Sexo biológico asignado al nacer (dato estadístico, no afecta la recomendación):", ["Femenino", "Masculino"], help="Esta información es solo para fines estadísticos.")

# Peso y talla
altura_str = st.text_input("¿Cuál es tu talla (cm)?", placeholder="Ejemplo: 165", help="Ingresa tu altura en centímetros para calcular tu IMC.")
peso_str = st.text_input("¿Cuál es tu peso actual (kg)?", placeholder="Ejemplo: 70", help="Ingresa tu peso en kilogramos para calcular tu IMC.")

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
fuma_actualmente = st.radio("¿Fumas actualmente?", ["Sí", "No"], help="Se refiere a si actualmente consumes cigarrillos u otros productos de tabaco.")
fumador_anterior = st.radio("¿Has fumado anteriormente al menos un cigarrillo al día durante un año o más?", ["Sí", "No"], help="Esto ayuda a calcular tu exposición acumulada al tabaco.")

pack_years = 0
if fuma_actualmente == "Sí" or fumador_anterior == "Sí":
    pack_years = st.number_input("¿Cuántos paquetes por año has consumido? (1 paquete = 20 cigarrillos/día por 1 año)", min_value=0, value=0, help="Un paquete/año equivale a fumar un paquete al día durante un año.")

anios_cessacion = 0
if fuma_actualmente == "No" and fumador_anterior == "Sí":
    anios_cessacion = st.number_input("¿Cuántos años hace que dejaste de fumar?", min_value=0, value=0, help="Esta información es necesaria para determinar si calificás para tamizaje según el tiempo desde que dejaste de fumar.")

# Sección: Exposición y comorbilidades
st.header("3. Exposición y condiciones clínicas")
biomasa = st.checkbox("¿Has estado expuesto(a) con frecuencia al humo de leña, carbón u otra biomasa en tu casa?", help="Incluye exposición constante en ambientes interiores, como cocinar con leña sin ventilación adecuada.")
ocupacional = st.checkbox("¿Has trabajado con exposición a sustancias como asbesto, sílice u otros agentes cancerígenos?", help="Esto puede incluir trabajos en minería, construcción o industrias químicas.")
familiar = st.checkbox("¿Tienes familiares cercanos con diagnóstico de cáncer de pulmón?", help="Aplica para padres, hermanos o hijos diagnosticados con cáncer de pulmón.")
copd = st.checkbox("¿Tienes diagnóstico de EPOC, enfisema u otra enfermedad pulmonar crónica?", help="Enfermedades respiratorias crónicas pueden aumentar tu riesgo de desarrollar cáncer de pulmón.")
cancer_previo = st.checkbox("¿Has tenido algún otro tipo de cáncer en el pasado?", help="Ciertos cánceres previos pueden estar asociados con un mayor riesgo de cáncer de pulmón.")

# Sección: Síntomas
sintomas = st.checkbox("¿Tenés sangrado por recto, cambios en el ritmo intestinal o pérdida de peso sin explicación?", help="Este síntoma no forma parte del tamizaje pulmonar, pero puede indicar otros problemas de salud relevantes.")

# Evaluación de elegibilidad para LDCT
st.header("Resultado de la evaluación")
eligible = False
if edad and 50 <= edad <= 74:
    if (fuma_actualmente == "Sí" or fumador_anterior == "Sí") and pack_years >= 30:
        if fuma_actualmente == "Sí" or anios_cessacion <= 15:
            eligible = True
            st.success("**Cumples con los criterios para tamizaje con Tomografía de Baja Dosis (LDCT)**")
            st.markdown("Recomendación: Realizar una tomografía de baja dosis una vez al año, de acuerdo al consenso latinoamericano.")

# Si no es elegible pero tiene factores
if not eligible:
    st.warning("**No cumples con los criterios tradicionales de tamizaje. Consulta con tu médico.**")
    if biomasa or ocupacional or familiar or copd or cancer_previo:
        st.markdown("### ⚠️ Se detectaron factores de riesgo adicionales:")
        if biomasa:
            st.markdown("- Exposición a biomasa (leña, carbón, etc.)")
        if ocupacional:
            st.markdown("- Exposición ocupacional a sustancias cancerígenas")
        if familiar:
            st.markdown("- Antecedente familiar de cáncer de pulmón")
        if copd:
            st.markdown("- Enfermedad pulmonar crónica (EPOC, enfisema, etc.)")
        if cancer_previo:
            st.markdown("- Antecedente de otro tipo de cáncer")
        st.markdown("**🔎 Nota para profesionales de salud:** Los siguientes factores fueron identificados como relevantes para evaluación individualizada en consenso clínico, aunque no forman parte de los criterios estándar de tamizaje. Su presencia puede justificar discusión médica caso por caso.")
        st.info("Actualmente no existen guías validadas para tamizaje con estos factores. Te recomendamos consultar con tu médico para una evaluación más detallada.")
    else:
        st.markdown("No se identificaron factores adicionales de riesgo.")

# Aviso final
disclaimer = """
---
**Aviso:** Esta herramienta tiene fines educativos. No reemplaza la consulta médica ni constituye una recomendación personalizada. Las decisiones deben ser tomadas junto con un profesional de salud.
"""
st.markdown(disclaimer)
