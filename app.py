""import streamlit as st
from datetime import datetime

# Título
st.title("Evaluación para Tamizaje de Cáncer de Pulmón (LATAM)")
st.markdown("Esta herramienta está basada en criterios del consenso latinoamericano y recoge factores adicionales de riesgo para apoyar la evaluación clínica.")

# Sección: Datos personales
st.header("1. Datos personales")
dob = st.date_input("Fecha de nacimiento", value=None, min_value=datetime(1900, 1, 1), max_value=datetime.today())
sexo = st.radio("Sexo biológico asignado al nacer (dato estadístico, no afecta la recomendación):", ["Femenino", "Masculino"])

# Calcular edad
today = datetime.today()
edad = None
if dob:
    edad = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    st.markdown(f"**Edad:** {edad} años")

# Peso y talla
altura_str = st.text_input("¿Cuál es tu talla (cm)?", placeholder="Ejemplo: 165")
peso_str = st.text_input("¿Cuál es tu peso actual (kg)?", placeholder="Ejemplo: 70")

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
fuma_actualmente = st.radio("¿Fumas actualmente?", ["Sí", "No"], index=None)
fumador_anterior = ""
if fuma_actualmente == "Sí":
    st.markdown("🛈 Como fumas actualmente, se considera que también has fumado anteriormente.")
    fumador_anterior = "Sí"
else:
    fumador_anterior = st.radio("¿Has fumado anteriormente al menos un cigarrillo al día durante un año o más?", ["Sí", "No"], index=None)

pack_years = 0
if fuma_actualmente == "Sí" or fumador_anterior == "Sí":
    pack_years = st.number_input("¿Cuántos paquetes por año has consumido? (1 paquete = 20 cigarrillos/día por 1 año)", min_value=0, value=0)

anios_cessacion = 0
if fuma_actualmente == "No" and fumador_anterior == "Sí":
    anios_cessacion = st.number_input("¿Cuántos años hace que dejaste de fumar?", min_value=0, value=0)

# Sección: Exposición y comorbilidades
st.header("3. Exposición y condiciones clínicas")
comorbilidad_severa = st.checkbox("¿Tienes alguna condición médica grave que pueda afectar tu calidad de vida o dificultar la realización de estudios por imágenes?", help="En algunos casos, estas condiciones pueden impedir que el tamizaje sea útil o seguro. Esto debe evaluarse junto con tu equipo de salud.")
biomasa = st.checkbox("¿Has estado expuesto(a) con frecuencia al humo de leña, carbón u otra biomasa en tu casa?", help="El humo de biomasa ha sido asociado a riesgo incrementado de enfermedades pulmonares crónicas y cáncer.")
ocupacional = st.checkbox("¿Has trabajado con exposición a sustancias como asbesto, sílice u otros agentes cancerígenos?", help="Sustancias como el asbesto o la sílice son carcinógenos conocidos para pulmón.")
familiar = st.checkbox("¿Tienes familiares cercanos con diagnóstico de cáncer de pulmón?", help="Incluye padre, madre, hermanos/as, o hijos/as con diagnóstico de cáncer de pulmón. Este factor no forma parte de los criterios tradicionales pero ha sido considerado en modelos como PLCOm2012 como marcador de riesgo adicional.")
copd = st.checkbox("¿Tienes diagnóstico de EPOC, enfisema u otra enfermedad pulmonar crónica?", help="Estas condiciones respiratorias aumentan el riesgo de desarrollar cáncer pulmonar.")
cancer_previo = st.checkbox("¿Has tenido algún otro tipo de cáncer en el pasado?", help="Algunos cánceres previos pueden estar relacionados con un mayor riesgo de cáncer de pulmón.")

# Sección: Síntomas de alerta
sintomas_alerta = st.checkbox(
    "¿Tienes alguno de estos síntomas: tos persistente, dolor en el pecho, pérdida de peso sin explicación o sangre al toser?",
    help="Si presentas síntomas compatibles con cáncer de pulmón, se recomienda realizar estudios diagnósticos, no tamizaje."
)

if sintomas_alerta:
    st.warning("Presentas síntomas compatibles con cáncer de pulmón. Se recomienda consultar de inmediato a un profesional de salud para estudios diagnósticos.")

# Evaluación de elegibilidad para LDCT
st.header("Resultado de la evaluación")
eligible = False
if edad is not None and fuma_actualmente is not None and fumador_anterior is not None:
    if pack_years < 15:
        st.warning("No cumples con el mínimo de 15 paquetes/año de carga tabáquica requerido por los programas de tamizaje.")
    elif edad > 50 and edad <= 75:
        if (fuma_actualmente == "Sí" or fumador_anterior == "Sí") and pack_years >= 15:
            if fuma_actualmente == "Sí" or anios_cessacion <= 15:
                eligible = True
                st.success("**Cumples con los criterios mínimos de inclusión establecidos por las guías RESPIRAR LATAM.**")
                st.markdown("Recomendación: Realizar una tomografía de baja dosis una vez al año.")
                st.markdown("🔎 **Resumen:** Edad entre 51 y 75 años, carga tabáquica ≥ 15 paquetes/año y cesación hace menos de 15 años (si aplica).")

# Recomendación de cesación
if fuma_actualmente == "Sí":
    st.markdown("🛑 **Recomendación:** Además del tamizaje, considera participar en un programa de cesación de tabaco. Dejar de fumar es la intervención más efectiva para reducir el riesgo de cáncer de pulmón y otras enfermedades respiratorias.")

# Evaluación extendida o factores adicionales
if edad is not None and fuma_actualmente is not None and fumador_anterior is not None:
    if not eligible and pack_years >= 15:
        st.warning("**No cumples con todos los criterios de programas estandarizados. Consulta con tu médico.**")

        if biomasa or ocupacional or familiar or copd or cancer_previo:
            st.markdown("### ⚠️ Clasificación de riesgo")
            st.info("Presentas un riesgo elevado por mecanismos diferentes al tabaquismo. Estos factores pueden justificar una evaluación individualizada para considerar tamizaje con LDCT.")
            st.markdown("### 🔎 Factores de riesgo identificados:")
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
            st.markdown("### ✅ Próximos pasos sugeridos")
            st.info("Comparte esta evaluación con tu médico o centro de salud. Podrán ayudarte a definir si es necesario realizar una tomografía u otros estudios.")
        elif pack_years >= 15:
            st.markdown("No se identificaron factores adicionales de riesgo.")

if comorbilidad_severa:
    st.warning("Presentas una condición médica grave que podría limitar los beneficios del tamizaje. Según las recomendaciones RESPIRAR, estos casos deben ser evaluados cuidadosamente por tu equipo médico.")

# Fuente y descargo
st.caption("📚 Fuente: Recomendaciones RESPIRAR LATAM 2024. Lamot SB et al. Revista RESPIRAR, 2024; 16(1):39.")

st.markdown("""
---
**Aviso:** Esta herramienta tiene fines educativos. No reemplaza la consulta médica ni constituye una recomendación personalizada. Las decisiones deben ser tomadas junto con un profesional de salud.
""")
