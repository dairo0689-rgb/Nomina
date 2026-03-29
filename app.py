import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora Nómina Mensual", page_icon="💰", layout="wide")

st.title("📊 Calculadora de Nómina Personal")
st.write("Configura las cantidades de horas para calcular el pago neto del mes.")

# --- FORMULARIO DE ENTRADA ---
with st.sidebar.form("nomina_form"):
    st.header("📋 Datos del Mes")
    
    # 1. Salario y Fijos (Actualizados según nueva imagen)
    sueldo_basico = st.number_input("Sueldo Básico Pactado", value=6137885)
    aux_alimentacion = st.number_input("Auxilio Alimentación S/P", value=359254)
    
    st.divider()
    
    # 2. Cantidades para Recargos
    st.subheader("⏰ Cantidad de Horas")
    cant_dom_fest_noc = st.number_input("Cant. Dominical Fest Nocturno (1212)", value=0.0, step=0.5)
    cant_dom_ord_diu = st.number_input("Cant. Dominical Ord Diurno (1214)", value=0.0, step=0.5)
    cant_rec_noc = st.number_input("Cant. Recargo Nocturno (M220)", value=0.0, step=1.0)
    
    st.divider()
    
    # 3. Deducciones y Otros
    st.subheader("💸 Deducciones y Beneficios")
    desc_prepaga = st.number_input("Deducción Prepagada (7418)", value=128057)
    desc_iva_prepaga = st.number_input("Deducción IVA Prepagada (7473)", value=6402)
    
    # Casillas de la columna "Beneficios"
    ben_prepaga = st.number_input("Beneficio Prepagada (1610)", value=256114)
    ben_prepaga_iva = st.number_input("Beneficio Prepagada IVA (1619)", value=12805)
    
    # BOTÓN DE CALCULAR
    submitted = st.form_submit_button("🚀 CALCULAR NÓMINA")

# --- LÓGICA DE CÁLCULO ---
if submitted:
    # Valor hora basado en el nuevo básico (mes de 240 horas)
    valor_hora = sueldo_basico / 240
    
    # Cálculos de Recargos (Factores legales aproximados a la imagen)
    # Dominical Fest Noc (1212) factor aprox 2.1 - 2.5 según empresa
    # Dominical Ord Diu (1214) factor aprox 1.75 - 2.0
    val_dom_fest_noc = valor_hora * cant_dom_fest_noc * 2.5
    val_dom_ord_diu = valor_hora * cant_dom_ord_diu * 1.75
    val_rec_noc = valor_hora * cant_rec_noc * 0.35
    
    # IBC (Base para Salud, Pensión y Solidaridad)
    ibc = sueldo_basico + val_dom_fest_noc + val_dom_ord_diu + val_rec_noc
    
    # Deducciones de ley (4%, 4% y 1% solidaridad)
    salud = ibc * 0.04
    pension = ibc * 0.04
    solidaridad = ibc * 0.01 if ibc > (1300000 * 4) else 0
    
    # Retención en la Fuente: 4.72% sobre el devengado gravable (IBC)
    retefuente = ibc * 0.0472
    
    # Totales
    total_devengado = ibc + aux_alimentacion
    total_deducido = salud + pension + solidaridad + retefuente + desc_prepaga + desc_iva_prepaga
    neto_a_pagar = total_devengado - total_deducido

    # --- MOSTRAR RESULTADOS ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Devengado", f"${total_devengado:,.0f}")
    c2.metric("Total Deducido", f"${total_deducido:,.0f}")
    c3.metric("Neto a Pagar", f"${neto_a_pagar:,.0f}")

    st.divider()

    # Creación de la tabla exacta a la imagen
    datos = [
        ["1000", "Sueldo Básico", 30.00, sueldo_basico, 0, 0],
        ["1212", "Dominical Fest Nocturno", cant_dom_fest_noc, val_dom_fest_noc, 0, 0],
        ["1214", "Dominical Ord Diurno", cant_dom_ord_diu, val_dom_ord_diu, 0, 0],
        ["13A2", "Aux. Alimentacion S/P", 30.00, aux_alimentacion, 0, 0],
        ["M220", "Recargo Nocturno", cant_rec_noc, val_rec_noc, 0, 0],
        ["7418", "Desc. Prepagada Colmedica", 0, 0, desc_prepaga, 0],
        ["7473", "Dto Prepa IVA LAN", 0, 0, desc_iva_prepaga, 0],
        ["T000", "Descuento Salud", 30.00, 0, salud, 0],
        ["T010", "Descuento Pension", 30.00, 0, pension, 0],
        ["T020", "Descuento Solidaridad", 30.00, 0, solidaridad, 0],
        ["T050", "Retención en la Fuente", 4.72, 0, retefuente, 0],
        ["1610", "Beneficio Prepagada", 0, 0, 0, ben_prepaga],
        ["1619", "Beneficio Prepagada IVA", 0, 0, 0, ben_prepaga_iva],
    ]

    df = pd.DataFrame(datos, columns=["Codigo", "Descripción", "Cantidad", "Devengado", "Deducido", "Beneficios"])
    
    # Formateo de moneda para visualización
    df_style = df.copy()
    for col in ["Devengado", "Deducido", "Beneficios"]:
        df_style[col] = df_style[col].apply(lambda x: f"${x:,.0f}" if x > 0 else "0")

    st.table(df_style)
    
    st.success(f"### Neto a Pagar: **${neto_a_pagar:,.0f}**")
    st.info(f"IBC (Base de cotización): ${ibc:,.0f} | Retefuente aplicada: 4.72%")

else:
    st.info("👈 Ingresa las cantidades en el panel lateral y presiona 'CALCULAR NÓMINA'")

