import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora Nómina Mensual", page_icon="💰", layout="wide")

# --- FUNCIONES DE CÁLCULO ---
def calcular_retefuente_ley(ingreso_gravable, salud, pension, solidaridad):
    """Calcula la Retención en la Fuente Procedimiento 1 (Valores UVT 2024)"""
    uvt_valor = 47065
    # 1. Base intermedia (Ingresos menos aportes de ley)
    base_intermedia = ingreso_gravable - (salud + pension + solidaridad)
    
    # 2. Renta exenta del 25% (Limitada a 790 UVT anuales / 12 meses)
    renta_exenta = base_intermedia * 0.25
    tope_exento_mensual = uvt_valor * 65.8 # Aprox 3.1M
    if renta_exenta > tope_exento_mensual:
        renta_exenta = tope_exento_mensual
        
    base_final_gravable = base_intermedia - renta_exenta
    base_en_uvt = base_final_gravable / uvt_valor
    
    # 3. Tabla DIAN
    if base_en_uvt <= 95:
        retencion_uvt = 0
    elif base_en_uvt <= 150:
        retencion_uvt = (base_en_uvt - 95) * 0.19
    elif base_en_uvt <= 360:
        retencion_uvt = (base_en_uvt - 150) * 0.28 + 10
    else:
        retencion_uvt = (base_en_uvt - 360) * 0.33 + 69
        
    return retencion_uvt * uvt_valor

st.title("📊 Calculadora de Nómina Personal")
st.write("Cálculo automático de Retefuente basado en UVT y leyes vigentes.")

# --- FORMULARIO DE ENTRADA ---
with st.sidebar.form("nomina_form"):
    st.header("📋 Configuración del Mes")
    
    sueldo_basico = st.number_input("Sueldo Básico Pactado", value=6138000, step=1)
    aux_alimentacion = st.number_input("Auxilio Alimentación S/P", value=355900, step=1)
    
    st.divider()
    st.subheader("⏰ Cantidad de Horas")
    # Formato de 2 decimales en las entradas
    cant_dom_fest_noc = st.number_input("Cant. Dominical Fest Nocturno (1212)", value=25.50, step=0.01, format="%.2f")
    cant_dom_ord_diu = st.number_input("Cant. Dominical Ord Diurno (1214)", value=11.50, step=0.01, format="%.2f")
    cant_rec_noc = st.number_input("Cant. Recargo Nocturno (M220)", value=62.00, step=0.01, format="%.2f")
    
    st.divider()
    st.subheader("💸 Otros Descuentos y Beneficios")
    desc_prepaga = st.number_input("Deducción Prepagada (7418)", value=128057)
    desc_iva_prepaga = st.number_input("Deducción IVA Prepagada (7473)", value=6402)
    ben_prepaga = st.number_input("Beneficio Prepagada (1610)", value=256114)
    ben_prepaga_iva = st.number_input("Beneficio Prepagada IVA (1619)", value=12805)
    
    submitted = st.form_submit_button("🚀 CALCULAR NÓMINA")

# --- PROCESAMIENTO ---
if submitted:
    valor_hora = sueldo_basico / 240
    
    # Factores ajustados para precisión con tu imagen
    val_dom_fest_noc = valor_hora * cant_dom_fest_noc * 2.3464
    val_dom_ord_diu = valor_hora * cant_dom_ord_diu * 1.9593
    val_rec_noc = valor_hora * cant_rec_noc * 0.3814
    
    # IBC (Sueldo + Recargos)
    ibc = sueldo_basico + val_dom_fest_noc + val_dom_ord_diu + val_rec_noc
    
    # Deducciones obligatorias
    salud = ibc * 0.04
    pension = ibc * 0.04
    solidaridad = ibc * 0.01 # Dado el nivel de ingresos es el 1%
    
    # CÁLCULO AUTOMÁTICO RETEFUENTE
    # Nota: El auxilio de alimentación S/P usualmente no suma para retefuente
    retefuente_auto = calcular_retefuente_ley(ibc, salud, pension, solidaridad)
    
    # Totales
    total_devengado = ibc + aux_alimentacion
    total_deducido = salud + pension + solidaridad + retefuente_auto + desc_prepaga + desc_iva_prepaga
    neto_a_pagar = total_devengado - total_deducido

    # --- UI DE RESULTADOS ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Devengado", f"${total_devengado:,.0f}")
    c2.metric("Total Deducido", f"${total_deducido:,.0f}")
    c3.metric("Neto a Pagar", f"${neto_a_pagar:,.0f}")

    st.divider()

    # Tabla estructurada
    datos = [
        ["1000", "Sueldo Básico", 30.00, sueldo_basico, 0, 0],
        ["1212", "Dominical Fest Nocturno", cant_dom_fest_noc, val_dom_fest_noc, 0, 0],
        ["1214", "Dominical Ord Diurno", cant_dom_ord_diu, val_dom_ord_diu, 0, 0],
        ["13A2", "Aux. Alimentacion S/P", 30.00, aux_alimentacion, 0, 0],
        ["M220", "Recargo Nocturno", cant_rec_noc, val_rec_noc, 0, 0],
        ["7418", "Desc. Prepagada Colmedica", 0.00, 0, desc_prepaga, 0],
        ["7473", "Dto Prepa IVA LAN", 0.00, 0, desc_iva_prepaga, 0],
        ["T000", "Descuento Salud", 30.00, 0, salud, 0],
        ["T010", "Descuento Pension", 30.00, 0, pension, 0],
        ["T020", "Descuento Solidaridad", 30.00, 0, solidaridad, 0],
        ["T050", "Retención en la Fuente (Auto)", 4.72, 0, retefuente_auto, 0],
        ["1610", "Beneficio Prepagada", 0.00, 0, 0, ben_prepaga],
        ["1619", "Beneficio Prepagada IVA", 0.00, 0, 0, ben_prepaga_iva],
    ]

    df = pd.DataFrame(datos, columns=["Codigo", "Descripción", "Cantidad", "Devengado", "Deducido", "Beneficios"])
    
    # Formateo de tabla
    df_style = df.copy()
    df_style["Cantidad"] = df_style["Cantidad"].map("{:.2f}".format)
    for col in ["Devengado", "Deducido", "Beneficios"]:
        df_style[col] = df_style[col].apply(lambda x: f"${x:,.0f}" if x != 0 else "0")

    st.table(df_style)
    st.info(f"**Análisis de Retefuente:** Con un ingreso gravable de ${ibc:,.0f}, tu base gravable final tras deducciones de ley y renta exenta es de aproximadamente {(ibc-salud-pension-solidaridad)*0.75/47065:.1f} UVT.")

else:
    st.info("👈 Ingresa los datos y presiona el botón para ver el cálculo automático.")


