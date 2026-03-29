import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora Nómina Mensual", page_icon="💰", layout="wide")

st.title("📊 Calculadora de Nómina Personal")
st.write("Ingresa las cantidades y valores de tu desprendible mensual.")

# --- FORMULARIO DE ENTRADA ---
with st.sidebar.form("nomina_form"):
    st.header("📋 Datos del Mes")
    
    # 1. Salario y Fijos
    sueldo_basico = st.number_input("Sueldo Básico (Valor total)", value=0)
    bono_desempeno = st.number_input("Bono de Desempeño", value=0)
    aux_alimentacion = st.number_input("Auxilio Alimentación S/P", value=0)
    
    st.divider()
    
    # 2. Cantidades para Recargos (Se calcula automático)
    st.subheader("⏰ Cantidad de Horas/Días")
    cant_dom_fest = st.number_input("Cant. Dominical Fest Nocturno", value=0.0, step=0.1)
    cant_rec_noc = st.number_input("Cant. Recargo Nocturno", value=0.0, step=1.0)
    cant_ext_diu = st.number_input("Cant. Hora Extra Diurna", value=0.0, step=0.1)
    cant_ext_noc = st.number_input("Cant. Hora Extra Nocturna", value=0.0, step=0.1)
    
    st.divider()
    
    # 3. Deducciones y Otros
    st.subheader("💸 Deducciones y Beneficios")
    desc_prepaga = st.number_input("Deducción Prepagada", value=0)
    desc_iva_prepaga = st.number_input("Deducción IVA Prepagada", value=0)
    retencion_fuente = st.number_input("Retención en la Fuente", value=0)
    
    # Casillas de la columna "Beneficios" de la imagen
    ben_prepaga = st.number_input("Beneficio Prepagada", value=0)
    ben_prepaga_iva = st.number_input("Beneficio Prepagada IVA", value=0)
    
    # BOTÓN DE CALCULAR
    submitted = st.form_submit_button("🚀 CALCULAR NÓMINA")

# --- LÓGICA DE CÁLCULO ---
if submitted:
    # Cálculo de valor hora basado en el básico (mes de 240 horas)
    # Si el sueldo es 0, el valor hora es 0 para evitar error
    valor_hora = sueldo_basico / 240 if sueldo_basico > 0 else 0
    
    # Cálculos según factores de ley para que coincida con la imagen
    val_dom_fest = valor_hora * cant_dom_fest * 2.5
    val_rec_noc = valor_hora * cant_rec_noc * 0.35
    val_ext_diu = valor_hora * cant_ext_diu * 1.25
    val_ext_noc = valor_hora * cant_ext_noc * 1.75
    
    # IBC (Base para Salud, Pensión y Solidaridad)
    ibc = sueldo_basico + val_dom_fest + val_rec_noc + val_ext_diu + val_ext_noc
    
    # Deducciones de ley
    salud = ibc * 0.04
    pension = ibc * 0.04
    solidaridad = ibc * 0.01 if ibc > (1300000 * 4) else 0 # 1% si supera 4 SMMLV
    
    # Totales
    total_devengado = ibc + bono_desempeno + aux_alimentacion
    total_deducido = salud + pension + solidaridad + desc_prepaga + desc_iva_prepaga + retencion_fuente
    total_beneficios = ben_prepaga + ben_prepaga_iva
    neto_a_pagar = total_devengado - total_deducido

    # --- MOSTRAR RESULTADOS ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Devengado", f"${total_devengado:,.0f}")
    c2.metric("Total Deducido", f"${total_deducido:,.0f}")
    c3.metric("Neto a Pagar", f"${neto_a_pagar:,.0f}", delta_color="normal")

    st.divider()

    # Creación de la tabla tipo desprendible
    datos = [
        ["Sueldo Básico", 30.00, sueldo_basico, 0, 0],
        ["Dominical Fest Nocturno", cant_dom_fest, val_dom_fest, 0, 0],
        ["Bono de Desempeño", 0, bono_desempeno, 0, 0],
        ["Aux. Alimentación S/P", 30.00, aux_alimentacion, 0, 0],
        ["Recargo Nocturno", cant_rec_noc, val_rec_noc, 0, 0],
        ["Hora Extra Diurna", cant_ext_diu, val_ext_diu, 0, 0],
        ["Hora Extra Nocturna", cant_ext_noc, val_ext_noc, 0, 0],
        ["Desc. Prepagada Colmedica", 0, 0, desc_prepaga, 0],
        ["Dto Prepa IVA LAN", 0, 0, desc_iva_prepaga, 0],
        ["Descuento Salud", 30.00, 0, salud, 0],
        ["Descuento Pension", 30.00, 0, pension, 0],
        ["Descuento Solidaridad", 30.00, 0, solidaridad, 0],
        ["Retención en la Fuente", 0, 0, retencion_fuente, 0],
        ["Beneficio Prepagada", 0, 0, 0, ben_prepaga],
        ["Beneficio Prepagada IVA", 0, 0, 0, ben_prepaga_iva],
    ]

    df = pd.DataFrame(datos, columns=["Descripción", "Cantidad", "Devengado", "Deducido", "Beneficios"])
    
    # Formatear tabla para que se vea limpia
    def format_moneda(val):
        return f"${val:,.0f}" if isinstance(val, (int, float)) and val > 0 else "0"

    df_style = df.copy()
    for col in ["Devengado", "Deducido", "Beneficios"]:
        df_style[col] = df_style[col].apply(format_moneda)

    st.table(df_style)
    
    st.subheader(f"Monto Neto Final: ${neto_a_pagar:,.0f}")
    st.caption(f"IBC calculado para este mes: ${ibc:,.0f}")

else:
    st.info("👈 Ingresa los datos en el panel de la izquierda y presiona 'CALCULAR NÓMINA'")
