#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import xmir_base
import gateway
from gateway import die
import read_info
from tqdm import tqdm

gw = gateway.Gateway()
dev = read_info.DevInfo(verbose=0, infolevel=1)
dev.get_dmesg()
dev.get_part_table()

if not dev.partlist or len(dev.partlist) <= 1:
    die("¡La lista de particiones está vacía!")

sn = gw.device_info.get('id', None)
if not gw.device_name:
    die("No se pudo obtener el modelo del router.")
if not sn:
    die("No se pudo obtener el número de serie (SN) del router.")

router_model = ''.join(e for e in gw.device_name if e.isalnum())
sn_sanitized = sn.replace('/', '_')

fn_dir = f'backups/{router_model}/{sn_sanitized}/'
os.makedirs(fn_dir, exist_ok=True)

def backup_and_download(pid, filename, part_size, file_bar):
    os.remove(filename) if os.path.exists(filename) else None
    with open(filename, 'wb') as file:
        pass
    
    fn_remote = f'/tmp/dump_mtd.bin'
    blk_size = 20*1024*1024
    dump_size = 0
    
    file_bar.reset()
    file_bar.total = part_size
    file_bar.refresh()
    
    error_count = 0
    max_errors = 3  # Número máximo de errores permitidos antes de saltar la partición
    
    while dump_size < part_size:
        if error_count >= max_errors:
            print(f'ERROR: Se superó el límite de errores en la partición mtd{pid}. Saltando...')
            return False
        
        skip = dump_size // blk_size
        fn_local = fn_dir + f'dump_mtd{pid}_{skip}.bin'
        os.remove(fn_local) if os.path.exists(fn_local) else None
        
        cmd = f"rm -f {fn_remote} ; dd if=/dev/mtd{pid} of={fn_remote} bs={blk_size} count=1 skip={skip}"
        ret = gw.run_cmd(cmd, timeout=25, die_on_error=False)

        if ret is None:
            print(f'ERROR al ejecutar el comando: "{cmd}"')
            error_count += 1
            continue  # Continuar con el siguiente bloque en caso de error
        
        try:
            gw.download(fn_remote, fn_local, verbose=0)
        except Exception:
            print(f'ERROR: ¡Archivo remoto "{fn_remote}" no encontrado!')
            error_count += 1
            continue  # Continuar con el siguiente bloque en caso de error
        
        if not os.path.exists(fn_local):
            print(f'ERROR: ¡Archivo "{fn_local}" no encontrado!')
            error_count += 1
            continue  # Continuar con el siguiente bloque en caso de error
        
        error_count = 0  # Resetear contador si no hubo error
        chunk_size = os.path.getsize(fn_local)
        if chunk_size:
            with open(fn_local, 'rb') as file:
                data = file.read()
            with open(filename, 'ab+') as file:
                file.write(data)
        
        dump_size += chunk_size
        file_bar.update(chunk_size)
        os.remove(fn_local)
    
    gw.run_cmd("rm -f " + fn_remote)
    return True

def select_partition():
    print("\nLista de particiones disponibles:")
    for p, part in enumerate(dev.partlist):
        print(f'  {p:2d} > addr: 0x{part["addr"]:08X}  size: 0x{part["size"]:08X}  name: "{part["name"]}"')
    print(" ")
    a_part = input("Introduce el nombre de la partición o el número de mtd: ")
    return int(a_part) if a_part.isdigit() else dev.get_part_num(a_part)

print("Iniciando respaldo...")
selected_pid = None
if len(sys.argv) > 1:
    selected_pid = select_partition()

with tqdm(total=1, unit='B', unit_scale=True, desc='Archivo actual', position=0, leave=True) as file_bar:
    for part_index, part in enumerate(dev.partlist):
        if selected_pid is not None and part_index != selected_pid:
            continue  # Respaldar solo la partición seleccionada
        
        if part['addr'] == 0 and part['size'] > 0x00800000:
            continue  # Omitir partición "ALL"
        
        name = ''.join(e for e in part['name'] if e.isalnum())
        fn_local = fn_dir + f'mtd{part_index}_{name}.bin'
        
        if backup_and_download(part_index, fn_local, part['size'], file_bar):
            file_bar.clear()  # Limpia la barra actual antes de imprimir el mensaje
            print(f'✔ Respaldo de "{name}" guardado en "{fn_local}"')
        else:
            print(f'✖ No se pudo respaldar "{name}". Se omitió.')

print("\n✔ ¡Respaldo completado!")
