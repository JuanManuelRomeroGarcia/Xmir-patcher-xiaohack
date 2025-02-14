#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import random
import time
import uuid
import getpass
import requests
import sys
import re
import argparse

# Configuración predeterminada
PUBLIC_KEY = "a2ffa5c9be07488bbb04a3a47d3c5f6a"
DEFAULT_HOSTNAME = "gateway"

def sha1(x: str):
    return hashlib.sha1(x.encode()).hexdigest()

def get_mac_address():
    as_hex = f"{uuid.getnode():012x}"
    return ":".join(as_hex[i : i + 2] for i in range(0, 12, 2))

def generate_nonce(miwifi_type=0):
    return f"{miwifi_type}_{get_mac_address()}_{int(time.time())}_{random.randint(0, 999)}"

def generate_password_hash(nonce, password):
    return sha1(nonce + sha1(password + PUBLIC_KEY))

def prompt_input(prompt):
    """Solicita una entrada al usuario con la opción de salir al ingresar '0'."""
    while True:
        value = input(f"{prompt} \n(o escribe '0' para salir): ").strip()
        if value == "0":
            print("Saliendo del programa...")
            sys.exit(0)
        if value:
            return value
        print("⚠️ Entrada no válida, intenta de nuevo.")

def display_ip(address):
    """Muestra la IP de conexión."""
    print(f"🔗 Conectando a la IP: {address}\n")

def validar_mac(mac):
    """Verifica que la dirección MAC tenga el formato correcto."""
    mac_regex = r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$"
    return bool(re.match(mac_regex, mac))

class MiWiFi():
    def __init__(self, address, miwifi_type=0):
        if not address.startswith(("http://", "https://")):
            address = f"http://{address}"
        self.address = address.rstrip("/")
        self.token = None
        self.miwifi_type = miwifi_type
        self.aiot = None

    def request(self, method, endpoint, data=None):
        """Manejo centralizado de solicitudes HTTP con validación."""
        url = f"{self.address}/cgi-bin/luci/;stok={self.token}{endpoint}" if self.token else f"{self.address}{endpoint}"
        try:
            response = requests.request(method, url, data=data, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error en la conexión: {e}")
            sys.exit(1)

    def login(self, password):
        nonce = generate_nonce(self.miwifi_type)
        data = {
            "username": "admin",
            "logtype": "2",
            "password": generate_password_hash(nonce, password),
            "nonce": nonce,
        }
        jdata = self.request("POST", "/cgi-bin/luci/api/xqsystem/login", data)
        if "token" in jdata:
            self.token = jdata["token"]
            return True
        print("❌ Error: No se pudo iniciar sesión. Verifica tu contraseña.")
        return False

    def get_infos(self):
        jdata = self.request("GET", "/api/misystem/status")
        if "hardware" in jdata:
            print(f"🖥️ Plataforma: {jdata['hardware']['platform']}")
        else:
            print("❌ Error al recuperar la información del sistema.")
            sys.exit(1)

    def set_aiot_status(self, status):
        """Activa o desactiva el escaneo AIoT solo si es necesario."""
        if not self.token:
            print("¡Necesitas iniciar sesión para usar esta función!")
            return None

        # Obtener el estado actual y manejar errores si no se obtiene correctamente
        current_status = self.get_aiot_status()
        if current_status is None:
            print("⚠️ No se pudo obtener el estado actual de AIoT. No se realizará ningún cambio.")
            return

        # Si el estado ya es el deseado, no hacer nada
        if current_status == status:
            print(f"⚡ No es necesario cambiar el estado de AIoT, ya está {'ENCENDIDO' if status else 'APAGADO'}.")
            return

        # Si es diferente, cambiar el estado
        aiotstatus = "ENCENDIDO" if status else "APAGADO"
        print(f"🔄 Cambiando el estado del escaneo AIoT a {aiotstatus}...")

        try:
            response = requests.post(
                f"{self.address}/cgi-bin/luci/;stok={self.token}/api/xqnetwork/miscan_switch",
                data={"on": str(int(status))},
                timeout=5
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error al cambiar el estado de AIoT: {e}")
            return

        # Confirmamos que el cambio realmente se hizo
        new_status = self.get_aiot_status()
        if new_status == status:
            print(f"✅ Estado del escaneo AIoT cambiado correctamente a {aiotstatus}.")
        else:
            print("❌ No se pudo confirmar el cambio de estado de AIoT.")

    def get_aiot_status(self):
        """Obtiene el estado actual del escaneo AIoT y maneja errores si ocurren."""
        try:
            jdata = self.request("GET", "/api/xqnetwork/get_miscan_switch")
            if "enabled" in jdata:
                self.aiot = bool(jdata["enabled"])
                aiotstatus = "ENCENDIDO" if self.aiot else "APAGADO"
                print(f"📡 Estado del escaneo AIoT: {aiotstatus}\n")
                return self.aiot
            else:
                print("⚠️ La respuesta del router no contiene información de AIoT.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error al obtener el estado de AIoT: {e}")
            return None


    def get_5ghz_xiaomi(self):
        if not self.token:
            print("¡Necesitas iniciar sesión para usar esta función!")
            return None

        intentos = 0
        max_intentos = 3  # 🔄 Máximo de intentos antes de preguntar al usuario

        while intentos < max_intentos:
            print(f"🔍  Intento {intentos + 1}/{max_intentos} - Escaneando puntos de acceso WiFi de Xiaomi...")

            detected = 0  # ✅ Inicializamos aquí para evitar errores de variable no definida

            try:
                response = requests.get(
                    f"{self.address}/cgi-bin/luci/;stok={self.token}/api/xqnetwork/wifi_list", 
                    timeout=15
                )
                response.raise_for_status()
                jdata = response.json()
            except requests.exceptions.Timeout:
                print("⚠️  El router tardó demasiado en responder.")
                intentos += 1
                continue  # 🔄 Reintenta hasta alcanzar el límite
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Error en la conexión: {e}")
                sys.exit(1)

            if "list" in jdata:
                for ap in jdata["list"]:
                    if ap["ssid"].startswith("Xiaomi_") and ap["encryption"] == "NONE":
                        if (ap["band"] == "5g" and ap["ssid"].endswith("_5G")) or (ap["band"] == "2g"):
                            if detected == 0:
                                print("📡 Puntos de acceso detectados:")
                            print(f'\tBanda: {ap["band"]}hz SSID: {ap["ssid"]} CH: {ap["channel"]} MODELO: {ap["wsc_modelname"]} MAC: {ap["bssid"]}')
                            if ap["band"] == "2g":
                                pmac = ap['bssid'].split(":")
                                pmac[-1] = hex(int(pmac[-1], 16) + 1)[2:].upper()
                                pmac = ':'.join(pmac)
                                print(f'\t\tMAC POSIBLE para 5GHz: {pmac}')
                            detected += 1

            if detected > 0:
                break  # ✅ Si se detectan redes, salir del bucle

            intentos += 1

        # Si no encontró redes después de los intentos, preguntar al usuario
        if detected == 0:
            print("❌ No se detectaron puntos de acceso.")
            while True:
                opcion = input("🔄 ¿Quieres volver a intentar el escaneo? (S/N): ").strip().lower()
                if opcion == "s":
                    intentos = 0  # 🔄 Restablece el contador y vuelve a intentar
                elif opcion == "n":
                    print("⚠️ Continuando sin escanear... Es posible que falle al agregar el nodo.")
                    break  # 🔚 Salimos del bucle
                else:
                    print("❌ Opción no válida. Escribe 'S' para reintentar o 'N' para continuar sin escanear.")

        print("")

    def add_mesh_node(self, macaddr, location="Estudio"):
        print(f"🔗 Agregando {macaddr} como nodo mesh en {location}...")
        jdata = self.request("POST", "/api/xqnetwork/add_mesh_node", {"mac": macaddr, "locate": location})
        if jdata.get("code") == 0:
            print(f"✅ Nodo {macaddr} agregado correctamente. Espera a que se reinicie.")
            return True
        print(f"❌ Error al agregar el nodo. Código de error: {jdata.get('code', 'Desconocido')}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agregador de Nodo Mesh MiWiFi")
    parser.add_argument("address", nargs="?", default=f"http://{DEFAULT_HOSTNAME}", help="Dirección IP o nombre del router")
    args = parser.parse_args()

    address_master = args.address
    display_ip(address_master)

    password_master = getpass.getpass(prompt='🔑 Introduce la contraseña del router principal \n(o escribe "0" para salir): ')
    if password_master == "0":
        print("Saliendo del programa...")
        sys.exit(0)

    router = MiWiFi(address=address_master)
    print("🔐 Iniciando sesión...")
    if not router.login(password_master):
        sys.exit(1)
    print("✅ Inicio de sesión exitoso.\n")

    router.get_infos()
    if not router.get_aiot_status():
        router.set_aiot_status(True)
    router.get_5ghz_xiaomi()

    while True:
        mac_address_client = prompt_input("📡 Introduce la dirección MAC del router (5GHz, no configurado) (AA:BB:CC:DD:EE:FF)")
        if validar_mac(mac_address_client):
            break
        print("❌ Dirección MAC inválida, intenta nuevamente.")

    if router.add_mesh_node(mac_address_client):
        sys.exit(0)
    else:
        sys.exit(1)
