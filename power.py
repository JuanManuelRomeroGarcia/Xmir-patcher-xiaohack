#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

if __name__ == "__main__":
    mostrar_menu()
