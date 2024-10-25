#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

import xmir_base

import gateway
import xqmodel

print(os.getcwd())

gw = gateway.Gateway()

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
    interfaces = ["wl0", "wl1", "wl2"] if interface is None else [interface]
    
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
(sleep 60;iwconfig wl0 txpower 30;iwconfig wl1 txpower 30;iwconfig wl2 txpower 30;uci set wireless.wifi0.country=EU; uci set wireless.wifi1.country=EU; uci set wireless.wifi2.country=EU; uci commit wireless)&
"""
    
    R3600_command = """
(sleep 60;iwconfig wl0 txpower 30;iwconfig wl1 txpower 30)&
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
    elif model_id == [45, 29]:  # RA82 , RM1800
        return common_content + RM1800_command + "\nexit 0"
    else:
        # Si el modelo no está soportado
        unsupported_model_message = "Error: Modelo {} con ID {} no soportado.".format(device_name, model_id)
        print(unsupported_model_message)
        print("Si su modelo no es soportado, mande un email a administracion@xiaohack.es con el modelo para su investigación.")
        return None


def mostrar_menu():
    """Función para mostrar el menú y manejar las opciones del usuario"""
    while True:
        print("\n--- Menú de Potencia de Antenas ---")
        print("-----------------------------------")
        print("1. Cambiar potencia de transmisión de wl0 (5GHz)")
        print("2. Cambiar potencia de transmisión de wl1 (2.4GHz)")
        print("3. Cambiar potencia de transmisión de wl2 (5GHz Gaming)")
        print("--- ---")
        print("4. Ver potencia de transmisión de wl0 (5GHz)")
        print("5. Ver potencia de transmisión de wl1 (2.4GHz)")
        print("6. Ver potencia de transmisión de wl2 (5GHz Gaming)")
        print("\n--- Cambiar Todas ---")
        print("7. Cambiar potencia de transmisión de todas las antenas")
        print("\n--- Ver todas  ---")
        print("8. Ver potencia de transmisión de todas las antenas")
        print("\n--- Actualizar rc.local ---")
        print("9. Actualizar archivo rc.local con los valores Maximos del modelo")
        print("--------------------------------")
        print("0. Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            set_tx_power("wl0")  # Cambiar potencia de wl0
        elif opcion == '2':
            set_tx_power("wl1")  # Cambiar potencia de wl1
        elif opcion == '3':
            set_tx_power("wl2")  # Cambiar potencia de wl2
        elif opcion == '4':
            get_tx_power("wl0")  # Ver potencia de wl0
        elif opcion == '5':
            get_tx_power("wl1")  # Ver potencia de wl1
        elif opcion == '6':
            get_tx_power("wl2")  # Ver potencia de wl2
        elif opcion == '7':
            set_tx_power()  # Cambiar potencia de todas las antenas
        elif opcion == '8':
            get_tx_power()  # Ver potencia de todas las antenas
        elif opcion == '9':
            update_rc_local()  # Actualizar archivo rc.local con los valores personalizados
        elif opcion == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, elige una opción del 0 al 9.")

if __name__ == "__main__":
    mostrar_menu()
