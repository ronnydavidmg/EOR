import streamlit as st
import numpy as np
import pandas as pd
import lasio
import matplotlib.pyplot as plt
from PIL import Image

def main():
    st.set_page_config(
        page_title="ESPOL EOR SCREENING",
        page_icon="logo.png",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Estilos personalizados
    st.markdown(
        """
        <style>
        body {
            background-color: #007wbb;
            color: black;
            padding: 1000px;
        }
        .stButton {
            background-color: #000ffff;
            color: skyblue;
            border-radius: 40px;
            width: 100px; /* Cambia el ancho del botón */
            height: 60px; /* Cambia la altura del botón */
            padding: 10px 0;
            margin: 5px 0;
        }
        .stMarkdown {
            color: white blue;
            text-align: center;
        }
        .logo {
        width: 70px;
        height: 70px;
        margin-left: auto; /* Centra horizontalmente a la derecha */
        margin-right: auto; /* Centra horizontalmente a la izquierda */
        display: block;
        }   
        .header {
            display: flex;
            align-items: center;
            justify-content: center; /* Centra horizontalmente los elementos */
            padding: 1px 0;
        }
        .header h1 {
            margin: 0;
            margin-left: 100px; /* Agrega un margen izquierdo al título */
        }
        .footer {
            display: flex;
            justify-content: left;
            align-items: left;
            margin-top: 100px;
        }
        .author {
            text-align: left;
            margin: 100px;
        }
        .author img {
            display: block;
            margin: 0 auto 10px; /* Centra la imagen horizontalmente con un margen inferior */
        }
        .author-name {
            margin-top: 10px;
        }
        
        .stMultiColumns {
            padding: 10px;
        }
        
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Encabezado
    st.markdown(
        '<div class="header"><h1>ESPOL EOR SCREENING</h1><h2>Bienvenido al software de screening de técnicas de EOR de la ESPOL.</h2>',
        unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    col2:  st.image("logo.png", width=70)

    #st.write("A continuación, selecciona la opción de ingreso de datos que dispones:")

    # Botones
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    col1, col2, col3= st.columns([0.50, 1, 0.0001])

    uploaded_file = st.file_uploader("Cargar archivo LAS (Log ASCII Standard)", type=["las"])
    if uploaded_file is not None:
            contenido = uploaded_file.read()
            with open("temp.las", "wb") as temp_file:
                temp_file.write(contenido)


            # Lectura de archivo
            las = lasio.read("temp.las")

            # Nombre de pozo
            st.write("Nombre de pozo:", las.well.WELL.value)
            st.write("País:", las.well["COUNT"].value)
            st.write("Provincia:", las.well["STATE"].value)
            st.write("Compañía:", las.well["COMP"].value)

            api = st.number_input("Gravedad API:", value=0, min_value=0)
            tem = st.number_input("Temperatura en °C:", value=0, min_value=0)

            # 3 decimales
            pd.options.display.float_format = '{:.3f}'.format

            st.write("")
            st.write("")
            las.delete_curve('CALI')
            las.delete_curve('ILD')
            las.delete_curve('KTR')
            las.delete_curve('TR1')
            las.delete_curve('VCLGR')
            las.delete_curve('BS')
            las.delete_curve('DTMA')
            las.delete_curve('DT')
            las.delete_curve('SP')
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            # Se transforma el archivo
            well = las.df()

            df_filtrado = well.loc[well['PAYFLAG'] == 1]
            # print("\n",df_filtrado)

            # Se imprime valores estadisticos
            # print(df_filtrado.describe())

            df_filtrado.reset_index(drop=False, inplace=True)

            df_filtrado = df_filtrado.sort_values(by='DEPTH')

            # Inicializamos variables para almacenar la información del intervalo más largo.
            max_width = 0
            max_width_start = 0
            current_width = 1
            current_start = 0

            # Recorremos las profundidades en el DataFrame.
            for i in range(1, len(df_filtrado)):
                if df_filtrado.iloc[i]['DEPTH'] == df_filtrado.iloc[i - 1]['DEPTH'] + 0.5:
                    current_width += 1
                else:
                    if current_width > max_width:
                        max_width = current_width
                        max_width_start = current_start
                    current_width = 1
                    current_start = i

            # Verificamos si el último intervalo es el más largo.
            if current_width > max_width:
                max_width = current_width
                max_width_start = current_start

            # Calculamos la profundidad final del intervalo más largo.
            intervalo_largo_final = df_filtrado.iloc[max_width_start]['DEPTH'] + (max_width - 1) * 0.5

            # Filtramos el DataFrame para obtener todo el intervalo más largo.
            intervalo_largo = df_filtrado[
                (df_filtrado['DEPTH'] >= df_filtrado.iloc[max_width_start]['DEPTH']) &
                (df_filtrado['DEPTH'] <= intervalo_largo_final)]

            # Imprimimos el intervalo más largo consecutivo.
            # print(intervalo_largo)

            # ESPESOR
            esp = intervalo_largo['DEPTH'].max() - intervalo_largo['DEPTH'].min()
            esp = esp * 0.3048
            esp = round(esp, 3)
            st.write("El valor del espesor es:", esp, "m")

            # PROFUNDIDAD
            prof = (intervalo_largo['DEPTH'].min() + intervalo_largo['DEPTH'].max()) / 2
            prof = prof * 0.3048
            prof = round(prof, 3)
            st.write("El valor de la profundidad es:", prof, "m")

            # POROSIDAD
            por = np.mean(intervalo_largo['PHIT'])
            por = round(por, 3)
            por = por * 100
            por = float(por)
            st.write("El valor de porosidad es:", por, "%")

            # SATURACIÓN DE PETRÓLEO
            swa = np.mean(intervalo_largo['SW'])
            swa = round(swa, 3)

            sat = (1 - swa) * 100
            st.write("El valor de saturación de petróleo es:", sat, "%")

            # PERMEABILIDAD -- ECUACION DE TIMUR 1968  k = C * (φ^3) * (S_w / (1 - S_w))^2 CARMAN KOZENY C= 5 SIMLFICADO
            per = ((((por / 100) ** 2.2) * 93) / (swa)) ** 2
            per = round(per, 3)
            st.write("El valor de permeabilidad es:", per, "mD")

            # VISCOSIDAD -- ECUACIÓN DE CARMAN-KOZENY SIMPLIFICADA

            vis = (((por / 100) ** 3) / ((swa / 100) * (sat / 100))) ** 0.5
            vis = round(vis, 3)
            st.write("El valor de viscosidad es:", vis, "cp")

            # TIPO DE ROCA

            GRm = well['GR'].min()
            GR = well['GR'].max() - well['GR'].min()
            gamma = np.mean(intervalo_largo['GR'])
            vsh = (gamma - GRm) / GR

            if vsh >= 0.6:
                roca = "LUTITA"
                st.write("La roca en su reservorio es:", roca)
            else:
                roca = "ARENISCA"
                st.write("La roca en su reservorio es:", roca)

            CIS = float(0)
            if float(per) >= float(10) and float(per) <= float(132.5):
                CIS = CIS + 0.5
            elif float(per) > float(132.5) and float(per) < float(377.5):
                CIS = CIS + 1.0
            elif float(per) >= float(377.5) and float(per) <= float(500):
                CIS = CIS + 0.5
            else:
                CIS = CIS + 0.0
            if por >= float(15) and por <= float(20):
                CIS = CIS + 0.5
            elif por > float(20) and por < float(30):
                CIS = CIS + 1.0
            elif por >= float(30) and por <= float(35):
                CIS = CIS + 0.5
            else:
                CIS = CIS + 0.0
            if esp >= float(5) and esp <= float(91.25):
                CIS = CIS + 0.5
            elif esp > float(91.25) and esp < float(263.75):
                CIS = CIS + 1
            elif esp >= float(263.75) and esp <= float(350):
                CIS = CIS + 0.5
            else:
                CIS = CIS + 0.0
            if tem >= float(150) and tem <= float(200):
                CIS = CIS + 0.5
            elif tem > float(200) and tem < float(300):
                CIS = CIS + 1.0
            elif tem >= float(300) and tem <= float(350):
                CIS = CIS + 0.5
            else:
                CIS = CIS + 0.0
            if api >= float(15):
                CIS = CIS + 1.0
            else:
                CIS = CIS + 0.0
            if vis >= float(100) and vis <= float(2575):
                CIS = CIS + 0.5
            elif vis > float(2575) and vis < float(7525):
                CIS = CIS + 1.0
            elif vis >= float(7525) and vis <= float(10000):
                CIS = CIS + 0.5
            else:
                CIS = CIS + 0.0
            if sat >= float(30):
                CIS = CIS + 1.0
            else:
                CIS = CIS + 0.0
            if prof >= float(500) and prof <= float(3500):
                CIS = CIS + 1.0
            elif prof >= float(3500):
                CIS = CIS + 0.5
            else:
                CIS = CIS + 0.0
            if roca == "ARENISCA":
                CIS = CIS + 1.0
            else:
                CIS = CIS + 0.0
            # THAI
            THAI = float(0)
            if float(per) >= float(10) and float(per) <= float(57.5):
                THAI = THAI + 0.5
            elif float(per) > float(57.5) and float(per) < float(152.5):
                THAI = THAI + 1.0
            elif float(per) >= float(152.5) and float(per) <= float(200):
                THAI = THAI + 0.5
            else:
                THAI = THAI + 0.0
            if por >= float(20) and por <= float(23.75):
                THAI = THAI + 0.5
            elif por > float(23.75) and por < float(31.25):
                THAI = THAI + 1.0
            elif por >= float(31.25) and por <= float(35):
                THAI = THAI + 0.5
            else:
                THAI = THAI + 0.0
            if esp >= float(5) and esp <= float(11.25):
                THAI = THAI + 0.5
            elif esp > float(11.25) and esp < float(23.75):
                THAI = THAI + 1
            elif esp >= float(23.75) and esp <= float(30):
                THAI = THAI + 0.5
            else:
                THAI = THAI + 0.0
            if tem >= float(300) and tem <= float(325):
                THAI = THAI + 0.5
            elif tem > float(325) and tem < float(375):
                THAI = THAI + 1.0
            elif tem >= float(375) and tem <= float(400):
                THAI = THAI + 0.5
            else:
                THAI = THAI + 0.0
            if api <= float(12) and api > float(0):
                THAI = THAI + 1.0
            else:
                THAI = THAI + 0.0
            if vis >= float(50) and vis <= float(12537.5):
                THAI = THAI + 0.5
            elif vis > float(12537.5) and vis < float(37512.5):
                THAI = THAI + 1.0
            elif vis >= float(37512.5) and vis <= float(50000):
                THAI = THAI + 0.5
            else:
                THAI = THAI + 0.0
            if sat >= float(20):
                THAI = THAI + 1.0
            else:
                THAI = THAI + 0.0
            if prof >= float(200) and prof <= float(3500):
                THAI = THAI + 1.0
            elif prof >= float(3500):
                THAI = THAI + 0.5
            else:
                THAI = THAI + 0.0
            if roca == "ARENISCA" or roca == "CARBONATA":
                THAI = THAI + 1.0
            else:
                THAI = THAI + 0.0
            # INYECCIÓN DE VAPOR
            VAP = float(0)
            if float(per) >= float(50) and float(per) <= float(162.5):
                VAP = VAP + 0.5
            elif float(per) > float(162.5) and float(per) < float(387.5):
                VAP = VAP + 1.0
            elif float(per) >= float(387.5) and float(per) <= float(500):
                VAP = VAP + 0.5
            else:
                VAP = VAP + 0.0
            if por >= float(20) and por <= float(22.5):
                VAP = VAP + 0.5
            elif por > float(22.5) and por < float(27.5):
                VAP = VAP + 1.0
            elif por >= float(27.5) and por <= float(30):
                VAP = VAP + 0.5
            else:
                VAP = VAP + 0.0
            if esp >= float(20) and esp <= float(25):
                VAP = VAP + 0.5
            elif esp > float(25) and esp <= float(35):
                VAP = VAP + 1
            elif esp >= float(35) and esp <= float(40):
                VAP = VAP + 0.5
            else:
                VAP = VAP + 0.0
            if tem >= float(200) and tem <= float(212.5):
                VAP = VAP + 0.5
            elif tem > float(212.5) and tem < float(237.5):
                VAP = VAP + 1.0
            elif tem >= float(237.5) and tem <= float(250):
                VAP = VAP + 0.5
            else:
                VAP = VAP + 0.0
            if api >= float(8) and api <= float(11):
                VAP = VAP + 0.5
            elif api > float(14) and api < float(17):
                VAP = VAP + 1.0
            elif api >= float(17) and api <= float(20):
                VAP = VAP + 0.5
            else:
                VAP = VAP + 0.0
            if vis >= float(10) and vis <= float(57.5):
                VAP = VAP + 0.5
            elif vis > float(57.5) and vis < float(152.5):
                VAP = VAP + 1.0
            elif vis >= float(152.5) and vis <= float(200):
                VAP = VAP + 0.5
            else:
                VAP = VAP + 0.0
            if sat >= float(50):
                VAP = VAP + 1.0
            elif sat >= float(30) and sat < float(50):
                VAP = VAP + 0.5
            else:
                VAP = VAP + 0.0
            if prof >= float(600) and prof <= float(700):
                VAP = VAP + 0.5
            elif prof > float(700) and prof < float(900):
                VAP = VAP + 1.0
            elif prof >= float(900) and prof <= float(1000):
                VAP = VAP + 0.5
            else:
                VAP = VAP + 0.0
            if roca == "ARENISCA":
                VAP = VAP + 1.0
            else:
                VAP = VAP + 0.0
            # HUFF AND PUFF
            HAP = float(0)
            if float(per) <= float(100) and float(per) >= float(77.5):
                HAP = HAP + 0.5
            elif float(per) < float(77.5) and float(per) > float(32.5):
                HAP = HAP + 1.0
            elif float(per) <= float(32.5) and float(per) >= float(10):
                HAP = HAP + 0.5
            else:
                HAP = HAP + 0.0
            if por >= float(10) and por <= float(13.75):
                HAP = HAP + 0.5
            elif por > float(13.75) and por < float(21.25):
                HAP = HAP + 1.0
            elif por >= float(21.25) and por <= float(25):
                HAP = HAP + 0.5
            else:
                HAP = HAP + 0.0
            if esp >= float(10):
                HAP = HAP + 1
            else:
                HAP = HAP + 0.0
            if tem >= float(90):
                HAP = HAP + 1.0
            else:
                HAP = HAP + 0.0
            if api >= float(15) and api <= float(23.75):
                HAP = HAP + 0.5
            elif api > float(23.75) and api < float(41.25):
                HAP = HAP + 1.0
            elif api >= float(41.25) and api <= float(50):
                HAP = HAP + 0.5
            else:
                HAP = HAP + 0.0
            if vis >= float(10) and vis <= float(382.5):
                HAP = HAP + 0.5
            elif vis > float(382.5) and vis < float(1127.5):
                HAP = HAP + 1.0
            elif vis >= float(1127.5) and vis <= float(1500):
                HAP = HAP + 0.5
            else:
                HAP = HAP + 0.0
            if sat >= float(50):
                HAP = HAP + 1.0
            else:
                HAP = HAP + 0.0
            if prof >= float(600):
                HAP = HAP + 1.0
            else:
                HAP = HAP + 0.0
            if roca == "ARENISCA":
                HAP = HAP + 1.0
            else:
                HAP = HAP + 0.0
            # STEAM DRIVE
            SD = float(0)
            if float(per) >= float(50) and float(per) <= float(537.5):
                SD = SD + 0.5
            elif float(per) > float(537.5) and float(per) < float(1512.5):
                SD = SD + 1.0
            elif float(per) >= float(1512.5) and float(per) <= float(2000):
                SD = SD + 0.5
            else:
                SD = SD + 0.0
            if por >= float(15) and por <= float(18.75):
                SD = SD + 0.5
            elif por > float(18.75) and por < float(26.25):
                SD = SD + 1.0
            elif por >= float(26.25) and por <= float(30):
                SD = SD + 0.5
            else:
                SD = SD + 0.0
            if esp >= float(10):
                SD = SD + 1
            else:
                SD = SD + 0.0
            if tem >= float(150) and tem <= float(187.5):
                SD = SD + 0.5
            elif tem > float(187.5) and tem < float(262.5):
                SD = SD + 1.0
            elif tem >= float(262.5) and tem <= float(300):
                SD = SD + 0.5
            else:
                SD = SD + 0.0
            if api >= float(12):
                SD = SD + 1.0
            else:
                SD = SD + 0.0
            if vis >= float(10) and vis <= float(2507.5):
                SD = SD + 0.5
            elif vis > float(2507.5) and vis < float(7502.5):
                SD = SD + 1.0
            elif vis >= float(7502.5) and vis <= float(10000):
                SD = SD + 0.5
            else:
                SD = SD + 0.0
            if sat >= float(50):
                SD = SD + 1.0
            else:
                SD = SD + 0.0
            if prof >= float(90) and prof <= float(442.5):
                SD = SD + 0.5
            elif prof > float(442.5) and prof < float(1147.5):
                SD = SD + 1.0
            elif prof >= float(1147.5) and prof <= float(1500):
                SD = SD + 0.5
            else:
                SD = SD + 0.0
            if roca == "ARENISCA":
                SD = SD + 1.0
            else:
                SD = SD + 0.0
            # SAGD
            SAGD = float(0)
            if float(per) >= float(1) and float(per) <= float(125):
                SAGD = SAGD + 0.5
            elif float(per) > float(125) and float(per) < float(375):
                SAGD = SAGD + 1.0
            elif float(per) >= float(375) and float(per) <= float(500):
                SAGD = SAGD + 0.5
            else:
                SAGD = SAGD + 0.0
            if por >= float(20) and por <= float(23.75):
                SAGD = SAGD + 0.5
            elif por > float(23.75) and por < float(31.25):
                SAGD = SAGD + 1.0
            elif por >= float(31.25) and por <= float(35):
                SAGD = SAGD + 0.5
            else:
                SAGD = SAGD + 0.0
            if esp >= float(5):
                SAGD = SAGD + 1
            else:
                SAGD = SAGD + 0.0
            if tem >= float(200) and tem <= float(225):
                SAGD = SAGD + 0.5
            elif tem > float(225) and tem < float(275):
                SAGD = SAGD + 1.0
            elif tem >= float(275) and tem <= float(300):
                SAGD = SAGD + 0.5
            else:
                SAGD = SAGD + 0.0
            if api <= float(15) and api > float(0):
                SAGD = SAGD + 1.0
            else:
                SAGD = SAGD + 0.0
            if vis >= float(10000):
                SAGD = SAGD + 1.0
            else:
                SAGD = SAGD + 0.0
            if sat >= float(70):
                SAGD = SAGD + 1.0
            else:
                SAGD = SAGD + 0.0
            if prof <= float(1000) and prof > float(0):
                SAGD = SAGD + 1.0
            else:
                SAGD = SAGD + 0.0
            if roca == "ARENISCA":
                SAGD = SAGD + 1.0
            else:
                SAGD = SAGD + 0.0
            # INYECCIÓN DE CO2 SUPERCRÍTICO
            COS = float(0)
            if float(per) >= float(50) and float(per) <= float(287.5):
                COS = COS + 0.5
            elif float(per) > float(287.5) and float(per) < float(762.5):
                COS = COS + 1.0
            elif float(per) >= float(762.5) and float(per) <= float(1000):
                COS = COS + 0.5
            else:
                COS = COS + 0.0
            if por >= float(20) and por <= float(22.5):
                COS = COS + 0.5
            elif por > float(22.5) and por < float(27.5):
                COS = COS + 1.0
            elif por >= float(27.5) and por <= float(30):
                COS = COS + 0.5
            else:
                COS = COS + 0.0
            if esp >= float(3) and esp <= float(4):
                COS = COS + 1
            else:
                COS = COS + 0.0
            if tem >= float(40) and tem <= float(45):
                COS = COS + 0.5
            elif tem > float(45) and tem < float(55):
                COS = COS + 1.0
            elif tem >= float(55) and tem <= float(60):
                COS = COS + 0.5
            else:
                COS = COS + 0.0
            if api <= float(20) and api > float(0):
                COS = COS + 1.0
            else:
                COS = COS + 0.0
            if vis >= float(1000):
                COS = COS + 1.0
            else:
                COS = COS + 0.0
            if sat >= float(30):
                COS = COS + 1.0
            else:
                COS = COS + 0.0
            if prof == float(0):
                COS = COS + 0.0
            else:
                COS = COS + 1.0  # Profundidad no relevante
            if roca == float(0):
                COS = COS + 0.0
            else:
                COS = COS + 1.0  # Tipo de roca no relevante
            # INYECCIÓN DE CO2 CONVENCIONAL
            COV = float(0)
            if float(per) >= float(10):
                COV = COV + 1.0
            else:
                COV = COV + 0.0
            if por >= float(10):
                COV = COV + 1.0
            else:
                COV = COV + 0.0
            if esp >= float(3):
                COV = COV + 1
            else:
                COV = COV + 0.0
            if tem >= float(60) and tem <= float(132.5):
                COV = COV + 0.5
            elif tem > float(132.5) and tem < float(277.5):
                COV = COV + 1.0
            elif tem >= float(277.5) and tem <= float(350):
                COV = COV + 0.5
            else:
                COV = COV + 0.0
            if api >= float(15) and api <= float(21.25):
                COV = COV + 0.5
            elif api > float(21.25) and api < float(33.75):
                COV = COV + 1.0
            elif api >= float(33.75) and api <= float(40):
                COV = COV + 0.5
            else:
                COV = COV + 0.0
            if vis >= float(50):
                COV = COV + 1.0
            else:
                COV = COV + 0.0
            if sat <= float(50) and sat > float(0):
                COV = COV + 1.0
            else:
                COV = COV + 0.0
            if prof <= float(1500) and prof > float(0):
                COV = COV + 1.0
            else:
                COV = COV + 0.0
            if roca == "ARENISCA" or roca == "CALIZA":
                COV = COV + 1.0
            else:
                COV = COV + 0.0
            # INYECCIÓN DE N2 CONVENCIONAL
            IN = float(0)
            if float(per) >= float(50) and float(per) <= float(287.5):
                IN = IN + 0.5
            elif float(per) > float(287.5) and float(per) < float(762.5):
                IN = IN + 1.0
            elif float(per) >= float(762.5) and float(per) <= float(1000):
                IN = IN + 0.5
            else:
                IN = IN + 0.0
            if por >= float(20) and por <= float(22.5):
                IN = IN + 0.5
            elif por > float(22.5) and por < float(27.5):
                IN = IN + 1.0
            elif por >= float(27.5) and por <= float(30):
                IN = IN + 0.5
            else:
                IN = IN + 0.0
            if esp >= float(10):
                IN = IN + 1
            else:
                IN = IN + 0.0
            if tem >= float(60) and tem <= float(82.5):
                IN = IN + 0.5
            elif tem > float(82.5) and tem < float(127.5):
                IN = IN + 1.0
            elif tem >= float(127.5) and tem <= float(150):
                IN = IN + 0.5
            else:
                IN = IN + 0.0
            if api >= float(15) and api <= float(20):
                IN = IN + 0.5
            elif api > float(20) and api < float(30):
                IN = IN + 1.0
            elif api >= float(30) and api <= float(35):
                IN = IN + 0.5
            else:
                IN = IN + 0.0
            if vis >= float(100) and vis <= float(2575):
                IN = IN + 0.5
            elif vis > float(2575) and vis < float(7525):
                IN = IN + 1.0
            elif vis >= float(7525) and vis <= float(10000):
                IN = IN + 0.5
            else:
                IN = IN + 0.0
            if sat >= float(50) and sat <= float(55):
                IN = IN + 0.5
            elif sat > float(55) and sat < float(65):
                IN = IN + 1.0
            elif sat >= float(65) and sat <= float(70):
                IN = IN + 0.5
            else:
                IN = IN + 0.0
            if prof >= float(1000):
                IN = IN + 1.0
            else:
                IN = IN + 0.0
            if roca == "ARENISCA" or roca == "CALIZA":
                IN = IN + 1.0
            else:
                IN = IN + 0.0
            # ASP
            ASP = float(0)
            if float(per) >= float(10) and float(per) <= float(257.5):
                ASP = ASP + 0.5
            elif float(per) > float(257.5) and float(per) < float(752.5):
                ASP = ASP + 1.0
            elif float(per) >= float(752.5) and float(per) <= float(1000):
                ASP = ASP + 0.5
            else:
                ASP = ASP + 0.0
            if por >= float(20) and por <= float(23.75):
                ASP = ASP + 0.5
            elif por > float(23.75) and por < float(31.25):
                ASP = ASP + 1.0
            elif por >= float(31.25) and por <= float(35):
                ASP = ASP + 0.5
            else:
                ASP = ASP + 0.0
            if esp >= float(10):
                ASP = ASP + 1
            else:
                ASP = ASP + 0.0
            if tem >= float(60) and tem <= float(67.5):
                ASP = ASP + 0.5
            elif tem > float(67.5) and tem < float(82.5):
                ASP = ASP + 1.0
            elif tem >= float(82.5) and tem <= float(90):
                ASP = ASP + 0.5
            else:
                ASP = ASP + 0.0
            if api >= float(10) and api <= float(15):
                ASP = ASP + 0.5
            elif api > float(15) and api < float(25):
                ASP = ASP + 1.0
            elif api >= float(25) and api <= float(30):
                ASP = ASP + 0.5
            else:
                ASP = ASP + 0.0
            if vis >= float(300):
                ASP = ASP + 1.0
            else:
                ASP = ASP + 0.0
            if sat >= float(70):
                ASP = ASP + 1.0
            else:
                ASP = ASP + 0.0
            if prof >= float(1000) and prof <= float(1500):
                ASP = ASP + 0.5
            elif prof > float(1500) and prof < float(2500):
                ASP = ASP + 1.0
            elif prof >= float(2500) and prof <= float(3000):
                ASP = ASP + 0.5
            else:
                ASP = ASP + 0.0
            if roca == "ARENISCA" or roca == "CARBONATA":
                ASP = ASP + 1.0
            else:
                ASP = ASP + 0.0
            # SP
            SP = float(0)
            if float(per) >= float(1):
                SP = SP + 1.0
            else:
                SP = SP + 0.0
            if por >= float(10) and por <= float(15):
                SP = SP + 0.5
            elif por > float(15) and por < float(25):
                SP = SP + 1.0
            elif por >= float(25) and por <= float(30):
                SP = SP + 0.5
            else:
                SP = SP + 0.0
            if esp >= float(10):
                SP = SP + 1
            else:
                SP = SP + 0.0
            if tem <= float(200) and tem > float(0):
                SP = SP + 1.0
            else:
                SP = SP + 0.0
            if api >= float(10) and api <= float(17.5):
                SP = SP + 0.5
            elif api > float(17.5) and api < float(32.5):
                SP = SP + 1.0
            elif api >= float(32.5) and api <= float(40):
                SP = SP + 0.5
            else:
                SP = SP + 0.0
            if vis >= float(100):
                SP = SP + 1.0
            else:
                SP = SP + 0.0
            if sat >= float(30):
                SP = SP + 1.0
            else:
                SP = SP + 0.0
            if prof <= float(2500) and prof > float(0):
                SP = SP + 1.0
            else:
                SP = SP + 0.0
            if roca == "ARENISCA" or roca == "CARBONATA":
                SP = SP + 1.0
            else:
                SP = SP + 0.0
            # MP
            MP = float(0)
            if float(per) <= float(50) and per > float(0):
                MP = MP + 1.0
            else:
                MP = MP + 0.0
            if por >= float(20):
                MP = MP + 1.0
            else:
                MP = MP + 0.0
            if esp >= float(10):
                MP = MP + 1
            else:
                MP = MP + 0.0
            if tem <= float(100) and tem > float(0):
                MP = MP + 1.0
            else:
                MP = MP + 0.0
            if api >= float(10) and api <= float(17.5):
                MP = MP + 0.5
            elif api > float(17.5) and api < float(32.5):
                MP = MP + 1.0
            elif api >= float(32.5) and api <= float(40):
                MP = MP + 0.5
            else:
                MP = MP + 0.0
            if vis >= float(10):
                MP = MP + 1.0
            else:
                MP = MP + 0.0
            if sat >= float(30):
                MP = MP + 1.0
            else:
                MP = MP + 0.0
            if prof <= float(1500) and prof > float(0):
                MP = MP + 1.0
            else:
                MP = MP + 0.0
            if roca == "ARENISCA" or roca == "CARBONATA":
                MP = MP + 1.0
            else:
                MP = MP + 0.0
            # INYECCIÓN DE GELES
            GEL = float(0)
            if float(per) >= float(10) and float(per) <= float(132.5):
                GEL = GEL + 0.5
            elif float(per) > float(132.5) and float(per) < float(377.5):
                GEL = GEL + 1.0
            elif float(per) >= float(377.5) and float(per) <= float(500):
                GEL = GEL + 0.5
            else:
                GEL = GEL + 0.0
            if por >= float(10):
                GEL = GEL + 1.0
            else:
                GEL = GEL + 0.0
            if esp >= float(10):
                GEL = GEL + 1
            else:
                GEL = GEL + 0.0
            if tem >= float(40) and tem <= float(50):
                GEL = GEL + 0.5
            elif tem > float(50) and tem < float(70):
                GEL = GEL + 1.0
            elif tem >= float(70) and tem <= float(80):
                GEL = GEL + 0.5
            else:
                GEL = GEL + 0.0
            if api >= float(20) and api <= float(25):
                GEL = GEL + 0.5
            elif api > float(25) and api < float(35):
                GEL = GEL + 1.0
            elif api >= float(35) and api <= float(40):
                GEL = GEL + 0.5
            else:
                GEL = GEL + 0.0
            if vis >= float(5):
                GEL = GEL + 1.0
            else:
                GEL = GEL + 0.0
            if sat >= float(30):
                GEL = GEL + 1.0
            else:
                GEL = GEL + 0.0
            if prof >= float(1000):
                GEL = GEL + 1.0
            else:
                GEL = GEL + 0.0
            if roca == "ARENISCA" or roca == "CALIZA" or roca == "DOLOMITA":
                GEL = GEL + 1.0
            else:
                GEL = GEL + 0.0
            # INYECCIÓN DE MICROORGANISMOS
            MIC = float(0)
            if float(per) >= float(10) and float(per) <= float(257.5):
                MIC = MIC + 0.5
            elif float(per) > float(257.5) and float(per) < float(752.5):
                MIC = MIC + 1.0
            elif float(per) >= float(752.5) and float(per) <= float(1000):
                MIC = MIC + 0.5
            else:
                MIC = MIC + 0.0
            if por >= float(10) and por <= float(15):
                MIC = MIC + 0.5
            elif por > float(15) and por < float(25):
                MIC = MIC + 1.0
            elif por >= float(25) and por <= float(30):
                MIC = MIC + 0.5
            else:
                MIC = MIC + 0.0
            if esp >= float(10):
                MIC = MIC + 1
            else:
                MIC = MIC + 0.0
            if tem >= float(30) and tem <= float(42.5):
                MIC = MIC + 0.5
            elif tem > float(42.5) and tem < float(67.5):
                MIC = MIC + 1.0
            elif tem >= float(67.5) and tem <= float(80):
                MIC = MIC + 0.5
            else:
                MIC = MIC + 0.0
            if api >= float(20) and api <= float(25):
                MIC = MIC + 0.5
            elif api > float(25) and api < float(35):
                MIC = MIC + 1.0
            elif api >= float(35) and api <= float(40):
                MIC = MIC + 0.5
            else:
                MIC = MIC + 0.0
            if vis <= float(100) and vis > float(0):
                MIC = MIC + 1.0
            else:
                MIC = MIC + 0.0
            if sat <= float(60) and sat > float(0):
                MIC = MIC + 1.0
            else:
                MIC = MIC + 0.0
            if prof <= float(3000) and prof > float(0):
                MIC = MIC + 1.0
            else:
                MIC = MIC + 0.0
            if roca == "ARENISCA":
                MIC = MIC + 1.0
            else:
                MIC = MIC + 0.0
            # HOT WATERFLOODING
            HW = float(0)
            if float(per) >= float(50) and float(per) <= float(287.5):
                HW = HW + 0.5
            elif float(per) > float(287.5) and float(per) < float(762.5):
                HW = HW + 1.0
            elif float(per) >= float(762.5) and float(per) <= float(1000):
                HW = HW + 0.5
            else:
                HW = HW + 0.0
            if por >= float(15):
                HW = HW + 1.0
            else:
                HW = HW + 0.0
            if esp >= float(10):
                HW = HW + 1
            else:
                HW = HW + 0.0
            if tem >= float(60):
                HW = HW + 1.0
            else:
                HW = HW + 0.0
            if api >= float(8) and api <= float(12.25):
                HW = HW + 0.5
            elif api > float(12.25) and api < float(20.75):
                HW = HW + 1.0
            elif api >= float(20.75) and api <= float(25):
                HW = HW + 0.5
            else:
                HW = HW + 0.0
            if vis >= float(100):
                HW = HW + 1.0
            else:
                HW = HW + 0.0
            if sat >= float(50):
                HW = HW + 1.0
            else:
                HW = HW + 0.0
            if prof >= float(1000):
                HW = HW + 1.0
            else:
                HW = HW + 0.0
            if roca == "ARENISCA" or roca == "CARBONATA":
                HW = HW + 1.0
            else:
                HW = HW + 0.0
            # WAG
            WAG = float(0)
            if float(per) >= float(1) and float(per) <= float(500):
                WAG = WAG + 1.0
            else:
                WAG = WAG + 0.0
            if por >= float(15):
                WAG = WAG + 1.0
            else:
                WAG = WAG + 0.0
            if esp >= float(10):
                WAG = WAG + 1
            else:
                WAG = WAG + 0.0
            if tem >= float(40):
                WAG = WAG + 1.0
            else:
                WAG = WAG + 0.0
            if api >= float(10) and api <= float(17.5):
                WAG = WAG + 0.5
            elif api > float(17.5) and api < float(32.5):
                WAG = WAG + 1.0
            elif api >= float(32.5) and api <= float(40):
                WAG = WAG + 0.5
            else:
                WAG = WAG + 0.0
            if vis >= float(50):
                WAG = WAG + 1.0
            else:
                WAG = WAG + 0.0
            if sat >= float(50):
                WAG = WAG + 1.0
            else:
                WAG = WAG + 0.0
            if prof >= float(500):
                WAG = WAG + 1.0
            else:
                WAG = WAG + 0.0
            if roca == "ARENISCA" or roca == "CARBONATA":
                WAG = WAG + 1.0
            else:
                WAG = WAG + 0.0
            # INYECCIÓN DE MICROFLUIDOS
            MICF = float(0)
            if float(per) >= float(1) and float(per) <= float(1000):
                MICF = MICF + 1.0
            else:
                MICF = MICF + 0.0
            if por >= float(20) and por <= float(23.75):
                MICF = MICF + 0.5
            elif por > float(23.75) and por < float(31.25):
                MICF = MICF + 1.0
            elif por >= float(31.25) and por <= float(35):
                MICF = MICF + 0.5
            else:
                MICF = MICF + 0.0
            if esp >= float(10) and esp <= float(20):
                MICF = MICF + 0.5
            elif esp > float(20) and esp < float(40):
                MICF = MICF + 1.0
            elif esp >= float(40) and esp <= float(50):
                MICF = MICF + 0.5
            else:
                MICF = MICF + 0.0
            if tem >= float(30) and tem <= float(40):
                MICF = MICF + 0.5
            elif tem > float(40) and tem < float(60):
                MICF = MICF + 1.0
            elif tem >= float(60) and tem <= float(70):
                MICF = MICF + 0.5
            else:
                MICF = MICF + 0.0
            if api >= float(20) and api <= float(27.5):
                MICF = MICF + 0.5
            elif api > float(27.5) and api < float(42.5):
                MICF = MICF + 1.0
            elif api >= float(42.5) and api <= float(50):
                MICF = MICF + 0.5
            else:
                MICF = MICF + 0.0
            if vis <= float(100) and vis > float(0):
                MICF = MICF + 1.0
            else:
                MICF = MICF + 0.0
            if sat >= float(60) and sat <= float(65):
                MICF = MICF + 0.5
            elif sat > float(65) and sat < float(75):
                MICF = MICF + 1.0
            elif sat >= float(75) and sat <= float(80):
                MICF = MICF + 0.5
            else:
                MICF = MICF + 0.0
            if prof >= float(500) and prof <= float(1125):
                MICF = MICF + 0.5
            elif prof > float(1125) and prof < float(2375):
                MICF = MICF + 1.0
            elif prof >= float(2375) and prof <= float(3000):
                MICF = MICF + 0.5
            else:
                MICF = MICF + 0.0
            if roca == "ARENISCA" or roca == "CALIZA":
                MICF = MICF + 1.0
            else:
                MICF = MICF + 0.0
            # INYECCIÓN DE AGENTES DE CAMBIO DE FASE
            ACS = float(0)
            if float(per) >= float(10) and float(per) <= float(250):
                ACS = ACS + 0.5
            elif float(per) > float(250) and float(per) < float(750):
                ACS = ACS + 1.0
            elif float(per) >= float(750) and float(per) <= float(1000):
                ACS = ACS + 0.5
            else:
                ACS = ACS + 0.0
            if por >= float(20) and por <= float(23.75):
                ACS = ACS + 0.5
            elif por > float(23.75) and por < float(31.25):
                ACS = ACS + 1.0
            elif por >= float(31.25) and por <= float(35):
                ACS = ACS + 0.5
            else:
                ACS = ACS + 0.0
            if esp >= float(10) and esp <= float(20):
                ACS = ACS + 0.5
            elif esp > float(20) and esp < float(40):
                ACS = ACS + 1.0
            elif esp >= float(40) and esp <= float(50):
                ACS = ACS + 0.5
            else:
                ACS = ACS + 0.0
            if tem >= float(50) and tem <= float(87.5):
                ACS = ACS + 0.5
            elif tem > float(87.5) and tem < float(162.5):
                ACS = ACS + 1.0
            elif tem >= float(162.5) and tem <= float(200):
                ACS = ACS + 0.5
            else:
                ACS = ACS + 0.0
            if api >= float(10) and api <= float(17.5):
                ACS = ACS + 0.5
            elif api > float(17.5) and api < float(32.5):
                ACS = ACS + 1.0
            elif api >= float(32.5) and api <= float(40):
                ACS = ACS + 0.5
            else:
                ACS = ACS + 0.0
            if vis >= float(10) and vis <= float(32.5):
                ACS = ACS + 0.5
            elif vis > float(32.5) and vis < float(77.5):
                ACS = ACS + 1.0
            elif vis >= float(77.5) and vis <= float(100):
                ACS = ACS + 0.5
            else:
                ACS = ACS + 0.0
            if sat >= float(30) and sat <= float(40):
                ACS = ACS + 0.5
            elif sat > float(40) and sat < float(60):
                ACS = ACS + 1.0
            elif sat >= float(60) and sat <= float(70):
                ACS = ACS + 0.5
            else:
                ACS = ACS + 0.0
            if prof >= float(1000) and prof <= float(1500):
                ACS = ACS + 0.5
            elif prof > float(1500) and prof < float(2500):
                ACS = ACS + 1.0
            elif prof >= float(2500) and prof <= float(3000):
                ACS = ACS + 0.5
            else:
                ACS = ACS + 0.0
            if roca == "LUTITA":
                ACS = ACS + 1.0
            else:
                ACS = ACS + 0.0
            # INYECCIÓN DE ÁCIDO
            IA = float(0)
            if float(per) >= float(10) and float(per) <= float(250):
                IA = IA + 0.5
            elif float(per) > float(250) and float(per) < float(750):
                IA = IA + 1.0
            elif float(per) >= float(750) and float(per) <= float(1000):
                IA = IA + 0.5
            else:
                IA = IA + 0.0
            if por >= float(10):
                IA = IA + 1.0
            else:
                IA = IA + 0.0
            if esp >= float(10):
                IA = IA + 1
            else:
                IA = IA + 0.0
            if tem >= float(65):
                IA = IA + 1.0
            else:
                IA = IA + 0.0
            if api == 0.0:
                IA = IA + 0.0
            else:
                IA = IA + 1.0
            if vis <= float(100) and vis > float(0):
                IA = IA + 1.0
            else:
                IA = IA + 0.0
            if sat >= float(20) and sat <= float(35):
                IA = IA + 0.5
            elif sat > float(35) and sat < float(65):
                IA = IA + 1.0
            elif sat >= float(65) and sat <= float(80):
                IA = IA + 0.5
            else:
                IA = IA + 0.0
            if prof <= float(3000) and prof > float(0):
                IA = IA + 1.0
            else:
                IA = IA + 0.0
            if roca == "ARENISCA" or roca == "CALIZA":
                IA = IA + 1.0
            else:
                IA = IA + 0.0
            # INYECCIÓN DE MICROEMULSIONES
            MICE = float(0)
            if float(per) >= float(100):
                MICE = MICE + 1.0
            else:
                MICE = MICE + 0.0
            if por >= float(10):
                MICE = MICE + 1.0
            else:
                MICE = MICE + 0.0
            if esp >= float(10):
                MICE = MICE + 1
            else:
                MICE = MICE + 0.0
            if tem <= float(100) and tem > float(0):
                MICE = MICE + 1.0
            else:
                MICE = MICE + 0.0
            if api <= float(30) and api > float(0):
                MICE = MICE + 1.0
            else:
                MICE = MICE + 0.0
            if vis >= float(10):
                MICE = MICE + 1.0
            else:
                MICE = MICE + 0.0
            if sat <= float(50) and sat > float(0):
                MICE = MICE + 1.0
            else:
                MICE = MICE + 0.0
            if prof >= float(1000):
                MICE = MICE + 1.0
            else:
                MICE = MICE + 0.0
            if roca == "ARENISCA":
                MICE = MICE + 1.0
            else:
                MICE = MICE + 0.0
            # INYECCIÓN DE ESPUMAS
            ESP = float(0)
            if float(per) >= float(50) and float(per) <= float(1287.5):
                ESP = ESP + 0.5
            elif float(per) > float(1287.5) and float(per) < float(3762.5):
                ESP = ESP + 1.0
            elif float(per) >= float(3762.5) and float(per) <= float(5000):
                ESP = ESP + 0.5
            else:
                ESP = ESP + 0.0
            if por >= float(20):
                ESP = ESP + 1.0
            else:
                ESP = ESP + 0.0
            if esp <= float(6) and esp > float(0):
                ESP = ESP + 1
            else:
                ESP = ESP + 0.0
            if tem <= float(100) and tem > float(0):
                ESP = ESP + 1.0
            else:
                ESP = ESP + 0.0
            if api >= float(8) and api <= float(12.25):
                ESP = ESP + 0.5
            elif api > float(12.25) and api < float(20.75):
                ESP = ESP + 1.0
            elif api >= float(20.75) and api <= float(25):
                ESP = ESP + 0.5
            else:
                ESP = ESP + 0.0
            if vis >= float(10):
                ESP = ESP + 1.0
            else:
                ESP = ESP + 0.0
            if sat >= float(50):
                ESP = ESP + 1.0
            else:
                ESP = ESP + 0.0
            if prof <= float(1800) and prof > float(0):
                ESP = ESP + 1.0
            else:
                ESP = ESP + 0.0
            if roca == "ARENISCA":
                ESP = ESP + 1.0
            else:
                ESP = ESP + 0.0
            # INYECCIÓN DE SOLUCIONES ACUOSAS DE CO2
            ACO = float(0)
            if float(per) >= float(50) and float(per) <= float(162.5):
                ACO = ACO + 0.5
            elif float(per) > float(162.5) and float(per) < float(387.5):
                ACO = ACO + 1.0
            elif float(per) >= float(387.5) and float(per) <= float(500):
                ACO = ACO + 0.5
            else:
                ACO = ACO + 0.0
            if por >= float(20) and por <= float(22.5):
                ACO = ACO + 0.5
            elif por > float(22.5) and por < float(27.5):
                ACO = ACO + 1.0
            elif por >= float(27.5) and por <= float(30):
                ACO = ACO + 0.5
            else:
                ACO = ACO + 0.0
            if esp >= float(10) and esp <= float(12.5):
                ACO = ACO + 0.5
            elif esp > float(12.5) and esp < float(17.5):
                ACO = ACO + 1.0
            elif esp >= float(17.5) and esp <= float(20):
                ACO = ACO + 0.5
            else:
                ACO = ACO + 0.0
            if tem >= float(60) and tem <= float(67.5):
                ACO = ACO + 0.5
            elif tem > float(67.5) and tem < float(82.5):
                ACO = ACO + 1.0
            elif tem >= float(82.5) and tem <= float(90):
                ACO = ACO + 0.5
            else:
                ACO = ACO + 0.0
            if api >= float(20) and api <= float(26.25):
                ACO = ACO + 0.5
            elif api > float(26.25) and api < float(38.75):
                ACO = ACO + 1.0
            elif api >= float(38.75) and api <= float(45):
                ACO = ACO + 0.5
            else:
                ACO = ACO + 0.0
            if vis >= float(10) and vis <= float(32.5):
                ACO = ACO + 0.5
            elif vis > float(32.5) and vis < float(77.5):
                ACO = ACO + 1.0
            elif vis >= float(77.5) and vis <= float(100):
                ACO = ACO + 0.5
            else:
                ACO = ACO + 0.0
            if sat <= float(60) and sat > float(0):
                ACO = ACO + 1.0
            else:
                ACO = ACO + 0.0
            if prof == 0.0:
                ACO = ACO + 0.0
            else:
                ACO = ACO + 1.0
            if roca == 0.0:
                ACO = ACO + 0.0
            else:
                ACO = ACO + 1.0
            # INYECCIÓN DE NANOHIERRO
            NH = float(0)
            if float(per) >= float(50) and float(per) <= float(112.5):
                NH = NH + 0.5
            elif float(per) > float(112.5) and float(per) < float(237.5):
                NH = NH + 1.0
            elif float(per) >= float(237.5) and float(per) <= float(300):
                NH = NH + 0.5
            else:
                NH = NH + 0.0
            if por >= float(20) and por <= float(21.25):
                NH = NH + 0.5
            elif por > float(21.25) and por < float(23.75):
                NH = NH + 1.0
            elif por >= float(23.75) and por <= float(25):
                NH = NH + 0.5
            else:
                NH = NH + 0.0
            if esp >= float(5):
                NH = NH + 1
            else:
                NH = NH + 0.0
            if tem >= float(40) and tem <= float(45):
                NH = NH + 0.5
            elif tem > float(45) and tem < float(55):
                NH = NH + 1.0
            elif tem >= float(55) and tem <= float(60):
                NH = NH + 0.5
            else:
                NH = NH + 0.0
            if api >= float(20) and api <= float(21.25):
                NH = NH + 0.5
            elif api > float(21.25) and api < float(23.75):
                NH = NH + 1.0
            elif api >= float(23.75) and api <= float(25):
                NH = NH + 0.5
            else:
                NH = NH + 0.0
            if vis >= float(100) and vis <= float(150):
                NH = NH + 0.5
            elif vis > float(150) and vis < float(250):
                NH = NH + 1.0
            elif vis >= float(250) and vis <= float(300):
                NH = NH + 0.5
            else:
                NH = NH + 0.0
            if sat >= float(50) and sat <= float(55):
                NH = NH + 0.5
            elif sat > float(55) and sat <= float(65):
                NH = NH + 1.0
            elif sat >= float(65) and sat <= float(70):
                NH = NH + 0.5
            else:
                NH = NH + 0.0
            if prof >= float(1500):
                NH = NH + 1.0
            else:
                NH = NH + 0.0
            if roca == "ARENISCA" or roca == "CARBONATA":
                NH = NH + 1.0
            else:
                NH = NH + 0.0
            # INYECCIÓN DE NANOARCILLA
            NA = float(0)
            if float(per) >= float(50):
                NA = NA + 1.0
            else:
                NA = NA + 0.0
            if por >= float(15):
                NA = NA + 1.0
            else:
                NA = NA + 0.0
            if esp >= float(10):
                NA = NA + 1
            else:
                NA = NA + 0.0
            if tem >= float(50) and tem <= float(62.5):
                NA = NA + 0.5
            elif tem > float(62.5) and tem < float(87.5):
                NA = NA + 1.0
            elif tem >= float(87.5) and tem <= float(100):
                NA = NA + 0.5
            else:
                NA = NA + 0.0
            if api >= float(20) and api <= float(25):
                NA = NA + 0.5
            elif api > float(25) and api < float(35):
                NA = NA + 1.0
            elif api >= float(35) and api <= float(40):
                NA = NA + 0.5
            else:
                NA = NA + 0.0
            if vis >= float(10):
                NA = NA + 1.0
            else:
                NA = NA + 0.0
            if sat <= float(70) and sat > float(0):
                NA = NA + 1.0
            else:
                NA = NA + 0.0
            if prof <= float(2000) and prof > float(0):
                NA = NA + 1.0
            else:
                NA = NA + 0.0
            if roca == 0.0:
                NA = NA + 0.0
            else:
                NA = NA + 1.0
            CIS = CIS * 100 / 9
            THAI = THAI * 100 / 9
            VAP = VAP * 100 / 9
            HAP = HAP * 100 / 9
            SD = SD * 100 / 9
            SAGD = SAGD * 100 / 9
            COS = COS * 100 / 9
            COV = COV * 100 / 9
            IN = IN * 100 / 9
            ASP = ASP * 100 / 9
            SP = SP * 100 / 9
            MP = MP * 100 / 9
            GEL = GEL * 100 / 9
            MIC = MIC * 100 / 9
            HW = HW * 100 / 9
            WAG = WAG * 100 / 9
            MICF = MICF * 100 / 9
            ACS = ACS * 100 / 9
            IA = IA * 100 / 9
            MICE = MICE * 100 / 9
            ESP = ESP * 100 / 9
            ACO = ACO * 100 / 9
            NH = NH * 100 / 9
            NA = NA * 100 / 9
            diccionario = {"Combustión in Situ.": CIS, "Toe to Heel Air Injection.": THAI,
                           "Inyección convencional de Vapor.": VAP,
                           "Método Huff & Puff.": HAP, "Método Steam Drive.": SD,
                           "Método Steam Assisted Gravity Drainage.": SAGD,
                           "Inyección de CO2 Supercrítico.": COS, "Inyección de CO2 Convencional.": COV,
                           "Inyección de N2.": IN,
                           "Inyección ASP.": ASP, "Inyección SP.": SP, "Inyección MP.": MP, "Inyección de geles.": GEL,
                           "Inyección de microorganismos.": MIC, "Hot Waterflooding.": HW,
                           "Water Alternating Gas.": WAG,
                           "Inyección de microfluidos.": MICF, "Inyección de Agentes de cambio de fase.": ACS,
                           "Inyección de ácido.": IA, "Inyección de microemulsiones.": MICE,
                           "Inyección de espumas.": ESP,
                           "Inyección de soluciones acuosas de CO2.": ACO, "Inyección de nanohierro.": NH,
                           "Inyección de nanoarcilla.": NA}
            sorted_d = dict(sorted(diccionario.items(), key=lambda x: x[1], reverse=True))
            st.write("")
            st.write("")
            st.write("")
            st.write(
                "A continuación, se mostrará una lista ordenada de forma descendente desde la técnica más idónea para su pozo hasta la menos recomendable con su respectiva probabilidad de éxito.")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            k = 1
            for i in sorted_d:
                valor = sorted_d[i]
                n2 = round(valor, 2)
                st.write("Puesto #", k, ":", i, "Probabilidad de éxito:", n2, "%", )
                k = k + 1
            diccionario_noordenado = dict(sorted(diccionario.items(), key=lambda x: x[1]))
            ejex = list(diccionario_noordenado.keys())
            ejey = list(diccionario_noordenado.values())

            fig, ax = plt.subplots()
            ax.barh(ejex, ejey)
            ax.set_title('Idoneidad de técnicas de EOR')
            ax.set_xlabel('Valor de probabilidad de éxito')
            ax.set_ylabel('Método')
            st.write("")
            st.write("")
            st.write("")
            st.pyplot(fig)

    st.write("")
    st.write("")
    st.write("")

    # Panel para ingreso manual de datos
    with st.sidebar.expander("Resultados"):

        por = st.sidebar.number_input("Porosidad en porcentaje:", value=0, min_value=0, max_value=100)
        per= st.sidebar.number_input("Permeabilidad en mD:", value=0, min_value=0)
        api = st.sidebar.number_input("Gravedad API:", value=0, min_value=0)
        sat = st.sidebar.number_input("Saturación en porcentaje:", value=0, min_value=0, max_value=100)
        tem = st.sidebar.number_input("Temperatura en °C:", value=0, min_value=0)
        prof = st.sidebar.number_input("Profundidad en metros:", value=0, min_value=0)
        esp = st.sidebar.number_input("Espesor en metros:", value=0, min_value=0)
        vis = st.sidebar.number_input("Viscosidad en cp:", value=0, min_value=0)
        roca = st.sidebar.selectbox("Tipo de roca:", ["","No se cuenta con información", "ARENISCA", "LUTITA", "DOLOMITA", "CALIZA", "CARBONATA"])
        if st.sidebar.button("Guardar valores", key="boton_guardar"):
            st.sidebar.success("Guardado exitosamente")


        st.write(f"Porosidad = {por} %")
        st.write(f"Permeabilidad = {per} mD")
        st.write(f"Gravedad API = {api}")
        st.write(f"Saturación = {sat} %")
        st.write(f"Temperatura = {tem} °C")
        st.write(f"Profundidad = {prof} metros")
        st.write(f"Espesor = {esp} metros")
        st.write(f"Viscosidad = {vis} cp")
        st.write(f"Tipo de roca = {roca}")

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        CIS = float(0)
        if float(per) >= float(10) and float(per) <= float(132.5):
            CIS = CIS + 0.5
        elif float(per) > float(132.5) and float(per) < float(377.5):
            CIS = CIS + 1.0
        elif float(per) >= float(377.5) and float(per) <= float(500):
            CIS = CIS + 0.5
        else:
            CIS = CIS + 0.0
        if por >= float(15) and por <= float(20):
            CIS = CIS + 0.5
        elif por > float(20) and por < float(30):
            CIS = CIS + 1.0
        elif por >= float(30) and por <= float(35):
            CIS = CIS + 0.5
        else:
            CIS = CIS + 0.0
        if esp >= float(5) and esp <= float(91.25):
            CIS = CIS + 0.5
        elif esp > float(91.25) and esp < float(263.75):
            CIS = CIS + 1
        elif esp >= float(263.75) and esp <= float(350):
            CIS = CIS + 0.5
        else:
            CIS = CIS + 0.0
        if tem >= float(150) and tem <= float(200):
            CIS = CIS + 0.5
        elif tem > float(200) and tem< float(300):
            CIS = CIS + 1.0
        elif tem >= float(300) and tem <= float(350):
            CIS = CIS + 0.5
        else:
            CIS = CIS + 0.0
        if api >= float(15):
            CIS = CIS + 1.0
        else:
            CIS = CIS + 0.0
        if vis >= float(100) and vis <= float(2575):
            CIS = CIS + 0.5
        elif vis > float(2575) and vis < float(7525):
            CIS = CIS + 1.0
        elif vis >= float(7525) and vis <= float(10000):
            CIS = CIS + 0.5
        else:
            CIS = CIS + 0.0
        if sat >= float(30):
            CIS = CIS + 1.0
        else:
            CIS = CIS + 0.0
        if prof >= float(500) and prof <= float(3500):
            CIS = CIS + 1.0
        elif prof >= float(3500):
            CIS = CIS + 0.5
        else:
            CIS = CIS + 0.0
        if roca == "ARENISCA":
            CIS = CIS + 1.0
        else:
            CIS = CIS + 0.0
        # THAI
        THAI = float(0)
        if float(per) >= float(10) and float(per) <= float(57.5):
            THAI = THAI + 0.5
        elif float(per) > float(57.5) and float(per) < float(152.5):
            THAI = THAI + 1.0
        elif float(per) >= float(152.5) and float(per) <= float(200):
            THAI = THAI + 0.5
        else:
            THAI = THAI + 0.0
        if por >= float(20) and por <= float(23.75):
            THAI = THAI + 0.5
        elif por > float(23.75) and por < float(31.25):
            THAI = THAI + 1.0
        elif por >= float(31.25) and por <= float(35):
            THAI = THAI + 0.5
        else:
            THAI = THAI + 0.0
        if esp >= float(5) and esp <= float(11.25):
            THAI = THAI + 0.5
        elif esp > float(11.25) and esp < float(23.75):
            THAI = THAI + 1
        elif esp >= float(23.75) and esp <= float(30):
            THAI = THAI + 0.5
        else:
            THAI = THAI + 0.0
        if tem >= float(300) and tem <= float(325):
            THAI = THAI + 0.5
        elif tem > float(325) and tem < float(375):
            THAI = THAI + 1.0
        elif tem >= float(375) and tem <= float(400):
            THAI = THAI + 0.5
        else:
            THAI = THAI + 0.0
        if api <= float(12) and api > float(0):
            THAI = THAI + 1.0
        else:
            THAI = THAI + 0.0
        if vis >= float(50) and vis <= float(12537.5):
            THAI = THAI + 0.5
        elif vis > float(12537.5) and vis < float(37512.5):
            THAI = THAI + 1.0
        elif vis >= float(37512.5) and vis <= float(50000):
            THAI = THAI + 0.5
        else:
            THAI = THAI + 0.0
        if sat >= float(20):
            THAI = THAI + 1.0
        else:
            THAI = THAI + 0.0
        if prof >= float(200) and prof <= float(3500):
            THAI = THAI + 1.0
        elif prof >= float(3500):
            THAI = THAI + 0.5
        else:
            THAI = THAI + 0.0
        if roca == "ARENISCA" or roca == "CARBONATA":
            THAI = THAI + 1.0
        else:
            THAI = THAI + 0.0
        # INYECCIÓN DE VAPOR
        VAP = float(0)
        if float(per) >= float(50) and float(per) <= float(162.5):
            VAP = VAP + 0.5
        elif float(per) > float(162.5) and float(per) < float(387.5):
            VAP = VAP + 1.0
        elif float(per) >= float(387.5) and float(per) <= float(500):
            VAP = VAP + 0.5
        else:
            VAP = VAP + 0.0
        if por >= float(20) and por <= float(22.5):
            VAP = VAP + 0.5
        elif por > float(22.5) and por < float(27.5):
            VAP = VAP + 1.0
        elif por >= float(27.5) and por <= float(30):
            VAP = VAP + 0.5
        else:
            VAP = VAP + 0.0
        if esp >= float(20) and esp <= float(25):
            VAP = VAP + 0.5
        elif esp > float(25) and esp <= float(35):
            VAP = VAP + 1
        elif esp >= float(35) and esp <= float(40):
            VAP = VAP + 0.5
        else:
            VAP = VAP + 0.0
        if tem >= float(200) and tem <= float(212.5):
            VAP = VAP + 0.5
        elif tem > float(212.5) and tem < float(237.5):
            VAP = VAP + 1.0
        elif tem >= float(237.5) and tem <= float(250):
            VAP = VAP + 0.5
        else:
            VAP = VAP + 0.0
        if api >= float(8) and api <= float(11):
            VAP = VAP + 0.5
        elif api > float(14) and api < float(17):
            VAP = VAP + 1.0
        elif api >= float(17) and api <= float(20):
            VAP = VAP + 0.5
        else:
            VAP = VAP + 0.0
        if vis >= float(10) and vis <= float(57.5):
            VAP = VAP + 0.5
        elif vis > float(57.5) and vis < float(152.5):
            VAP = VAP + 1.0
        elif vis >= float(152.5) and vis <= float(200):
            VAP = VAP + 0.5
        else:
            VAP = VAP + 0.0
        if sat >= float(50):
            VAP = VAP + 1.0
        elif sat >= float(30) and sat < float(50):
            VAP = VAP + 0.5
        else:
            VAP = VAP + 0.0
        if prof >= float(600) and prof <= float(700):
            VAP = VAP + 0.5
        elif prof > float(700) and prof < float(900):
            VAP = VAP + 1.0
        elif prof >= float(900) and prof <= float(1000):
            VAP = VAP + 0.5
        else:
            VAP = VAP + 0.0
        if roca == "ARENISCA":
            VAP = VAP + 1.0
        else:
            VAP = VAP + 0.0
        # HUFF AND PUFF
        HAP = float(0)
        if float(per) <= float(100) and float(per) >= float(77.5):
            HAP = HAP + 0.5
        elif float(per) < float(77.5) and float(per) > float(32.5):
            HAP = HAP + 1.0
        elif float(per) <= float(32.5) and float(per) >= float(10):
            HAP = HAP + 0.5
        else:
            HAP = HAP + 0.0
        if por >= float(10) and por <= float(13.75):
            HAP = HAP + 0.5
        elif por > float(13.75) and por < float(21.25):
            HAP = HAP + 1.0
        elif por >= float(21.25) and por <= float(25):
            HAP = HAP + 0.5
        else:
            HAP = HAP + 0.0
        if esp >= float(10):
            HAP = HAP + 1
        else:
            HAP = HAP + 0.0
        if tem >= float(90):
            HAP = HAP + 1.0
        else:
            HAP = HAP + 0.0
        if api >= float(15) and api <= float(23.75):
            HAP = HAP + 0.5
        elif api > float(23.75) and api < float(41.25):
            HAP = HAP + 1.0
        elif api >= float(41.25) and api <= float(50):
            HAP = HAP + 0.5
        else:
            HAP = HAP + 0.0
        if vis >= float(10) and vis <= float(382.5):
            HAP = HAP + 0.5
        elif vis > float(382.5) and vis < float(1127.5):
            HAP = HAP + 1.0
        elif vis >= float(1127.5) and vis <= float(1500):
            HAP = HAP + 0.5
        else:
            HAP = HAP + 0.0
        if sat >= float(50):
            HAP = HAP + 1.0
        else:
            HAP = HAP + 0.0
        if prof >= float(600):
            HAP = HAP + 1.0
        else:
            HAP = HAP + 0.0
        if roca == "ARENISCA":
            HAP = HAP + 1.0
        else:
            HAP = HAP + 0.0
        # STEAM DRIVE
        SD = float(0)
        if float(per) >= float(50) and float(per) <= float(537.5):
            SD = SD + 0.5
        elif float(per) > float(537.5) and float(per) < float(1512.5):
            SD = SD + 1.0
        elif float(per) >= float(1512.5) and float(per) <= float(2000):
            SD = SD + 0.5
        else:
            SD = SD + 0.0
        if por >= float(15) and por <= float(18.75):
            SD = SD + 0.5
        elif por > float(18.75) and por < float(26.25):
            SD = SD + 1.0
        elif por >= float(26.25) and por <= float(30):
            SD = SD + 0.5
        else:
            SD = SD + 0.0
        if esp >= float(10):
            SD = SD + 1
        else:
            SD = SD + 0.0
        if tem >= float(150) and tem <= float(187.5):
            SD = SD + 0.5
        elif tem > float(187.5) and tem < float(262.5):
            SD = SD + 1.0
        elif tem >= float(262.5) and tem <= float(300):
            SD = SD + 0.5
        else:
            SD = SD + 0.0
        if api >= float(12):
            SD = SD + 1.0
        else:
            SD = SD + 0.0
        if vis >= float(10) and vis <= float(2507.5):
            SD = SD + 0.5
        elif vis > float(2507.5) and vis < float(7502.5):
            SD = SD + 1.0
        elif vis >= float(7502.5) and vis <= float(10000):
            SD = SD + 0.5
        else:
            SD = SD + 0.0
        if sat >= float(50):
            SD = SD + 1.0
        else:
            SD = SD + 0.0
        if prof >= float(90) and prof <= float(442.5):
            SD = SD + 0.5
        elif prof > float(442.5) and prof < float(1147.5):
            SD = SD + 1.0
        elif prof >= float(1147.5) and prof <= float(1500):
            SD = SD + 0.5
        else:
            SD = SD + 0.0
        if roca == "ARENISCA":
            SD = SD + 1.0
        else:
            SD = SD + 0.0
        # SAGD
        SAGD = float(0)
        if float(per) >= float(1) and float(per) <= float(125):
            SAGD = SAGD + 0.5
        elif float(per) > float(125) and float(per) < float(375):
            SAGD = SAGD + 1.0
        elif float(per) >= float(375) and float(per) <= float(500):
            SAGD = SAGD + 0.5
        else:
            SAGD = SAGD + 0.0
        if por >= float(20) and por <= float(23.75):
            SAGD = SAGD + 0.5
        elif por > float(23.75) and por < float(31.25):
            SAGD = SAGD + 1.0
        elif por >= float(31.25) and por <= float(35):
            SAGD = SAGD + 0.5
        else:
            SAGD = SAGD + 0.0
        if esp >= float(5):
            SAGD = SAGD + 1
        else:
            SAGD = SAGD + 0.0
        if tem >= float(200) and tem <= float(225):
            SAGD = SAGD + 0.5
        elif tem > float(225) and tem < float(275):
            SAGD = SAGD + 1.0
        elif tem >= float(275) and tem <= float(300):
            SAGD = SAGD + 0.5
        else:
            SAGD = SAGD + 0.0
        if api <= float(15) and api > float(0):
            SAGD = SAGD + 1.0
        else:
            SAGD = SAGD + 0.0
        if vis >= float(10000):
            SAGD = SAGD + 1.0
        else:
            SAGD = SAGD + 0.0
        if sat >= float(70):
            SAGD = SAGD + 1.0
        else:
            SAGD = SAGD + 0.0
        if prof <= float(1000) and prof > float(0):
            SAGD = SAGD + 1.0
        else:
            SAGD = SAGD + 0.0
        if roca == "ARENISCA":
            SAGD = SAGD + 1.0
        else:
            SAGD = SAGD + 0.0
        # INYECCIÓN DE CO2 SUPERCRÍTICO
        COS = float(0)
        if float(per) >= float(50) and float(per) <= float(287.5):
            COS = COS + 0.5
        elif float(per) > float(287.5) and float(per) < float(762.5):
            COS = COS + 1.0
        elif float(per) >= float(762.5) and float(per) <= float(1000):
            COS = COS + 0.5
        else:
            COS = COS + 0.0
        if por >= float(20) and por <= float(22.5):
            COS = COS + 0.5
        elif por > float(22.5) and por < float(27.5):
            COS = COS + 1.0
        elif por >= float(27.5) and por <= float(30):
            COS = COS + 0.5
        else:
            COS = COS + 0.0
        if esp >= float(3) and esp <= float(4):
            COS = COS + 1
        else:
            COS = COS + 0.0
        if tem >= float(40) and tem <= float(45):
            COS = COS + 0.5
        elif tem > float(45) and tem < float(55):
            COS = COS + 1.0
        elif tem >= float(55) and tem <= float(60):
            COS = COS + 0.5
        else:
            COS = COS + 0.0
        if api <= float(20) and api > float(0):
            COS = COS + 1.0
        else:
            COS = COS + 0.0
        if vis >= float(1000):
            COS = COS + 1.0
        else:
            COS = COS + 0.0
        if sat >= float(30):
            COS = COS + 1.0
        else:
            COS = COS + 0.0
        if prof == float(0):
            COS = COS + 0.0
        else:
            COS = COS + 1.0  # Profundidad no relevante
        if roca == float(0):
            COS = COS + 0.0
        else:
            COS = COS + 1.0  # Tipo de roca no relevante
        # INYECCIÓN DE CO2 CONVENCIONAL
        COV = float(0)
        if float(per) >= float(10):
            COV = COV + 1.0
        else:
            COV = COV + 0.0
        if por >= float(10):
            COV = COV + 1.0
        else:
            COV = COV + 0.0
        if esp >= float(3):
            COV = COV + 1
        else:
            COV = COV + 0.0
        if tem >= float(60) and tem <= float(132.5):
            COV = COV + 0.5
        elif tem > float(132.5) and tem < float(277.5):
            COV = COV + 1.0
        elif tem >= float(277.5) and tem <= float(350):
            COV = COV + 0.5
        else:
            COV = COV + 0.0
        if api >= float(15) and api <= float(21.25):
            COV = COV + 0.5
        elif api > float(21.25) and api < float(33.75):
            COV = COV + 1.0
        elif api >= float(33.75) and api <= float(40):
            COV = COV + 0.5
        else:
            COV = COV + 0.0
        if vis >= float(50):
            COV = COV + 1.0
        else:
            COV = COV + 0.0
        if sat <= float(50) and sat > float(0):
            COV = COV + 1.0
        else:
            COV = COV + 0.0
        if prof <= float(1500) and prof > float(0):
            COV = COV + 1.0
        else:
            COV = COV + 0.0
        if roca == "ARENISCA" or roca == "CALIZA":
            COV = COV + 1.0
        else:
            COV = COV + 0.0
        # INYECCIÓN DE N2 CONVENCIONAL
        IN = float(0)
        if float(per) >= float(50) and float(per) <= float(287.5):
            IN = IN + 0.5
        elif float(per) > float(287.5) and float(per) < float(762.5):
            IN = IN + 1.0
        elif float(per) >= float(762.5) and float(per) <= float(1000):
            IN = IN + 0.5
        else:
            IN = IN + 0.0
        if por >= float(20) and por <= float(22.5):
            IN = IN + 0.5
        elif por > float(22.5) and por < float(27.5):
            IN = IN + 1.0
        elif por >= float(27.5) and por <= float(30):
            IN = IN + 0.5
        else:
            IN = IN + 0.0
        if esp >= float(10):
            IN = IN + 1
        else:
            IN = IN + 0.0
        if tem >= float(60) and tem <= float(82.5):
            IN = IN + 0.5
        elif tem > float(82.5) and tem < float(127.5):
            IN = IN + 1.0
        elif tem >= float(127.5) and tem <= float(150):
            IN = IN + 0.5
        else:
            IN = IN + 0.0
        if api >= float(15) and api <= float(20):
            IN = IN + 0.5
        elif api > float(20) and api < float(30):
            IN = IN + 1.0
        elif api >= float(30) and api <= float(35):
            IN = IN + 0.5
        else:
            IN = IN + 0.0
        if vis >= float(100) and vis <= float(2575):
            IN = IN + 0.5
        elif vis > float(2575) and vis < float(7525):
            IN = IN + 1.0
        elif vis >= float(7525) and vis <= float(10000):
            IN = IN + 0.5
        else:
            IN = IN + 0.0
        if sat >= float(50) and sat <= float(55):
            IN = IN + 0.5
        elif sat > float(55) and sat < float(65):
            IN = IN + 1.0
        elif sat >= float(65) and sat <= float(70):
            IN = IN + 0.5
        else:
            IN = IN + 0.0
        if prof >= float(1000):
            IN = IN + 1.0
        else:
            IN = IN + 0.0
        if roca == "ARENISCA" or roca == "CALIZA":
            IN = IN + 1.0
        else:
            IN = IN + 0.0
        # ASP
        ASP = float(0)
        if float(per) >= float(10) and float(per) <= float(257.5):
            ASP = ASP + 0.5
        elif float(per) > float(257.5) and float(per) < float(752.5):
            ASP = ASP + 1.0
        elif float(per) >= float(752.5) and float(per) <= float(1000):
            ASP = ASP + 0.5
        else:
            ASP = ASP + 0.0
        if por >= float(20) and por <= float(23.75):
            ASP = ASP + 0.5
        elif por > float(23.75) and por < float(31.25):
            ASP = ASP + 1.0
        elif por >= float(31.25) and por <= float(35):
            ASP = ASP + 0.5
        else:
            ASP = ASP + 0.0
        if esp >= float(10):
            ASP = ASP + 1
        else:
            ASP = ASP + 0.0
        if tem >= float(60) and tem <= float(67.5):
            ASP = ASP + 0.5
        elif tem > float(67.5) and tem < float(82.5):
            ASP = ASP + 1.0
        elif tem >= float(82.5) and tem <= float(90):
            ASP = ASP + 0.5
        else:
            ASP = ASP + 0.0
        if api >= float(10) and api <= float(15):
            ASP = ASP + 0.5
        elif api > float(15) and api < float(25):
            ASP = ASP + 1.0
        elif api >= float(25) and api <= float(30):
            ASP = ASP + 0.5
        else:
            ASP = ASP + 0.0
        if vis >= float(300):
            ASP = ASP + 1.0
        else:
            ASP = ASP + 0.0
        if sat >= float(70):
            ASP = ASP + 1.0
        else:
            ASP = ASP + 0.0
        if prof >= float(1000) and prof <= float(1500):
            ASP = ASP + 0.5
        elif prof > float(1500) and prof < float(2500):
            ASP = ASP + 1.0
        elif prof >= float(2500) and prof <= float(3000):
            ASP = ASP + 0.5
        else:
            ASP = ASP + 0.0
        if roca == "ARENISCA" or roca == "CARBONATA":
            ASP = ASP + 1.0
        else:
            ASP = ASP + 0.0
        # SP
        SP = float(0)
        if float(per) >= float(1):
            SP = SP + 1.0
        else:
            SP = SP + 0.0
        if por >= float(10) and por <= float(15):
            SP = SP + 0.5
        elif por > float(15) and por < float(25):
            SP = SP + 1.0
        elif por >= float(25) and por <= float(30):
            SP = SP + 0.5
        else:
            SP = SP + 0.0
        if esp >= float(10):
            SP = SP + 1
        else:
            SP = SP + 0.0
        if tem <= float(200) and tem > float(0):
            SP = SP + 1.0
        else:
            SP = SP + 0.0
        if api >= float(10) and api <= float(17.5):
            SP = SP + 0.5
        elif api > float(17.5) and api < float(32.5):
            SP = SP + 1.0
        elif api >= float(32.5) and api <= float(40):
            SP = SP + 0.5
        else:
            SP = SP + 0.0
        if vis >= float(100):
            SP = SP + 1.0
        else:
            SP = SP + 0.0
        if sat >= float(30):
            SP = SP + 1.0
        else:
            SP = SP + 0.0
        if prof <= float(2500) and prof > float(0):
            SP = SP + 1.0
        else:
            SP = SP + 0.0
        if roca == "ARENISCA" or roca == "CARBONATA":
            SP = SP + 1.0
        else:
            SP = SP + 0.0
        # MP
        MP = float(0)
        if float(per) <= float(50) and per > float(0):
            MP = MP + 1.0
        else:
            MP = MP + 0.0
        if por >= float(20):
            MP = MP + 1.0
        else:
            MP = MP + 0.0
        if esp >= float(10):
            MP = MP + 1
        else:
            MP = MP + 0.0
        if tem <= float(100) and tem > float(0):
            MP = MP + 1.0
        else:
            MP = MP + 0.0
        if api >= float(10) and api <= float(17.5):
            MP = MP + 0.5
        elif api > float(17.5) and api < float(32.5):
            MP = MP + 1.0
        elif api >= float(32.5) and api <= float(40):
            MP = MP + 0.5
        else:
            MP = MP + 0.0
        if vis >= float(10):
            MP = MP + 1.0
        else:
            MP = MP + 0.0
        if sat >= float(30):
            MP = MP + 1.0
        else:
            MP = MP + 0.0
        if prof <= float(1500) and prof > float(0):
            MP = MP + 1.0
        else:
            MP = MP + 0.0
        if roca == "ARENISCA" or roca == "CARBONATA":
            MP = MP + 1.0
        else:
            MP = MP + 0.0
        # INYECCIÓN DE GELES
        GEL = float(0)
        if float(per) >= float(10) and float(per) <= float(132.5):
            GEL = GEL + 0.5
        elif float(per) > float(132.5) and float(per) < float(377.5):
            GEL = GEL + 1.0
        elif float(per) >= float(377.5) and float(per) <= float(500):
            GEL = GEL + 0.5
        else:
            GEL = GEL + 0.0
        if por >= float(10):
            GEL = GEL + 1.0
        else:
            GEL = GEL + 0.0
        if esp >= float(10):
            GEL = GEL + 1
        else:
            GEL = GEL + 0.0
        if tem >= float(40) and tem <= float(50):
            GEL = GEL + 0.5
        elif tem > float(50) and tem < float(70):
            GEL = GEL + 1.0
        elif tem >= float(70) and tem <= float(80):
            GEL = GEL + 0.5
        else:
            GEL = GEL + 0.0
        if api >= float(20) and api <= float(25):
            GEL = GEL + 0.5
        elif api > float(25) and api < float(35):
            GEL = GEL + 1.0
        elif api >= float(35) and api <= float(40):
            GEL = GEL + 0.5
        else:
            GEL = GEL + 0.0
        if vis >= float(5):
            GEL = GEL + 1.0
        else:
            GEL = GEL + 0.0
        if sat >= float(30):
            GEL = GEL + 1.0
        else:
            GEL = GEL + 0.0
        if prof >= float(1000):
            GEL = GEL + 1.0
        else:
            GEL = GEL + 0.0
        if roca == "ARENISCA" or roca == "CALIZA" or roca == "DOLOMITA":
            GEL = GEL + 1.0
        else:
            GEL = GEL + 0.0
        # INYECCIÓN DE MICROORGANISMOS
        MIC = float(0)
        if float(per) >= float(10) and float(per) <= float(257.5):
            MIC = MIC + 0.5
        elif float(per) > float(257.5) and float(per) < float(752.5):
            MIC = MIC + 1.0
        elif float(per) >= float(752.5) and float(per) <= float(1000):
            MIC = MIC + 0.5
        else:
            MIC = MIC + 0.0
        if por >= float(10) and por <= float(15):
            MIC = MIC + 0.5
        elif por > float(15) and por < float(25):
            MIC = MIC + 1.0
        elif por >= float(25) and por <= float(30):
            MIC = MIC + 0.5
        else:
            MIC = MIC + 0.0
        if esp >= float(10):
            MIC = MIC + 1
        else:
            MIC = MIC + 0.0
        if tem >= float(30) and tem <= float(42.5):
            MIC = MIC + 0.5
        elif tem > float(42.5) and tem < float(67.5):
            MIC = MIC + 1.0
        elif tem >= float(67.5) and tem <= float(80):
            MIC = MIC + 0.5
        else:
            MIC = MIC + 0.0
        if api >= float(20) and api <= float(25):
            MIC = MIC + 0.5
        elif api > float(25) and api < float(35):
            MIC = MIC + 1.0
        elif api >= float(35) and api <= float(40):
            MIC = MIC + 0.5
        else:
            MIC = MIC + 0.0
        if vis <= float(100) and vis > float(0):
            MIC = MIC + 1.0
        else:
            MIC = MIC + 0.0
        if sat <= float(60) and sat > float(0):
            MIC = MIC + 1.0
        else:
            MIC = MIC + 0.0
        if prof <= float(3000) and prof > float(0):
            MIC = MIC + 1.0
        else:
            MIC = MIC + 0.0
        if roca == "ARENISCA":
            MIC = MIC + 1.0
        else:
            MIC = MIC + 0.0
        # HOT WATERFLOODING
        HW = float(0)
        if float(per) >= float(50) and float(per) <= float(287.5):
            HW = HW + 0.5
        elif float(per) > float(287.5) and float(per) < float(762.5):
            HW = HW + 1.0
        elif float(per) >= float(762.5) and float(per) <= float(1000):
            HW = HW + 0.5
        else:
            HW = HW + 0.0
        if por >= float(15):
            HW = HW + 1.0
        else:
            HW = HW + 0.0
        if esp >= float(10):
            HW = HW + 1
        else:
            HW = HW + 0.0
        if tem >= float(60):
            HW = HW + 1.0
        else:
            HW = HW + 0.0
        if api >= float(8) and api <= float(12.25):
            HW = HW + 0.5
        elif api > float(12.25) and api < float(20.75):
            HW = HW + 1.0
        elif api >= float(20.75) and api <= float(25):
            HW = HW + 0.5
        else:
            HW = HW + 0.0
        if vis >= float(100):
            HW = HW + 1.0
        else:
            HW = HW + 0.0
        if sat >= float(50):
            HW = HW + 1.0
        else:
            HW = HW + 0.0
        if prof >= float(1000):
            HW = HW + 1.0
        else:
            HW = HW + 0.0
        if roca == "ARENISCA" or roca == "CARBONATA":
            HW = HW + 1.0
        else:
            HW = HW + 0.0
        # WAG
        WAG = float(0)
        if float(per) >= float(1) and float(per) <= float(500):
            WAG = WAG + 1.0
        else:
            WAG = WAG + 0.0
        if por >= float(15):
            WAG = WAG + 1.0
        else:
            WAG = WAG + 0.0
        if esp >= float(10):
            WAG = WAG + 1
        else:
            WAG = WAG + 0.0
        if tem >= float(40):
            WAG = WAG + 1.0
        else:
            WAG = WAG + 0.0
        if api >= float(10) and api <= float(17.5):
            WAG = WAG + 0.5
        elif api > float(17.5) and api < float(32.5):
            WAG = WAG + 1.0
        elif api >= float(32.5) and api <= float(40):
            WAG = WAG + 0.5
        else:
            WAG = WAG + 0.0
        if vis >= float(50):
            WAG = WAG + 1.0
        else:
            WAG = WAG + 0.0
        if sat >= float(50):
            WAG = WAG + 1.0
        else:
            WAG = WAG + 0.0
        if prof >= float(500):
            WAG = WAG + 1.0
        else:
            WAG = WAG + 0.0
        if roca == "ARENISCA" or roca == "CARBONATA":
            WAG = WAG + 1.0
        else:
            WAG = WAG + 0.0
        # INYECCIÓN DE MICROFLUIDOS
        MICF = float(0)
        if float(per) >= float(1) and float(per) <= float(1000):
            MICF = MICF + 1.0
        else:
            MICF = MICF + 0.0
        if por >= float(20) and por <= float(23.75):
            MICF = MICF + 0.5
        elif por > float(23.75) and por < float(31.25):
            MICF = MICF + 1.0
        elif por >= float(31.25) and por <= float(35):
            MICF = MICF + 0.5
        else:
            MICF = MICF + 0.0
        if esp >= float(10) and esp <= float(20):
            MICF = MICF + 0.5
        elif esp > float(20) and esp < float(40):
            MICF = MICF + 1.0
        elif esp >= float(40) and esp <= float(50):
            MICF = MICF + 0.5
        else:
            MICF = MICF + 0.0
        if tem >= float(30) and tem <= float(40):
            MICF = MICF + 0.5
        elif tem > float(40) and tem < float(60):
            MICF = MICF + 1.0
        elif tem >= float(60) and tem <= float(70):
            MICF = MICF + 0.5
        else:
            MICF = MICF + 0.0
        if api >= float(20) and api <= float(27.5):
            MICF = MICF + 0.5
        elif api > float(27.5) and api < float(42.5):
            MICF = MICF + 1.0
        elif api >= float(42.5) and api <= float(50):
            MICF = MICF + 0.5
        else:
            MICF = MICF + 0.0
        if vis <= float(100) and vis > float(0):
            MICF = MICF + 1.0
        else:
            MICF = MICF + 0.0
        if sat >= float(60) and sat <= float(65):
            MICF = MICF + 0.5
        elif sat > float(65) and sat < float(75):
            MICF = MICF + 1.0
        elif sat >= float(75) and sat <= float(80):
            MICF = MICF + 0.5
        else:
            MICF = MICF + 0.0
        if prof >= float(500) and prof <= float(1125):
            MICF = MICF + 0.5
        elif prof > float(1125) and prof < float(2375):
            MICF = MICF + 1.0
        elif prof >= float(2375) and prof <= float(3000):
            MICF = MICF + 0.5
        else:
            MICF = MICF + 0.0
        if roca == "ARENISCA" or roca == "CALIZA":
            MICF = MICF + 1.0
        else:
            MICF = MICF + 0.0
        # INYECCIÓN DE AGENTES DE CAMBIO DE FASE
        ACS = float(0)
        if float(per) >= float(10) and float(per) <= float(250):
            ACS = ACS + 0.5
        elif float(per) > float(250) and float(per) < float(750):
            ACS = ACS + 1.0
        elif float(per) >= float(750) and float(per) <= float(1000):
            ACS = ACS + 0.5
        else:
            ACS = ACS + 0.0
        if por >= float(20) and por <= float(23.75):
            ACS = ACS + 0.5
        elif por > float(23.75) and por < float(31.25):
            ACS = ACS + 1.0
        elif por >= float(31.25) and por <= float(35):
            ACS = ACS + 0.5
        else:
            ACS = ACS + 0.0
        if esp >= float(10) and esp <= float(20):
            ACS = ACS + 0.5
        elif esp > float(20) and esp < float(40):
            ACS = ACS + 1.0
        elif esp >= float(40) and esp <= float(50):
            ACS = ACS + 0.5
        else:
            ACS = ACS + 0.0
        if tem >= float(50) and tem <= float(87.5):
            ACS = ACS + 0.5
        elif tem > float(87.5) and tem < float(162.5):
            ACS = ACS + 1.0
        elif tem >= float(162.5) and tem <= float(200):
            ACS = ACS + 0.5
        else:
            ACS = ACS + 0.0
        if api >= float(10) and api <= float(17.5):
            ACS = ACS + 0.5
        elif api > float(17.5) and api < float(32.5):
            ACS = ACS + 1.0
        elif api >= float(32.5) and api <= float(40):
            ACS = ACS + 0.5
        else:
            ACS = ACS + 0.0
        if vis >= float(10) and vis <= float(32.5):
            ACS = ACS + 0.5
        elif vis > float(32.5) and vis < float(77.5):
            ACS = ACS + 1.0
        elif vis >= float(77.5) and vis <= float(100):
            ACS = ACS + 0.5
        else:
            ACS = ACS + 0.0
        if sat >= float(30) and sat <= float(40):
            ACS = ACS + 0.5
        elif sat > float(40) and sat < float(60):
            ACS = ACS + 1.0
        elif sat >= float(60) and sat <= float(70):
            ACS = ACS + 0.5
        else:
            ACS = ACS + 0.0
        if prof >= float(1000) and prof <= float(1500):
            ACS = ACS + 0.5
        elif prof > float(1500) and prof < float(2500):
            ACS = ACS + 1.0
        elif prof >= float(2500) and prof <= float(3000):
            ACS = ACS + 0.5
        else:
            ACS = ACS + 0.0
        if roca == "LUTITA":
            ACS = ACS + 1.0
        else:
            ACS = ACS + 0.0
        # INYECCIÓN DE ÁCIDO
        IA = float(0)
        if float(per) >= float(10) and float(per) <= float(250):
            IA = IA + 0.5
        elif float(per) > float(250) and float(per) < float(750):
            IA = IA + 1.0
        elif float(per) >= float(750) and float(per) <= float(1000):
            IA = IA + 0.5
        else:
            IA = IA + 0.0
        if por >= float(10):
            IA = IA + 1.0
        else:
            IA = IA + 0.0
        if esp >= float(10):
            IA = IA + 1
        else:
            IA = IA + 0.0
        if tem >= float(65):
            IA = IA + 1.0
        else:
            IA = IA + 0.0
        if api == 0.0:
            IA = IA + 0.0
        else:
            IA = IA + 1.0
        if vis <= float(100) and vis > float(0):
            IA = IA + 1.0
        else:
            IA = IA + 0.0
        if sat >= float(20) and sat <= float(35):
            IA = IA + 0.5
        elif sat > float(35) and sat < float(65):
            IA = IA + 1.0
        elif sat >= float(65) and sat <= float(80):
            IA = IA + 0.5
        else:
            IA = IA + 0.0
        if prof <= float(3000) and prof > float(0):
            IA = IA + 1.0
        else:
            IA = IA + 0.0
        if roca == "ARENISCA" or roca == "CALIZA":
            IA = IA + 1.0
        else:
            IA = IA + 0.0
        # INYECCIÓN DE MICROEMULSIONES
        MICE = float(0)
        if float(per) >= float(100):
            MICE = MICE + 1.0
        else:
            MICE = MICE + 0.0
        if por >= float(10):
            MICE = MICE + 1.0
        else:
            MICE = MICE + 0.0
        if esp >= float(10):
            MICE = MICE + 1
        else:
            MICE = MICE + 0.0
        if tem <= float(100) and tem > float(0):
            MICE = MICE + 1.0
        else:
            MICE = MICE + 0.0
        if api <= float(30) and api > float(0):
            MICE = MICE + 1.0
        else:
            MICE = MICE + 0.0
        if vis >= float(10):
            MICE = MICE + 1.0
        else:
            MICE = MICE + 0.0
        if sat <= float(50) and sat > float(0):
            MICE = MICE + 1.0
        else:
            MICE = MICE + 0.0
        if prof >= float(1000):
            MICE = MICE + 1.0
        else:
            MICE = MICE + 0.0
        if roca == "ARENISCA":
            MICE = MICE + 1.0
        else:
            MICE = MICE + 0.0
        # INYECCIÓN DE ESPUMAS
        ESP = float(0)
        if float(per) >= float(50) and float(per) <= float(1287.5):
            ESP = ESP + 0.5
        elif float(per) > float(1287.5) and float(per) < float(3762.5):
            ESP = ESP + 1.0
        elif float(per) >= float(3762.5) and float(per) <= float(5000):
            ESP = ESP + 0.5
        else:
            ESP = ESP + 0.0
        if por >= float(20):
            ESP = ESP + 1.0
        else:
            ESP = ESP + 0.0
        if esp <= float(6) and esp > float(0):
            ESP = ESP + 1
        else:
            ESP = ESP + 0.0
        if tem <= float(100) and tem > float(0):
            ESP = ESP + 1.0
        else:
            ESP = ESP + 0.0
        if api >= float(8) and api <= float(12.25):
            ESP = ESP + 0.5
        elif api > float(12.25) and api < float(20.75):
            ESP = ESP + 1.0
        elif api >= float(20.75) and api <= float(25):
            ESP = ESP + 0.5
        else:
            ESP = ESP + 0.0
        if vis >= float(10):
            ESP = ESP + 1.0
        else:
            ESP = ESP + 0.0
        if sat >= float(50):
            ESP = ESP + 1.0
        else:
            ESP = ESP + 0.0
        if prof <= float(1800) and prof > float(0):
            ESP = ESP + 1.0
        else:
            ESP = ESP + 0.0
        if roca == "ARENISCA":
            ESP = ESP + 1.0
        else:
            ESP = ESP + 0.0
        # INYECCIÓN DE SOLUCIONES ACUOSAS DE CO2
        ACO = float(0)
        if float(per) >= float(50) and float(per) <= float(162.5):
            ACO = ACO + 0.5
        elif float(per) > float(162.5) and float(per) < float(387.5):
            ACO = ACO + 1.0
        elif float(per) >= float(387.5) and float(per) <= float(500):
            ACO = ACO + 0.5
        else:
            ACO = ACO + 0.0
        if por >= float(20) and por <= float(22.5):
            ACO = ACO + 0.5
        elif por > float(22.5) and por < float(27.5):
            ACO = ACO + 1.0
        elif por >= float(27.5) and por <= float(30):
            ACO = ACO + 0.5
        else:
            ACO = ACO + 0.0
        if esp >= float(10) and esp <= float(12.5):
            ACO = ACO + 0.5
        elif esp > float(12.5) and esp < float(17.5):
            ACO = ACO + 1.0
        elif esp >= float(17.5) and esp <= float(20):
            ACO = ACO + 0.5
        else:
            ACO = ACO + 0.0
        if tem >= float(60) and tem <= float(67.5):
            ACO = ACO + 0.5
        elif tem > float(67.5) and tem < float(82.5):
            ACO = ACO + 1.0
        elif tem >= float(82.5) and tem <= float(90):
            ACO = ACO + 0.5
        else:
            ACO = ACO + 0.0
        if api >= float(20) and api <= float(26.25):
            ACO = ACO + 0.5
        elif api > float(26.25) and api < float(38.75):
            ACO = ACO + 1.0
        elif api >= float(38.75) and api <= float(45):
            ACO = ACO + 0.5
        else:
            ACO = ACO + 0.0
        if vis >= float(10) and vis <= float(32.5):
            ACO = ACO + 0.5
        elif vis > float(32.5) and vis < float(77.5):
            ACO = ACO + 1.0
        elif vis >= float(77.5) and vis <= float(100):
            ACO = ACO + 0.5
        else:
            ACO = ACO + 0.0
        if sat <= float(60) and sat > float(0):
            ACO = ACO + 1.0
        else:
            ACO = ACO + 0.0
        if prof == 0.0:
            ACO = ACO + 0.0
        else:
            ACO = ACO + 1.0
        if roca == 0.0:
            ACO = ACO + 0.0
        else:
            ACO = ACO + 1.0
        # INYECCIÓN DE NANOHIERRO
        NH = float(0)
        if float(per) >= float(50) and float(per) <= float(112.5):
            NH = NH + 0.5
        elif float(per) > float(112.5) and float(per) < float(237.5):
            NH = NH + 1.0
        elif float(per) >= float(237.5) and float(per) <= float(300):
            NH = NH + 0.5
        else:
            NH = NH + 0.0
        if por >= float(20) and por <= float(21.25):
            NH = NH + 0.5
        elif por > float(21.25) and por < float(23.75):
            NH = NH + 1.0
        elif por >= float(23.75) and por <= float(25):
            NH = NH + 0.5
        else:
            NH = NH + 0.0
        if esp >= float(5):
            NH = NH + 1
        else:
            NH = NH + 0.0
        if tem >= float(40) and tem <= float(45):
            NH = NH + 0.5
        elif tem > float(45) and tem < float(55):
            NH = NH + 1.0
        elif tem >= float(55) and tem <= float(60):
            NH = NH + 0.5
        else:
            NH = NH + 0.0
        if api >= float(20) and api <= float(21.25):
            NH = NH + 0.5
        elif api > float(21.25) and api < float(23.75):
            NH = NH + 1.0
        elif api >= float(23.75) and api <= float(25):
            NH = NH + 0.5
        else:
            NH = NH + 0.0
        if vis >= float(100) and vis <= float(150):
            NH = NH + 0.5
        elif vis > float(150) and vis < float(250):
            NH = NH + 1.0
        elif vis >= float(250) and vis <= float(300):
            NH = NH + 0.5
        else:
            NH = NH + 0.0
        if sat >= float(50) and sat <= float(55):
            NH = NH + 0.5
        elif sat > float(55) and sat <= float(65):
            NH = NH + 1.0
        elif sat >= float(65) and sat <= float(70):
            NH = NH + 0.5
        else:
            NH = NH + 0.0
        if prof >= float(1500):
            NH = NH + 1.0
        else:
            NH = NH + 0.0
        if roca == "ARENISCA" or roca == "CARBONATA":
            NH = NH + 1.0
        else:
            NH = NH + 0.0
        # INYECCIÓN DE NANOARCILLA
        NA = float(0)
        if float(per) >= float(50):
            NA = NA + 1.0
        else:
            NA = NA + 0.0
        if por >= float(15):
            NA = NA + 1.0
        else:
            NA = NA + 0.0
        if esp >= float(10):
            NA = NA + 1
        else:
            NA = NA + 0.0
        if tem >= float(50) and tem <= float(62.5):
            NA = NA + 0.5
        elif tem > float(62.5) and tem < float(87.5):
            NA = NA + 1.0
        elif tem >= float(87.5) and tem <= float(100):
            NA = NA + 0.5
        else:
            NA = NA + 0.0
        if api >= float(20) and api <= float(25):
            NA = NA + 0.5
        elif api > float(25) and api < float(35):
            NA = NA + 1.0
        elif api >= float(35) and api <= float(40):
            NA = NA + 0.5
        else:
            NA = NA + 0.0
        if vis >= float(10):
            NA = NA + 1.0
        else:
            NA = NA + 0.0
        if sat <= float(70) and sat > float(0):
            NA = NA + 1.0
        else:
            NA = NA + 0.0
        if prof <= float(2000) and prof > float(0):
            NA = NA + 1.0
        else:
            NA = NA + 0.0
        if roca == 0.0:
            NA = NA + 0.0
        else:
            NA = NA + 1.0
        CIS = CIS * 100 / 9
        THAI = THAI * 100 / 9
        VAP = VAP * 100 / 9
        HAP = HAP * 100 / 9
        SD = SD * 100 / 9
        SAGD = SAGD * 100 / 9
        COS = COS * 100 / 9
        COV = COV * 100 / 9
        IN = IN * 100 / 9
        ASP = ASP * 100 / 9
        SP = SP * 100 / 9
        MP = MP * 100 / 9
        GEL = GEL * 100 / 9
        MIC = MIC * 100 / 9
        HW = HW * 100 / 9
        WAG = WAG * 100 / 9
        MICF = MICF * 100 / 9
        ACS = ACS * 100 / 9
        IA = IA * 100 / 9
        MICE = MICE * 100 / 9
        ESP = ESP * 100 / 9
        ACO = ACO * 100 / 9
        NH = NH * 100 / 9
        NA = NA * 100 / 9
        diccionario = {"Combustión in Situ.": CIS, "Toe to Heel Air Injection.": THAI,
                       "Inyección convencional de Vapor.": VAP,
                       "Método Huff & Puff.": HAP, "Método Steam Drive.": SD,
                       "Método Steam Assisted Gravity Drainage.": SAGD,
                       "Inyección de CO2 Supercrítico.": COS, "Inyección de CO2 Convencional.": COV, "Inyección de N2.": IN,
                       "Inyección ASP.": ASP, "Inyección SP.": SP, "Inyección MP.": MP, "Inyección de geles.": GEL,
                       "Inyección de microorganismos.": MIC, "Hot Waterflooding.": HW, "Water Alternating Gas.": WAG,
                       "Inyección de microfluidos.": MICF, "Inyección de Agentes de cambio de fase.": ACS,
                       "Inyección de ácido.": IA, "Inyección de microemulsiones.": MICE, "Inyección de espumas.": ESP,
                       "Inyección de soluciones acuosas de CO2.": ACO, "Inyección de nanohierro.": NH,
                       "Inyección de nanoarcilla.": NA}
        sorted_d = dict(sorted(diccionario.items(), key=lambda x: x[1], reverse=True))
        st.write(
            "A continuación, se mostrará una lista ordenada de forma descendente desde la técnica más idónea para su pozo hasta la menos recomendable con su respectiva probabilidad de éxito.")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        k = 1
        for i in sorted_d:
            valor = sorted_d[i]
            n2 = round(valor, 2)
            st.write("Puesto #", k, ":", i, "Probabilidad de éxito:", n2, "%",)
            k = k + 1
        diccionario_noordenado = dict(sorted(diccionario.items(), key=lambda x: x[1]))
        ejex = list(diccionario_noordenado.keys())
        ejey = list(diccionario_noordenado.values())

        fig, ax = plt.subplots()
        ax.barh(ejex, ejey)
        ax.set_title('Idoneidad de técnicas de EOR')
        ax.set_xlabel('Valor de probabilidad de éxito')
        ax.set_ylabel('Método')
        st.write("")
        st.write("")
        st.write("")
        st.pyplot(fig)

        # Autores
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

    authors_col1, authors_col2 = st.columns(2)
    with authors_col1:
            #st.image("autor1.png", width=75)
        st.markdown("**Ronny David Morales García - rondamor@espol.edu.ec**")
    with authors_col2:
           #st.image("autor2.png", width=75)
       st.markdown("**Leopoldo Guillermo Medina Cáceres - lgmedina@espol.edu.ec**")

if __name__ == "__main__":
    main()