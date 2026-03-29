import streamlit as st

st.set_page_config(page_title="Calculadora Nómina por Horas", page_icon="💰")

st.title("📊 Calculadora de Nómina Mensual (Cálculo por Horas)")
st.write("Ajusta los sueldos y cantidades de horas en la izquierda.")

# --- BARRA LATERAL (ENTRADAS) ---
st.sidebar.header("1. Salario Base y Fijos")
# Tomado de la imagen como base
sueldo_basico_pactado = st.sidebar.number_input("Sueldo Básico Pactado (30 días)", value=6138000, step=10000)
# Suponemos un mes laboral estándar de 240 horas para los cálculos legales
horas_mes = 240
valor_hora_ordinaria = sueldo_basico_pactado / horas_mes

bono_desempeno = st.sidebar.number_input("Bono de Desempeño", value=4369581, step=10000)
aux_alimentacion = st.sidebar.number_input("Auxilio Alimentación (S/P)", value=372200, step=10000)

st.sidebar.header("2. Cantidad de Horas (Recargos/Extras)")
st.sidebar.markdown(f"**Valor Hora Ordinaria:** `${valor_hora_ordinaria:,.2f}`")

# Ingreso de CANTIDADES (Horas), no de valores en pesos
# Los porcentajes son los estándar legales en Colombia
cant_dominical_fest_noct = st.sidebar.number_input("Cantidad Horas Dominical/Fest Nocturno (Factor 2.5)", value=10.50, step=0.5)
cant_recargo_nocturno = st.sidebar.number_input("Cantidad Horas Recargo Nocturno (Factor 0.35)", value=106.00, step=1.0)
cant_extras_diurnas = st.sidebar.number_input("Cantidad Horas Extras Diurnas (Factor 1.25)", value=0.50, step=0.1)
cant_extras_nocturnas = st.sidebar.number_input("Cantidad Horas Extras Nocturnas (Factor 1.75)", value=4.50, step=0.5)

st.sidebar.header("3. Deducciones Adicionales (Fijas)")
prepaga_colmedica = st.sidebar.number_input("Prepagada Colmedica", value=128057, step=1000)
iva_prepaga = st.sidebar.number_input("IVA Prepagada", value=6402, step=100)
retencion_fuente = st.sidebar.number_input("Retención en la Fuente", value=435000, step=10000)


# --- CÁLCULOS ---

# A. Cálculos de Recargos y Horas Extra (Valor Hora * Cantidad * Factor)
# Usamos factores estándar de la ley colombiana para aproximar los valores de tu imagen
valor_dominical_fest_noct = valor_hora_ordinaria * cant_dominical_fest_noct * 2.5
valor_recargo_nocturno = valor_hora_ordinaria * cant_recargo_nocturno * 0.35
valor_extras_diurnas = valor_hora_ordinaria * cant_extras_diurnas * 1.25
valor_extras_nocturnas = valor_hora_ordinaria * cant_extras_nocturnas * 1.75

# B. IBC (Ingreso Base de Cotización)
# Es el Sueldo Básico + todos los recargos y extras. Excluye bono no prestacional y auxilio.
ibc = sueldo_basico_pactado + valor_dominical_fest_noct + valor_recargo_nocturno + valor_extras_diurnas + valor_extras_nocturnas

# C. Deducciones de Ley (4% salud, 4% pensión)
desc_salud = ibc * 0.04
desc_pension = ibc * 0.04

# D. Fondo de Solidaridad Pensional
# Es una tabla progresiva. Para el nivel de ingresos de la imagen (~12M+), es el 1%.
porcentaje_solidaridad = 0.01 if ibc > (1300000 * 4) else 0 # 1300000 aprox smmlv
desc_solidaridad = ibc * porcentaje_solidaridad

# E. Totales
total_devengado = ibc + bono_desempeno + aux_alimentacion
total_deducido = desc_salud + desc_pension + desc_solidaridad + prepaga_colmedica + iva_prepaga + retencion_fuente
neto_a_pagar = total_devengado - total_deducido


# --- VISUALIZACIÓN ---
# Tarjetas de resumen
c1, c2, c3 = st.columns(3)
c1.metric("Total Devengado", f"${total_devengado:,.0f}")
c2.metric("Total Deducciones", f"-${total_deducido:,.0f}")
c3.metric("Neto a Recibir", f"${neto_a_pagar:,.0f}")

st.divider()

# Sección de resultados detallados
st.subheader("Simulación de Desprendible de Nómina")

# Usamos una tabla para que se parezca más a tu imagen
import pandas as pd

# Datos para la tabla detallada
datos_devengado = {
    "Descripción": ["Sueldo Básico (30 días)", "Dominical Fest Nocturno", "Bono de Desempeño", "Aux. Alimentación S/P", "Recargo Nocturno", "Hora Extra Diurna", "Hora Extra Nocturna"],
    "Cantidad": ["30.00", f"{cant_dominical_fest_noct:.2f}", "0.00", "30.00", f"{cant_recargo_nocturno:.2f}", f"{cant_extras_diurnas:.2f}", f"{cant_extras_nocturnas:.2f}"],
    "Valor": [sueldo_basico_pactado, valor_dominical_fest_noct, bono_desempeno, aux_alimentacion, valor_recargo_nocturno, valor_extras_diurnas, valor_extras_nocturnas]
}
df_devengado = pd.DataFrame(datos_devengado)

datos_deducciones = {
    "Descripción": ["Prepaga Colmedica", "IVA Prepagada", "Descuento Salud (4%)", "Descuento Pensión (4%)", "Descuento Solidaridad", "Retención en la Fuente"],
    "Valor": [prepaga_colmedica, iva_prepaga, desc_salud, desc_pension, desc_solidaridad, retencion_fuente]
}
df_deducciones = pd.DataFrame(datos_deducciones)

col_izq, col_der = st.columns(2)

with col_izq:
    st.markdown("**INGRESOS (Devengado)**")
    # Formatear la columna Valor como moneda
    df_devengado_show = df_devengado.copy()
    df_devengado_show["Valor"] = df_devengado_show["Valor"].apply(lambda x: f"${x:,.0f}")
    st.table(df_devengado_show)
    st.markdown(f"**Subtotal Devengado:** `${total_devengado:,.0f}`")

with col_der:
    st.markdown("**EGRESOS (Deducido)**")
    # Formatear la columna Valor como moneda
    df_deducciones_show = df_deducciones.copy()
    df_deducciones_show["Valor"] = df_deducciones_show["Valor"].apply(lambda x: f"${x:,.0f}")
    st.table(df_deducciones_show)
    st.markdown(f"**Subtotal Deducciones:** `${total_deducido:,.0f}`")

st.info(f"**Cálculos legales basados en IBC de:** `${ibc:,.0f}`")
st.success(f"### Neto a Pagar: **${neto_a_pagar:,.0f}**")
