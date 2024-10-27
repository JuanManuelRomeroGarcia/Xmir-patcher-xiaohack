#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import random
import time
import uuid
import getpass
import requests
import sys

PUBLIC_KEY = "a2ffa5c9be07488bbb04a3a47d3c5f6a"
DEFAULT_HOSTNAME = "gateway"

def sha1(x: str):
    return hashlib.sha1(x.encode()).hexdigest()

def get_mac_address():
    as_hex = f"{uuid.getnode():012x}"
    return ":".join(as_hex[i : i + 2] for i in range(0, 12, 2))

def generate_nonce(miwifi_type=0):
    return f"{miwifi_type}_{get_mac_address()}_{int(time.time())}_{int(random.random() * 1000)}"

def generate_password_hash(nonce, password):
    return sha1(nonce + sha1(password + PUBLIC_KEY))

def prompt_input(prompt):
    """Función para solicitar entrada con opción de salir."""
    value = input(f"{prompt} \n (o escribe '0' para terminar): ")
    if value == "0":
        print("Saliendo del programa...")
        sys.exit(0)
    return value

def display_ip(address):
    """Función para mostrar la IP a la que se conecta."""
    print(f"Conectando a la IP: {address}\n")

class MiWiFi():
    def __init__(self, address, miwifi_type=0):
        # Añade el prefijo "http://" si no está presente
        if not address.startswith("http://") and not address.startswith("https://"):
            address = f"http://{address}"
        if address.endswith("/"):
            address = address[:-1]
        self.address = address
        self.token = None
        self.miwifi_type = miwifi_type
        self.aiot = None

    def get_infos(self):
        if not self.token:
            print("¡Necesitas iniciar sesión para usar esta función!")
            return None
        response = requests.get(f"{self.address}/cgi-bin/luci/;stok={self.token}/api/misystem/status")
        jdata = response.json()
        if response.status_code == 200 and "hardware" in jdata:
            print(f"Plataforma: {jdata['hardware']['platform']}")
        else:
            print("¡Hubo un problema al recuperar la información!")
            exit(1)

    def set_aiot_status(self, status):
        if not self.token:
            print("¡Necesitas iniciar sesión para usar esta función!")
            return None
        aiotstatus = "ENCENDIDO" if status else "APAGADO"
        print(f"Cambiando el estado del escaneo AIoT a {aiotstatus}...")
        response = requests.post(
            f"{self.address}/cgi-bin/luci/;stok={self.token}/api/xqnetwork/miscan_switch",
            data = {
                "on": str(int(status))
            },
        )
        jdata = response.json()
        if response.status_code == 200:
            self.get_aiot_status()
        else:
            print("¡Hubo un problema al recuperar la información de AIoT!")
            exit(1)

    def get_aiot_status(self):
        if not self.token:
            print("¡Necesitas iniciar sesión para usar esta función!")
            return None
        response = requests.get(f"{self.address}/cgi-bin/luci/;stok={self.token}/api/xqnetwork/get_miscan_switch")
        jdata = response.json()
        if response.status_code == 200 and "enabled" in jdata:
            self.aiot = bool(jdata['enabled'])
            aiotstatus = "ENCENDIDO" if self.aiot else "APAGADO"
            print(f"Estado del escaneo AIoT: {aiotstatus}")
            print("")
            return self.aiot
        else:
            print("¡Hubo un problema al recuperar la información de AIoT!")
            exit(1)

    def get_5ghz_xiaomi(self):
        if not self.token:
            print("¡Necesitas iniciar sesión para usar esta función!")
            return None
        print("Pidiendo al router principal que escanee puntos de acceso WiFi de Xiaomi...")
        response = requests.get(f"{self.address}/cgi-bin/luci/;stok={self.token}/api/xqnetwork/wifi_list")
        jdata = response.json()
        detected = 0
        if response.status_code == 200 and "list" in jdata:
            for ap in jdata["list"]:
                if ap["ssid"].startswith("Xiaomi_") and ap["encryption"] == "NONE":
                    if (ap["band"] == "5g" and ap["ssid"].endswith("_5G")) or (ap["band"] == "2g"):
                        if detected == 0:
                            print("Puntos de acceso detectados:")
                        print(f'\tBanda: {ap["band"]}hz SSID: {ap["ssid"]} CH: {ap["channel"]} MODELO: {ap["wsc_modelname"]} MAC: {ap["bssid"]}')
                        if ap["band"] == "2g":
                            pmac = ap['bssid'].split(":")
                            pmac[-1] = hex(int(pmac[-1], 16) + 1)[2:]
                            pmac = ':'.join(pmac).upper()
                            print(f'\t\tMAC POSIBLE para 5GHz: {pmac}')
                        detected += 1
        if detected == 0:
            print("¡No se detectaron puntos de acceso!\n (¿Están los dispositivos lo suficientemente cerca?)")
            print("Puedes continuar, pero probablemente fallará.")
        print("")

    def login(self, password):
        nonce = generate_nonce(self.miwifi_type)

        response = requests.post(
            f"{self.address}/cgi-bin/luci/api/xqsystem/login",
            data={
                "username": "admin",
                "logtype": "2",
                "password": generate_password_hash(nonce, password),
                "nonce": nonce,
            },
        )
        jdata = response.json()
        if response.status_code == 200 and "token" in jdata:
            self.token = jdata["token"]
            return jdata
        return None

    def add_mesh_node(self, macaddr, location="Estudio"):
        if not self.token:
            print("¡Necesitas iniciar sesión para usar esta función!")
            return None
        response = requests.post(
            f"{self.address}/cgi-bin/luci/;stok={self.token}/api/xqnetwork/add_mesh_node",
            data={
                "mac": macaddr,
                "locate": location
            },
        )
        jdata = response.json()
        if response.status_code == 200 and "code" in jdata and jdata['code'] == 0:
            return jdata
        return None

if __name__ == "__main__":
    print("Agregador de Nodo Mesh MiWiFi v1.2 por Xiaohack \n\n")

    # Obtiene la IP desde los argumentos o usa 'gateway' por defecto
    address_master = f"{sys.argv[1]}" if len(sys.argv) > 1 else f"http://{DEFAULT_HOSTNAME}"
    
    # Muestra la IP a la que se está conectando
    display_ip(address_master)

    # Pide solo la contraseña, ya que la IP ya está definida
    password_master = getpass.getpass(prompt='Contraseña del router principal \n(o escribe "0" para terminar): ')
    if password_master == "0":
        print("Saliendo del programa...")
        sys.exit(0)

    router = MiWiFi(address=address_master)
    print("Iniciando sesión...")
    if not router.login(password_master):
        print("¡Fallo en la autenticación!")
        exit(1)
    print("Inicio de sesión: OK\n")
    
    router.get_infos()
    if not router.get_aiot_status():
        router.set_aiot_status(True)
    router.get_5ghz_xiaomi()

    mac_address_client = prompt_input("Dirección MAC del cliente (5GHz, no configurado) (AA:BB:CC:DD:EE:FF)")
    print(f"Agregando {mac_address_client} como nodo mesh...")
    if router.add_mesh_node(mac_address_client):
        print("Nodo configurado correctamente. Espera a que se reinicie.")
        exit(0)
    else:
        print("¡Algo salió mal!")
        exit(1)
