import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora Nómina", page_icon="💰", layout="wide")

# --- FUNCIONES DE CÁLCULO ---
def calcular_retefuente_ley(ingreso_gravable, salud, pension, solidaridad):
    uvt_valor = 47065
    base_intermedia = ingreso_gravable - (salud + pension + solidaridad)
    renta_exenta = base_intermedia * 0.25
    tope_exento_mensual = uvt_valor * 65.8
    if renta_exenta > tope_exento_mensual:
        renta_exenta = tope_exento_mensual
    
    base_final_gravable = base_intermedia - renta_exenta
    base_en_uvt = base_final_gravable / uvt_valor
    
    if base_en_uvt <= 95:
        retencion_uvt = 0
    elif base_en_uvt <= 150:
        retencion_uvt = (base_en_uvt - 95) * 0.19
    elif base_en_uvt <= 360:
        retencion_uvt = (base_en_uvt - 150) * 0.28 + 10
    else:
        retencion_uvt = (base_en_uvt - 360) * 0.33 + 69
        
    return retencion_uvt * uvt_valor

# --- TÍTULO CENTRADO ---
st.markdown("<h1 style='text-align: center;'>📊 Calculadora de Nómina 📚</h1>", unsafe_allow_html=True)

# --- FORMULARIO DE ENTRADA ---
with st.sidebar.form("nomina_form", clear_on_submit=True):
    st.header("📋 Configuración del Mes")
    
    sueldo_basico = st.number_input("Sueldo Básico Pactado ($6,138,000)", value=6138000, step=1)
    aux_alimentacion = st.number_input("Auxilio Alimentación S/P ($355,900)", value=355900, step=1)
    
    st.divider()
    st.subheader("⏰ Cantidad de Horas")
    c_dom_fest = st.number_input("Cant. Dominical Fest Nocturno (1212)", value=None, placeholder="0.00", step=0.01, format="%.2f")
    c_dom_ord = st.number_input("Cant. Dominical Ord Diurno (1214)", value=None, placeholder="0.00", step=0.01, format="%.2f")
    c_rec_noc = st.number_input("Cant. Recargo Nocturno (M220)", value=None, placeholder="0.00", step=0.01, format="%.2f")
    
    st.divider()
    st.subheader("💸 Otros Descuentos")
    desc_prepaga = st.number_input("Deducción Prepagada (7418)", value=128057)
    desc_iva_prepaga = st.number_input("Deducción IVA Prepagada (7473)", value=6402)
    ben_prepaga = st.number_input("Beneficio Prepagada (1610)", value=256114)
    ben_prepaga_iva = st.number_input("Beneficio Prepagada IVA (1619)", value=12805)
    
    submitted = st.form_submit_button("CALCULAR NÓMINA 🟰")

# --- PROCESAMIENTO ---
if submitted:
    c_dom_fest_v = c_dom_fest if c_dom_fest is not None else 0.0
    c_dom_ord_v = c_dom_ord if c_dom_ord is not None else 0.0
    c_rec_noc_v = c_rec_noc if c_rec_noc is not None else 0.0

    valor_hora = sueldo_basico / 240
    
    val_dom_fest_noc = valor_hora * c_dom_fest_v * 2.3464
    val_dom_ord_diu = valor_hora * c_dom_ord_v * 1.9593
    val_rec_noc = valor_hora * c_rec_noc_v * 0.3814
    
    ibc = sueldo_basico + val_dom_fest_noc + val_dom_ord_diu + val_rec_noc
    salud = ibc * 0.04
    pension = ibc * 0.04
    solidaridad = ibc * 0.01
    
    retefuente_auto = calcular_retefuente_ley(ibc, salud, pension, solidaridad)
    
    total_devengado = ibc + aux_alimentacion
    total_deducido = salud + pension + solidaridad + retefuente_auto + desc_prepaga + desc_iva_prepaga
    neto_a_pagar = total_devengado - total_deducido

    # --- TABLA DE DETALLE ---
    datos = [
        ["1000", "Sueldo Básico", 30.00, sueldo_basico, 0, 0],
        ["1212", "Dominical Fest Nocturno", c_dom_fest_v, val_dom_fest_noc, 0, 0],
        ["1214", "Dominical Ord Diurno", c_dom_ord_v, val_dom_ord_diu, 0, 0],
        ["13A2", "Aux. Alimentacion S/P", 30.00, aux_alimentacion, 0, 0],
        ["M220", "Recargo Nocturno", c_rec_noc_v, val_rec_noc, 0, 0],
        ["7418", "Desc. Prepagada Colmedica", 0.00, 0, desc_prepaga, 0],
        ["7473", "Dto Prepa IVA LAN", 0.00, 0, desc_iva_prepaga, 0],
        ["T000", "Descuento Salud", 30.00, 0, salud, 0],
        ["T010", "Descuento Pension", 30.00, 0, pension, 0],
        ["T020", "Descuento Solidaridad", 30.00, 0, solidaridad, 0],
        ["T050", "Retención en la Fuente", 4.72, 0, retefuente_auto, 0],
        ["1610", "Beneficio Prepagada", 0.00, 0, 0, ben_prepaga],
        ["1619", "Beneficio Prepagada IVA", 0.00, 0, 0, ben_prepaga_iva],
    ]

    df = pd.DataFrame(datos, columns=["Codigo", "Descripción", "Cantidad", "Devengado", "Deducido", "Beneficios"])
    
    df_style = df.copy()
    df_style["Cantidad"] = df_style["Cantidad"].map("{:.2f}".format)
    for col in ["Devengado", "Deducido", "Beneficios"]:
        df_style[col] = df_style[col].apply(lambda x: f"${x:,.0f}" if x != 0 else "0")

    st.table(df_style)

    # --- TOTALES EN LA PARTE INFERIOR ---
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("TOTAL DEVENGADO", f"${total_devengado:,.0f}")
    col2.metric("TOTAL DEDUCIDO", f"${total_deducido:,.0f}")
    col3.subheader(f"NETO A PAGAR: ${neto_a_pagar:,.0f}")

else:
    st.info("👈 Ingresa las cantidades y el sueldo en el panel lateral. Presiona 'CALCULAR NÓMINA' para generar el desglose.")

# --- LÍNEA DE CRÉDITO A LA IZQUIERDA ---
st.markdown("<br><hr><p style='color: gray; text-align: left;'>Created by: Dairo Romero</p>", unsafe_allow_html=True)
