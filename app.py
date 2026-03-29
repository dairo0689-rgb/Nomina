import streamlit as st

st.set_page_config(page_title="Calculadora de Nómina Personal", page_icon="💰")

st.title("📊 Calculadora de Nómina Mensual")
st.write("Ajusta los valores de la izquierda para calcular tu pago neto.")

# --- BARRA LATERAL (ENTRADAS) ---
st.sidebar.header("Configuración de Ingresos")

# Ingresos Fijos y Variables
sueldo_basico = st.sidebar.number_input("Sueldo Básico", value=6138000)
bono_desempeno = st.sidebar.number_input("Bono de Desempeño", value=4369581)
aux_alimentacion = st.sidebar.number_input("Auxilio Alimentación (S/P)", value=372200)

st.sidebar.header("Recargos y Horas Extra")
dominical_fest = st.sidebar.number_input("Dominical/Fest Nocturno ($)", value=629843)
recargo_nocturno = st.sidebar.number_input("Recargo Nocturno ($)", value=1035090)
extras_diurnas = st.sidebar.number_input("Horas Extra Diurnas ($)", value=17438)
extras_nocturnas = st.sidebar.number_input("Horas Extra Nocturnas ($)", value=219713)

st.sidebar.header("Deducciones Adicionales")
prepaga_colmedica = st.sidebar.number_input("Prepagada Colmedica", value=128057)
iva_prepaga = st.sidebar.number_input("IVA Prepagada", value=6402)
retencion_fuente = st.sidebar.number_input("Retención en la Fuente", value=435000)

# --- CÁLCULOS ---
# El IBC (Ingreso Base de Cotización) usualmente excluye auxilios no prestacionales
ibc = sueldo_basico + dominical_fest + recargo_nocturno + extras_diurnas + extras_nocturnas

# Deducciones de Ley (4% salud, 4% pensión)
desc_salud = ibc * 0.04
desc_pension = ibc * 0.04

# Fondo de Solidaridad (Aproximado según tabla legal si aplica, aquí lo mantenemos dinámico)
# En tu imagen es aprox 0.5% - 1% del IBC
desc_solidaridad = ibc * 0.01 if ibc > (1300000 * 4) else 0

total_devengado = ibc + bono_desempeno + aux_alimentacion
total_deducido = desc_salud + desc_pension + desc_solidaridad + prepaga_colmedica + iva_prepaga + retencion_fuente
neto_a_pagar = total_devengado - total_deducido

# --- VISUALIZACIÓN ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Devengado", f"${total_devengado:,.0f}")
col2.metric("Total Deducciones", f"-${total_deducido:,.0f}")
col3.metric("Neto a Recibir", f"${neto_a_pagar:,.0f}", delta_color="normal")

st.divider()

### Detalle de Nómina
st.subheader("Detalle del Cálculo")
col_a, col_b = st.columns(2)

with col_a:
    st.write("**Ingresos**")
    st.write(f"Sueldo Base: ${sueldo_basico:,.0f}")
    st.write(f"Bonos/Auxilios: ${bono_desempeno + aux_alimentacion:,.0f}")
    st.write(f"Recargos/Extras: ${dominical_fest + recargo_nocturno + extras_diurnas + extras_nocturnas:,.0f}")

with col_b:
    st.write("**Descuentos de Ley**")
    st.write(f"Salud (4%): ${desc_salud:,.0f}")
    st.write(f"Pensión (4%): ${desc_pension:,.0f}")
    st.write(f"Solidaridad: ${desc_solidaridad:,.0f}")

st.info("Nota: Los cálculos de salud y pensión se basan en el IBC (Sueldo + Recargos + Extras).")
