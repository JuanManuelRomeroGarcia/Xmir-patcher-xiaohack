#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import subprocess
import sys
import os

import xmir_base

import gateway
import xqmodel

#print(os.getcwd())

gw = gateway.Gateway()

def mostrar_menu():
    """Función para mostrar el menú y manejar las opciones del usuario según el modelo del dispositivo."""
    
    # Detectar el dispositivo y obtener el nombre y modelo
    gw.detect_device()
    device_name = gw.device_name
    model_id = xqmodel.get_modelid_by_name(device_name)
    
    # Mostrar el modelo detectado
    print(f"Modelo detectado: {device_name} (ID: {model_id})\n")

    # Definir opciones del menú base en orden
    menu_options = [
        "1. Cambiar potencia de transmisión de wl0 (5GHz)",
        "2. Cambiar potencia de transmisión de wl1 (2.4GHz)",
        "3. Cambiar potencia de transmisión de wl2 (5GHz Gaming)",  # Solo para RA70
        "4. Ver potencia de transmisión de wl0 (5GHz)",
        "5. Ver potencia de transmisión de wl1 (2.4GHz)",
        "6. Ver potencia de transmisión de wl2 (5GHz Gaming)",  # Solo para RA70
        "7. Cambiar potencia de transmisión de todas las antenas",
        "8. Ver potencia de transmisión de todas las antenas",
        "9. Actualizar archivo rc.local con los valores Maximos del modelo",
        "10. Configurar país Antenas para RA82",  # Solo para RA82
        "11. Configurar país Antenas para RA70",
        "12. Configurar país en todas las interfaces detectadas",
        "0. Salir"
    ]

    # Eliminar opciones específicas según el modelo
    if model_id != 37:  # Si no es RA70, quitar opciones de wl2
        menu_options.remove("3. Cambiar potencia de transmisión de wl2 (5GHz Gaming)")
        menu_options.remove("6. Ver potencia de transmisión de wl2 (5GHz Gaming)")
        menu_options.remove("11. Configurar país Antenas para RA70")
    if model_id != 45:  # Si no es RA82, quitar la opción específica para RA82
        menu_options.remove("10. Configurar país Antenas para RA82")

    # Mostrar el menú específico del modelo detectado
    while True:
        print("\n--- Menú de Potencia de Antenas ---")
        print("-----------------------------------")
        for option in menu_options:
            print(option)
        print("-----------------------------------")
        
        opcion = input("Elige una opción: ")

        # Procesar la opción seleccionada
        if opcion == '1':
            set_tx_power("wl0")  # Cambiar potencia de wl0
        elif opcion == '2':
            set_tx_power("wl1")  # Cambiar potencia de wl1
        elif opcion == '3' and model_id == 37:
            set_tx_power("wl2")  # Cambiar potencia de wl2 (solo RA70)
        elif opcion == '4':
            get_tx_power("wl0")  # Ver potencia de wl0
        elif opcion == '5':
            get_tx_power("wl1")  # Ver potencia de wl1
        elif opcion == '6' and model_id == 37:
            get_tx_power("wl2")  # Ver potencia de wl2 (solo RA70)
        elif opcion == '7':
            set_tx_power()  # Cambiar potencia de todas las antenas
        elif opcion == '8':
            get_tx_power()  # Ver potencia de todas las antenas
        elif opcion == '9':
            update_rc_local()  # Actualizar archivo rc.local con los valores personalizados
        elif opcion == '10' and model_id == 45:
            opcion_especifica_ra82()  # Ejecutar la opción específica para RA82
        elif opcion == '11' and model_id == 37:
            opcion_especifica_ra70()  # Ejecutar la opción específica para RA82
        elif opcion == '12':
            nuevo_pais = input("Ingrese el código del país (ej. US, EU, CN): ").strip().upper()
            if len(nuevo_pais) < 2:
                print("❌ Código de país inválido.")
                continue

            cambiar_pais_interfaces(nuevo_pais)  # ✅ Se corrige la llamada a la función

            
        elif opcion == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, elige una opción válida.")

def opcion_especifica_ra82():
    """Función específica para el modelo RA82 que configura el país a EU mediante SSH."""
    try:
        # Ejecutar comandos para configurar el país
        cmds = [
            'uci set wireless.wifi0.country=EU',
            'uci set wireless.wifi1.country=EU',
            'uci commit wireless'
        ]
        
        for cmd in cmds:
            output = gw.run_cmd_with_output(cmd)
            if output:
                print(f"Resultado de '{cmd}': {output}")
            else:
                print(f"Comando '{cmd}' ejecutado exitosamente.")
                
    except Exception as e:
        print(f"Error al ejecutar los comandos para RA82: {str(e)}")

def opcion_especifica_ra70():
    """Función específica para el modelo RA70 que configura el país a EU mediante SSH."""
    try:
        # Ejecutar comandos para configurar el país
        cmds = [
            'uci set wireless.wifi0.country=CN',
            'uci set wireless.wifi1.country=EU',
            'uci set wireless.wifi2.country=EU',
            'uci set wireless.wifi3.country=US',
            'uci commit wireless'
        ]
        
        for cmd in cmds:
            output = gw.run_cmd_with_output(cmd)
            if output:
                print(f"Resultado de '{cmd}': {output}")
            else:
                print(f"Comando '{cmd}' ejecutado exitosamente.")
                
    except Exception as e:
        print(f"Error al ejecutar los comandos para RA70: {str(e)}")

def get_tx_power(interface=None):
    """Función para obtener la potencia de transmisión de una interfaz de red o de todas las interfaces"""
    
    # Si se especifica una interfaz, usa el comando para esa interfaz
    if interface:
        cmd = f'iwlist {interface} txpower'
    else:
        # Si no se especifica interfaz, lista todas las interfaces
        cmd = f'iwlist txpower'
    
    try:
        result = gw.run_cmd_with_output(cmd)
        
        if result:
            # Dividimos el resultado por bloques de interfaces
            interfaces_data = result.split("\n\n")
            
            for block in interfaces_data:
                # Filtramos las líneas que contienen 'no transmit-power information'
                if ("no transmit-power information" not in block and
                    "unknown transmit-power information" not in block):
                    # Limpiamos espacios adicionales y eliminamos líneas vacías
                    block_cleaned = "\n".join([line.strip() for line in block.splitlines() if line.strip()])
                    
                    if block_cleaned:  # Solo imprimimos si el bloque tiene contenido
                        print(block_cleaned)
                        print() 
        else:
            print("No se pudo obtener la potencia de transmisión.")
    
    except Exception as e:
        print(f"Error al ejecutar el comando: {str(e)}")


def set_tx_power(interface=None):
    """Función para cambiar la potencia de transmisión de una interfaz de red o todas las interfaces"""
    
    # Detectar el modelo antes de cambiar la potencia
    gw.detect_device()
    model_id = xqmodel.get_modelid_by_name(gw.device_name)

    # Modelos permitidos para modificar wl2
    modelos_wl2 = [37, 70 ]  # RA70, BE7000

    # Si no es un modelo permitido, evitar que se modifique wl2
    if model_id not in modelos_wl2 and interface == "wl2":
        print(f"Error: El modelo detectado ({gw.device_name}) no admite cambios en wl2 (5GHz Gaming).")
        return

    # Si no se especifica interfaz, seleccionar wl0 y wl1 (wl2 solo si el modelo es compatible)
    if interface is None:
        interfaces = ["wl0", "wl1"]
        if model_id in modelos_wl2:
            interfaces.append("wl2")  # Agregar wl2 solo si el modelo está en la lista
    else:
        interfaces = [interface]

    potencia = input(f"Introduce la potencia de transmisión (por ejemplo, 20): ")
    if not potencia.isdigit():
        print("Por favor, introduce un valor numérico válido para la potencia.")
        return

    for iface in interfaces:
        try:
            cmd = f'iwconfig {iface} txpower {potencia}'
            result = gw.run_cmd_with_output(cmd)

            # Si result es vacío, asumimos que fue exitoso
            if result:
                print(f"Potencia de transmisión de {iface} cambiada a {potencia}.")
            else:
                print(f"Potencia de transmisión de {iface} cambiada exitosamente a {potencia}, aunque no hay salida del comando.")
        except Exception as e:
            print(f"Error al ejecutar el comando para {iface}: {str(e)}")



def update_rc_local():
    """Función para actualizar el archivo rc.local en el dispositivo remoto según el dispositivo"""
    # Detectar el dispositivo
    gw.detect_device()
    if not gw.device_name:
        print("No se pudo detectar el dispositivo.")
        return

    # Obtener el contenido personalizado para el archivo rc.local
    new_rc_local_content = customize_rc_local_content(gw.device_name)

    # Comando para escribir el nuevo contenido en /etc/rc.local
    write_rc_local_cmd = f'echo "{new_rc_local_content}" > /etc/rc.local'

    # Ejecutar el comando en el dispositivo
    output = gw.run_cmd_with_output(write_rc_local_cmd)
    
    # Confirmar que el archivo se modificó correctamente (opcional)
    confirm_output = gw.run_cmd_with_output("cat /etc/rc.local")
    print(confirm_output)


def customize_rc_local_content(device_name):
    """Función para personalizar el contenido de rc.local basado en el dispositivo usando los IDs"""
    
    common_content = """
# Put your custom commands here that should be executed once
# the system init finished. By default this file does nothing.
"""
    
    # Comandos específicos por ID de modelo
    RA70_command = """
(sleep 60;iwconfig wl0 txpower 30; iwconfig wl1 txpower 30; iwconfig wl2 txpower 30; iwconfig wl3 txpower 31; uci set wireless.wifi0.country=CN; uci set wireless.wifi1.country=EU; uci set wireless.wifi2.country=EU; uci set wireless.wifi3.country=US; uci commit wireless)&
"""
    
    R3600_command = """
(sleep 60;iwconfig wl0 txpower 30;iwconfig wl1 txpower 30;iwconfig wl2 txpower 30)&
"""

    RM1800_command = """
(sleep 60;iwconfig wl0 txpower 26;iwconfig wl1 txpower 28;uci commit wireless)&
"""

    # Obtener el ID del modelo basado en el nombre del dispositivo
    model_id = xqmodel.get_modelid_by_name(device_name)

    # Verificar el ID y asignar el comando correcto
    if model_id == 37:  # RA70
        return common_content + RA70_command + "\nexit 0"
    elif model_id == 24:  # R3600
        return common_content + R3600_command + "\nexit 0"
    elif model_id in [45, 29, 31]:  # RA82 , RM1800, RA67
        return common_content + RM1800_command + "\nexit 0"
    else:
        # Si el modelo no está soportado
        unsupported_model_message = "Error: Modelo {} con ID {} no soportado.".format(device_name, model_id)
        print(unsupported_model_message)
        print("Si su modelo no es soportado, mande un email a administracion@xiaohack.es con el modelo para su investigación.")
        return None

def guardar_en_rc_local(nuevo_pais):
    """
    Guarda la configuración del país en /etc/rc.local asegurando que:
    - Se mantiene solo una línea en blanco después del (sleep ...).
    - Se reemplaza correctamente la configuración previa de `(sleep 60; ...)`.
    - `exit 0` siempre está al final con solo una línea en blanco antes.
    """
    try:
        # Obtener la potencia de transmisión deseada del usuario
        while True:
            potencia_tx = input("Ingrese la potencia de transmisión (txpower) en dBm [Ejemplo: 30]: ").strip()
            if potencia_tx.isdigit() and 1 <= int(potencia_tx) <= 33:  # Rango válido para OpenWrt
                potencia_tx = int(potencia_tx)
                break
            else:
                print("❌ Entrada inválida. Ingrese un número entre 1 y 33 dBm.")

        # Obtener las interfaces Wi-Fi configurables (wifiX)
        salida_uci = gw.run_cmd_with_output("uci show wireless | grep country")
        interfaces_wifi = re.findall(r'wireless\.(wifi\d+)\.country=', salida_uci)

        # Obtener todas las interfaces de transmisión desde `iw dev`
        salida_iw = gw.run_cmd_with_output("iw dev")
        interfaces_detectadas = re.findall(r'Interface (\S+)', salida_iw)

        # Filtrar interfaces de transmisión (wlX) y Wi-Fi (wifiX)
        interfaces_wl = [iface for iface in interfaces_detectadas if iface.startswith("wl")]
        interfaces_wifi = [iface for iface in interfaces_detectadas if iface.startswith("wifi")]

        if not interfaces_wifi:
            print("⚠️ No se encontraron interfaces 'wifiX' para configurar el país.")
            return

        if not interfaces_wl:
            print(f"⚠️ No se encontraron interfaces 'wlX' para configurar la potencia de transmisión.")
            print(f"🔍 Interfaces detectadas en el sistema: {interfaces_detectadas}")

        # Construcción de los comandos para cambiar potencia y país
        comandos_txpower = [f"iwconfig {wl} txpower {potencia_tx}" for wl in interfaces_wl]
        comandos_pais = [f"uci set wireless.{wifi}.country='{nuevo_pais}'" for wifi in interfaces_wifi]

        # Crear la nueva línea de configuración que queremos introducir
        nueva_configuracion = f"(sleep 60; {'; '.join(comandos_txpower)}; {'; '.join(comandos_pais)}; uci commit wireless)&"

        # Obtener el contenido actual de `/etc/rc.local`
        rc_local_actual = gw.run_cmd_with_output("cat /etc/rc.local").splitlines()

        # Lista final sin acumulación de espacios
        rc_local_limpio = []
        posicion_sleep = -1
        contenido_extra = []
        agrego_linea_vacia = False

        for i, line in enumerate(rc_local_actual):
            stripped_line = line.strip()

            if stripped_line.startswith("(sleep 60;"):
                posicion_sleep = i  # Guardar la posición del antiguo `sleep`
                continue  # Omitir línea vieja

            if stripped_line == "exit 0":
                break  # No agregar líneas extra después de `exit 0`

            # Si es una línea vacía, solo agregarla si no se ha agregado una antes
            if stripped_line == "":
                if not agrego_linea_vacia:
                    rc_local_limpio.append("")
                    agrego_linea_vacia = True
                continue

            rc_local_limpio.append(stripped_line)
            agrego_linea_vacia = False  # Restablecer el control de línea vacía

        # Asegurar que haya exactamente UNA línea en blanco después del segundo comentario
        if len(rc_local_limpio) >= 2 and rc_local_limpio[1] != "":
            rc_local_limpio.insert(2, "")

        # Insertar la nueva configuración en la misma posición donde estaba `(sleep 60; ...)`
        if posicion_sleep != -1:
            rc_local_limpio.insert(posicion_sleep, nueva_configuracion)
        else:
            # Si no existía `(sleep 60; ...)`, agregarlo antes del contenido extra
            rc_local_limpio.append(nueva_configuracion)

        # Eliminar líneas en blanco innecesarias antes de `exit 0`
        while rc_local_limpio and rc_local_limpio[-1] == "":
            rc_local_limpio.pop()

        # Agregar solo una línea en blanco antes de `exit 0`
        rc_local_limpio.append("")
        rc_local_limpio.append("exit 0")

        # Unir las líneas en un solo string sin líneas vacías extras
        nuevo_contenido = "\n".join(rc_local_limpio)

        # Guardar en el router
        comando_guardado = f'echo "{nuevo_contenido}" > /etc/rc.local'
        gw.run_cmd_with_output(comando_guardado)

        print(f"✅ Configuración guardada en /etc/rc.local correctamente con potencia {potencia_tx} dBm.")

    except Exception as e:
        print(f"❌ Error al guardar en /etc/rc.local: {str(e)}")



def obtener_interfaces_wifi():
    """Ejecuta 'uci show wireless | grep country' en el router y obtiene solo las interfaces Wi-Fi configurables."""
    try:
        # Obtener la configuración de país desde UCI
        salida = gw.run_cmd_with_output("uci show wireless | grep country")

        if not salida:
            print("❌ No se pudo obtener la configuración de país de las interfaces Wi-Fi.")
            return []

        # Extraer solo las interfaces que tienen una configuración de 'country'
        interfaces = re.findall(r'wireless\.(wifi\d+)\.country=', salida)

        if not interfaces:
            print("⚠️ No se encontraron interfaces Wi-Fi configurables con opción 'country'.")
        return interfaces

    except Exception as e:
        print(f"❌ Error al ejecutar 'uci show wireless': {str(e)}")
        return []


def cambiar_pais_interfaces(nuevo_pais):
    """
    Cambia la configuración del país para cada interfaz Wi-Fi válida ('wifiX') en OpenWrt usando 'uci'.
    Luego pregunta si se desea guardar en rc.local.
    """
    interfaces_wifi = obtener_interfaces_wifi()
    
    if not interfaces_wifi:
        print("❌ No hay interfaces Wi-Fi configurables con opción 'country'.")
        return

    for interfaz in interfaces_wifi:
        comando = f"uci set wireless.{interfaz}.country='{nuevo_pais}'"
        try:
            salida = gw.run_cmd_with_output(comando)
            if salida:
                print(f"✅ País cambiado a '{nuevo_pais}' en {interfaz}. Respuesta: {salida}")
            else:
                print(f"✅ País cambiado a '{nuevo_pais}' en {interfaz}. ejecutado exitosamente.")
        except Exception as e:
            print(f"❌ Error al cambiar el país en {interfaz}: {str(e)}")

    # Preguntar si desea guardar los cambios en rc.local
    opcion_guardar = input("¿Desea guardar estos cambios en /etc/rc.local para que sean permanentes? (S/N): ").strip().lower()

    if opcion_guardar == 's':
        guardar_en_rc_local(nuevo_pais)

    # Aplicar y guardar los cambios en el sistema
    try:
        gw.run_cmd_with_output("uci commit wireless")
        #gw.run_cmd_with_output("wifi reload")
        print("✅ Configuración guardada y Wi-Fi reiniciado.")
    except Exception as e:
        print(f"❌ Error al aplicar los cambios: {str(e)}")

if __name__ == "__main__":
    mostrar_menu()
