import matplotlib.pyplot as plt
import pandas as pd
import lasio

def bold(text): return "\033[1m" + text + "\033[0m"
print(bold("\nBienvenido al software de screening de técnicas de EOR de la ESPOL. A continuación, selecciona la opción de ingreso de datos que dispone:"))
print("\n1. Carga de archivo LAS (Log ASCII Standard).\n2. Ingreso manual de datos promedio de pozos.")
while True:
    opc = input("\n\033[1mDigite 1 o 2 según corresponda:")

    if not opc:  # si se presiona enter sin ingresar nada
        print("\nDebe ingresar una opción. Intente de nuevo.")
        break
    elif not opc.replace('.', '', 1).isdigit():  # si hay caracteres no numéricos
        print("\nError: ha ingresado caracteres no numéricos. Intente de nuevo.")
    elif float(opc) == 0 or float(opc) > 2:  # si el valor es igual a cero o mayor que 2
        print("\nError: el valor debe ser 1 o 2. Intente de nuevo.")

    elif int(opc) == 1:

        #las = input("\n\033[1mPor favor ingrese la ruta de acceso al archivo:\033[0m")
        #CORREGIR ABAJO DIRECCION DE RUTA USANDO DOS DIAGONALES
        la = "C:\\Users\\USUARIO\\Desktop\\LGA-027.las"  #Directorio de computadora de autor, en otra computadora saldrá error.

        # Lectura de archivo
        las = lasio.read(la)

        # Nombre de pozo
        print("\n\033[1mNombre de pozo:\033[0m", las.well.WELL.value)
        print("\n\033[1mPaís:\033[0m", las.well["COUNT"].value)
        print("\n\033[1mProvincia:\033[0m", las.well["STATE"].value)
        print("\n\033[1mCompañía:\033[0m", las.well["COMP"].value)


        # Se transforma el archivo
        well = las.df()

        # 3 decimales
        pd.options.display.float_format = '{:.3f}'.format

        print("\n")

        # Selección de datos de payflag

        #contador = 0  # contador para la secuencia actual de 1
        #sequence_started = False  # indica si ya se ha empezado una secuencia
        #a = pd.DataFrame()  # subdataframe actual
        #b = []  # lista de subdataframes

        #for i, row in well.iterrows():
        #    if row['PAYFLAG'] == 1:  # si el valor es 1
        #        #print(i,row)
        #        if not sequence_started:  # si no se ha empezado una secuencia
        #            sequence_started = True  # se empieza una secuencia
        #            c = pd.DataFrame()  # se crea un nuevo subdataframe
        #        contador += 1  # se incrementa el contador de la secuencia actual
        #        c = c.append(row,ignore_index=True)  # se añade la fila al subdataframe

        #    elif row['PAYFLAG'] == 0 and sequence_started:  # si el valor es 0 y se ha empezado una secuencia
        #        b.append(a)  # se añade el subdataframe actual a la lista de subdataframes
        #        contador = 0  # se reinicia el contador de la secuencia actual
        #        sequence_started = False  # se indica que no hay secuencia actual

        #if sequence_started:
        #    b.append(a)

        #for a in b:
        #    print(a)

        #df_filtrado = well.loc[well['PAYFLAG'] == 1.000]
        #print(df_filtrado)

        # Se borra curvas innecesarias
        #PHIT POROSIDAD TOTAL
        #PHIE POROSIDAD EFECTIVA
        #RESFLAG INDICADOR DE FIABILIDAD DE DATOS DE RESISTIVIDAD
        #DTMA POROSIDAD Y LITOLOGIA
        #RHOB DENSIDAD APARENTE
        #CALIPER
        las.delete_curve('CALI')
        # Borrar ILD Resistividad
        las.delete_curve('ILD')
        # FACTOR DE CALIDAD DEL REGISTRO
        las.delete_curve('KTR')
        # INVERSION DE RESISTIVIDAD
        las.delete_curve('MINV')
        # MICRO NORMAL RESISTIVITY
        las.delete_curve('MNOR')
        las.delete_curve('TR1')
        las.delete_curve('DTMA')
        las.delete_curve('PEFS1')

        # Se da un vistazo general de las curvas utiles que se trabajara
        #for count, curve in enumerate(las.curves):
            #print(f"Curva: {curve.mnemonic}, \t Unidades: {curve.unit}, \t Descripción: {curve.descr}")
            #print(f"Existe un total de: {count+1} curvas en su archivo.")


        #df_filtrado = df.loc[df['PAYFLAG'] == 1]
        #print()
        # Se imprime los primeros valores
        #print(well.head())

        print("\n")

        # Se imprime valores estadisticos
        #print(well.describe())

        # Se grafica

        #Se asigna los valores a los 9 parámetros
        por=0.0
        per=0.0
        esp=0.0
        tem=0.0
        api=0.0
        vis = 0.0
        sat = 0.0
        prof=0.0
        roca = 0.0

        break

    elif int(opc) == 2:
        print(bold("\nA continuación, ingrese los valores promedio de su pozo."))
        # POROSIDAD
        while True:
            por = input(
                "\n\033[1mIngrese el valor numérico de la Porosidad promedio en formato de porcentaje\033[0m.\nSi no cuenta con el dato presione Enter:")
            if not por:  # si se presiona enter sin ingresar nada
                por = "-"
                break
            elif not por.replace('.', '', 1).isdigit():  # si hay caracteres no numéricos
                print(
                    "\nError: ha ingresado caracteres no numéricos. Recuerde que para separar decimales debe usar el punto (.) Intente de nuevo.")
            elif float(por) == 0 or float(por) > 100:  # si el valor es igual a cero o mayor que 100
                print("\nError: el valor debe ser mayor que cero y menor o igual a 100. Intente de nuevo.")
            else:
                por = float(por)
                print("\nEl valor ingresado es:", por, "%")
                break
        # PERMEABILIDAD
        while True:
            per = input(
                "\n\033[1mIngrese el valor numérico de la Permeabilidad promedio en unidades de mili Darcys.\033[0m\nSi no cuenta con el dato presione Enter:")
            if not per:  # si se presiona enter sin ingresar nada
                per = "-"
                break
            elif not per.replace('.', '', 1).isdigit():  # si hay caracteres no numéricos
                print(
                    "\nError: ha ingresado caracteres no numéricos. Recuerde que para separar decimales debe usar el punto (.) Intente de nuevo.")
            elif float(per) == 0:  # si el valor es igual a cero
                print("\nError: el valor debe ser mayor que cero. Intente de nuevo.")
            else:
                per = float(per)
                print("\nEl valor ingresado es:", per, "mD")
                break
        # ESPESOR
        while True:
            esp = input(
                "\n\033[1mIngrese el valor numérico del Espesor del yacimiento en unidades de metros.\033[0m\nSi no cuenta con el dato presione Enter:")
            if not esp:  # si se presiona enter sin ingresar nada
                esp = "-"
                break
            elif not esp.replace('.', '', 1).isdigit():  # si hay caracteres no numéricos
                print(
                    "\nError: ha ingresado caracteres no numéricos. Recuerde que para separar decimales debe usar el punto (.) Intente de nuevo.")
            elif float(esp) == 0:  # si el valor es igual a cero
                print("\nError: el valor debe ser mayor que cero. Intente de nuevo.")
            else:
                esp = float(esp)
                print("\nEl valor ingresado es:", esp, "metros")
                break
        # TEMPERATURA
        while True:
            tem = input(
                "\n\033[1mIngrese el valor numérico de la Temperatura del yacimiento en unidades de grados Celsius.\033[0m\nSi no cuenta con el dato presione Enter:")
            if not tem:  # si se presiona enter sin ingresar nada
                tem = "-"
                break
            elif not tem.replace('.', '', 1).isdigit():  # si hay caracteres no numéricos
                print(
                    "\nError: ha ingresado caracteres no numéricos. Recuerde que para separar decimales debe usar el punto (.) Intente de nuevo.")
            elif float(tem) == 0:  # si el valor es igual a cero
                print("\nError: el valor debe ser mayor que cero. Intente de nuevo.")
            else:
                tem = float(tem)
                print("\nEl valor ingresado es:", tem, "°C")
                break
        # API
        while True:
            api = input(
                "\n\033[1mIngrese el valor de Gravedad API de su petróleo.\033[0m\nSi no cuenta con el dato presione Enter.")
            if not api:  # si se presiona enter sin ingresar nada
                api = "-"
                break
            elif not api.replace('.', '', 1).isdigit():  # si hay caracteres no numéricos
                print(
                    "\nError: ha ingresado caracteres no numéricos. Recuerde que para separar decimales debe usar el punto (.) Intente de nuevo.")
            elif float(api) == 0:  # si el valor es igual a cero
                print("\nError: el valor debe ser mayor que cero. Intente de nuevo.")
            else:
                api = float(api)
                print("\nEl valor ingresado es:", api, "API")
                break
        # VISCOSIDAD
        while True:
            vis = input(
                "\n\033[1mIngrese el valor de Viscosidad del petróleo en unidades de centi Poise.\033[0m\nSi no cuenta con el dato presione Enter.")
            if not vis:  # si se presiona enter sin ingresar nada
                vis = "-"
                break
            elif not vis.replace('.', '', 1).isdigit():  # si hay caracteres no numéricos
                print(
                    "\nError: ha ingresado caracteres no numéricos. Recuerde que para separar decimales debe usar el punto (.) Intente de nuevo.")
            elif float(vis) == 0:  # si el valor es igual a cero
                print("\nError: el valor debe ser mayor que cero. Intente de nuevo.")
            else:
                vis = float(vis)
                print("\nEl valor ingresado es:", vis, "cP")
                break
        # SATURACIÓN
        while True:
            sat = input(
                "\n\033[1mIngrese el valor de Saturación de petróleo promedio en formato de porcentaje.\033[0m\nSi no cuenta con el dato presione Enter.")
            if not sat:  # si se presiona enter sin ingresar nada
                sat = "-"
                break
            elif not sat.replace('.', '', 1).isdigit():  # si hay caracteres no numéricos
                print(
                    "\nError: ha ingresado caracteres no numéricos. Recuerde que para separar decimales debe usar el punto (.) Intente de nuevo.")
            elif float(sat) == 0 or float(sat) > 100:  # si el valor es igual a cero o mayor a 100%
                print("\nError: el valor debe ser mayor que cero o menor o igual a cien. Intente de nuevo.")
            else:
                sat = float(sat)
                print("\nEl valor ingresado es:", sat, "%")
                break
        # PROFUNDIDAD
        while True:
            prof = input(
                "\n\033[1mIngrese el valor de la Profundidad de su yacimiento en unidades de metros.\033[0m\nSi no cuenta con el dato presione Enter.")
            if not prof:  # si se presiona enter sin ingresar nada
                prof = "-"
                break
            elif not prof.replace('.', '', 1).isdigit():  # si hay caracteres no numéricos
                print(
                    "\nError: ha ingresado caracteres no numéricos. Recuerde que para separar decimales debe usar el punto (.) Intente de nuevo.")
            elif float(prof) == 0:  # si el valor es menor o igual a cero
                print("\nError: el valor debe ser mayor que cero. Intente de nuevo.")
            else:
                prof = float(prof)
                print("\nEl valor ingresado es:", prof, "metros")
                break
        # TIPO DE ROCA
        while True:
            roca = input(
                "\n\033[1mIngrese el número que corresponda al Tipo de roca presente en su reservorio de la siguiente manera:\033[0m\n1. Arenisca.\n2. Lutita.\n3. Dolomita.\n4. Caliza.\n5. Carbonatos.\n\nSi no cuenta con el dato presione Enter.")
            if not roca:  # si se presiona enter sin ingresar nada
                roca = "-"
                break
            elif not roca.replace('.', '', 1).isdigit():  # si hay caracteres no numéricos
                print(
                    "\nError: ha ingresado caracteres no numéricos. Recuerde que debe ingresar los números correspondientes a cada tipo de roca. Intente de nuevo.")
            elif float(roca) <= 0:  # si el valor es menor o igual a cero
                print("\nError: el valor debe ser 1, 2, 3, 4 o 5. Intente de nuevo.")
            elif float(roca) == 1:  # si el valor es menor o igual a cero
                roca = "ARENISCA"
                print("\nLa roca en su reservorio es:", roca)
                break
            elif float(roca) == 2:  # si el valor es menor o igual a cero
                roca = "LUTITA"
                print("\nLa roca en su reservorio es:", roca)
                break
            elif float(roca) == 3:  # si el valor es menor o igual a cero
                roca = "DOLOMITA"
                print("\nLa roca en su reservorio es:", roca)
                break
            elif float(roca) == 4:  # si el valor es menor o igual a cero
                roca = "CALIZA"
                print("\nLa roca en su reservorio es:", roca)
                break
            elif float(roca) == 5:  # si el valor es menor o igual a cero
                roca = "CARBONATA"
                print("\nLa roca en su reservorio es:", roca)
                break
            elif float(roca) >= 6:  # si el valor es menor o igual a cero
                print("\nError: el valor debe ser 1, 2, 3, 4 o 5. Intente de nuevo.")
            else:
                print("\nError: el valor debe ser 1, 2, 3, 4 o 5. Intente de nuevo.")
        print("\n\033[1mUsted ha registrado los siguientes valores:\033[0m\n\n\033[1mPorosidad:\033[0m", por, "%", "\n\033[1mPermeabilidad\033[0m", per, "mD",
              "\n\033[1mEspesor de yacimiento:\033[0m", esp, "metros", "\n\033[1mTemperatura:\033[0m", tem, "°C", "\n\033[1mGrados API:\033[0m", api,
              "\n\033[1mViscosidad:\033[0m",vis, "cP", "\n\033[1mSaturación de petróleo:\033[0m", sat, "%", "\n\033[1mProfundidad de reservorio:\033[0m", prof, "metros",
              "\n\033[1mTipo de roca presente:\033[0m", roca)
        if per == "-":
            per = float(0)
        if por == "-":
            por = float(0)
        if tem == "-":
            tem = float(0)
        if esp == "-":
            esp = float(0)
        if api == "-":
            api = float(0)
        if vis == "-":
            vis = float(0)
        if sat == "-":
            sat = float(0)
        if prof == "-":
            prof = float(0)
        if roca == "-":
            roca = float(0)
        break

# COMBUSTIÓN IN SITU
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
CIS = CIS *100/9
THAI = THAI *100/9
VAP = VAP *100/9
HAP= HAP *100/9
SD= SD *100/9
SAGD= SAGD *100/9
COS= COS *100/9
COV= COV *100/9
IN= IN *100/9
ASP= ASP *100/9
SP= SP *100/9
MP= MP*100/9
GEL=GEL *100/9
MIC= MIC *100/9
HW= HW*100/9
WAG= WAG*100/9
MICF= MICF *100/9
ACS= ACS *100/9
IA= IA *100/9
MICE= MICE *100/9
ESP= ESP *100/9
ACO= ACO *100/9
NH= NH *100/9
NA= NA*100/9
diccionario = {"Combustión in Situ.": CIS, "Toe to Heel Air Injection.": THAI, "Inyección convencional de Vapor.": VAP,
               "Método Huff & Puff.": HAP, "Método Steam Drive.": SD, "Método Steam Assisted Gravity Drainage.": SAGD,
               "Inyección de CO2 Supercrítico.": COS, "Inyección de CO2 Convencional.": COV, "Inyección de N2.": IN,
               "Inyección ASP.": ASP, "Inyección SP.": SP, "Inyección MP.": MP, "Inyección de geles.": GEL,
               "Inyección de microorganismos.": MIC, "Hot Waterflooding.": HW, "Water Alternating Gas.": WAG,
               "Inyección de microfluidos.": MICF, "Inyección de Agentes de cambio de fase.": ACS,
               "Inyección de ácido.": IA, "Inyección de microemulsiones.": MICE, "Inyección de espumas.": ESP,
               "Inyección de soluciones acuosas de CO2.": ACO, "Inyección de nanohierro.": NH,
               "Inyección de nanoarcilla.": NA}
sorted_d = dict(sorted(diccionario.items(), key=lambda x: x[1], reverse=True))
print(bold("\nA continuación, se mostrará una lista ordenada de forma descendente desde la técnica más idónea para su pozo hasta la menos recomendable con su respectiva probabilidad de éxito."))
k = 1
for i in sorted_d:
    valor = sorted_d[i]
    n2 = round(valor, 2)
    print("\n\033[1mPuesto #\033[0m", "\033[1m", k, "\033[0m:", i, "Probabilidad:", "\033[1m", n2, "%", "\033[0m")
    k = k + 1
diccionario_noordenado = dict(sorted(diccionario.items(), key=lambda x: x[1]))
ejex = list(diccionario_noordenado.keys())
ejey = list(diccionario_noordenado.values())
plt.barh(ejex, ejey)
plt.title('Idoneidad de técnicas de EOR')
plt.xlabel('Valor de probabilidad de éxito')
plt.ylabel('Método')
plt.show()
