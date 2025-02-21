#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

import xmir_base
import gateway
from gateway import die
from update_xmir import check_for_update, install_requirements

import os
print(os.getcwd())
gw = gateway.Gateway(detect_device = False, detect_ssh = False)

def get_local_version():
    version_file = os.path.join(os.path.dirname(__file__), "VERSION")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            return f.read().strip()
    return "0.0.0"


def get_header(delim, suffix = ''):
    version = get_local_version()
    update_message = check_for_update()  # Verifica si hay una nueva versión
    
    header = delim * 58 + '\n'
    header += '\n'
    header += ' XiaoHack.es ' + '\n'
    header += '\n'
    header += f' Xiaomi XMiR Patcher (ES) {suffix} \n'
    header += f' (Ver. {version}) {suffix} \n'
    
    if update_message:  # Solo se muestra si hay una actualización
        header += f'{update_message}\n'
    
    header += '\n'
    return header

RESET = "\033[0m"
YELLOW_BOLD = "\033[1;33m"  # Amarillo en negrita

def menu1_show():
  gw.load_config()
  update_message = check_for_update()
  print(get_header('='))
  print(' 1 - Configurar dirección IP (valor actual: {})'.format(gw.ip_addr))
  print(' 2 - Conectar al dispositivo (instalar exploit)')
  print(' 3 - Leer información completa del dispositivo')
  print(' 4 - Crear una copia de seguridad completa')
  print(' 5 - Instalar idiomas ES/EN/RU')
  print(' 6 - Potencia de Antenas Wifi')
  print(' 7 - Instalar firmware (desde el directorio "firmware")')
  if update_message:
    print(f' 8 - {YELLOW_BOLD}{{{{ Otras funciones }}}} ACTUALIZAR XMIR{RESET}')
  else:
      print(' 8 - {{{ Otras funciones }}}')
  print(' 9 - [[ Reiniciar dispositivo ]]')
  print(' 10 - [[ SSH ]]')
  print(' 11 - [[ Apoyar el proyecto (Donaciones) ]]')
  print(' 0 - Salir')


def menu1_process(id):
  if id == 1: 
      ip_addr = input("Introduce la dirección IP del dispositivo: ")
      return ["gateway.py", ip_addr]
  if id == 2: return "connect.py"
  if id == 3: return "read_info.py"
  if id == 4: return "create_backup.py"
  if id == 5: return "install_lang.py"
  if id == 6: return "power.py"
  if id == 7: return "install_fw.py"
  if id == 8: return "__menu2"
  if id == 9: return "reboot.py"
  if id == 10: return ["ssh.py", gw.ip_addr]
  if id == 11: return ["qr.py"]
  if id == 0: sys.exit(0)
  return None


def menu2_show():
  update_message = check_for_update()
  print(get_header('-', '(funciones extendidas)'))
  print(' 1 - Establecer dirección IP (valor actual: {})'.format(gw.ip_addr))
  print(' 2 - Cambiar la contraseña de root')
  print(' 3 - Leer dmesg y syslog')
  print(' 4 - Crear una copia de seguridad de la partición especificada')
  print(' 5 - Desinstalar idiomas ES/EN/RU')
  print(' 6 - Configurar la dirección de arranque del kernel')
  print(' 7 - Instalar SSH permanente')
  print(' 8 - Instalar bootloader Breed')
  print(' 9 - Add Mesh')
  if update_message:
    print(f' 10 - {YELLOW_BOLD}{{{{ [ UPDATE XMIR_XiaoHack ]}}}} ACTUALIZAR XMIR{RESET}')
  else:
    print(' 10 - [[ UPDATE XMIR_XiaoHack ]]')
  print(' 0 - Volver al menú principal')


def menu2_process(id):
  if id == 1:
    ip_addr = input("Enter device IP-address: ")
    return [ "gateway.py", ip_addr ]
  if id == 2: return "passw.py"
  if id == 3: return "read_dmesg.py"
  if id == 4: return [ "create_backup.py", "part" ]
  if id == 5: return [ "install_lang.py", "uninstall" ]
  if id == 6: return "activate_boot.py"
  if id == 7: return "install_ssh.py"
  if id == 8: return ["install_bl.py", "breed"]
  if id == 9: return ["addmesh.py", gw.ip_addr]
  if id == 10: return ["update_xmir.py"]
  if id == 0: return "__menu1" 
  return None

def menu_show(level):
  if level == 1:
      menu1_show()
      return 'Seleccionar: '
  else:
      menu2_show()
      return 'Opción: '


def menu_process(level, id):
  if level == 1:
    return menu1_process(id)
  else:
    return menu2_process(id)

def menu():
  install_requirements()
  level = 1
  while True:
    print('')
    prompt = menu_show(level)
    print('')
    select = input(prompt)
    print('')
    if not select:
      continue
    try:
      id = int(select)
    except Exception:
      id = -1
    if id < 0:
      continue
    cmd = menu_process(level, id)
    if not cmd:
      continue
    if cmd == '__menu1':
      level = 1
      continue
    if cmd == '__menu2':
      level = 2
      continue
    #print("cmd2 =", cmd)
    if isinstance(cmd, str):
      result = subprocess.run([sys.executable, cmd])
    else:  
      result = subprocess.run([sys.executable] + cmd)


menu()


