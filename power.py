#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

# Añadir manualmente la ruta donde está gateway.py (directorio de menu.py y power.py)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gateway

import os
print(os.getcwd())

gw = gateway.Gateway()

def get_tx_power(interface=None):
    """Función para obtener la potencia de transmisión de una interfaz de red o todas las interfaces"""
    interfaces = ["wl0", "wl1", "wl2"] if interface is None else [interface]
    
    for iface in interfaces:
        try:
            cmd = f'iwlist {iface} txpower'
            result = gw.run_cmd_with_output(cmd)
            
            if result:
                print(f"\nPotencia de transmisión para {iface}:")
                print(result)
            else:
                print(f"No se pudo obtener la potencia de transmisión para {iface}")
        except Exception as e:
            print(f"Error al ejecutar el comando para {iface}: {str(e)}")

        
        
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
        elif opcion == '0':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, elige una opción del 0 al 8.")

if __name__ == "__main__":
    mostrar_menu()
