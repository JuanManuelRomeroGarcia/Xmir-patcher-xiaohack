#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import xmir_base
import gateway
from gateway import die
import read_info

gw = gateway.Gateway()
dev = read_info.DevInfo(verbose=0, infolevel=1)
dev.get_dmesg()
dev.get_part_table()

if not dev.partlist or len(dev.partlist) <= 1:
    die("¡La lista de particiones está vacía!")

# Obtener el modelo del router y el número de serie
sn = gw.device_info.get('id', None)
if not gw.device_name:
    die("No se pudo obtener el modelo del router.")
if not sn:
    die("No se pudo obtener el número de serie (SN) del router.")

# Eliminar caracteres no alfanuméricos para nombres de carpetas seguros
router_model = ''.join(e for e in gw.device_name if e.isalnum())
sn_sanitized = sn.replace('/', '_')

# Crear la carpeta basada en el modelo del router y SN
fn_dir = f'backups/{router_model}/{sn_sanitized}/'
fn_old = fn_dir + 'full_dump.old'
fn_local = fn_dir + 'full_dump.bin'
fn_remote = '/tmp/mtd_dump.bin'

os.makedirs(fn_dir, exist_ok=True)

a_part = None
pid = None

if len(sys.argv) > 1:
    for p, part in enumerate(dev.partlist):
        print('  %2d > addr: 0x%08X  size: 0x%08X  name: "%s"' % (p, part['addr'], part['size'], part['name']))
    print(" ")
    a_part = input("Introduce el nombre de la partición o el número de mtd: ")
    if a_part != 'a':
        try:
            i_part = int(a_part)
        except:
            i_part = None
        if i_part is not None:
            p = i_part
            if p < 0 or p >= len(dev.partlist):
                die('¡Partición "mtd{}" no encontrada!'.format(a_part))
        else:
            p = dev.get_part_num(a_part)
            if p < 0:
                die('¡Partición "{}" no encontrada!'.format(a_part))
        name = dev.partlist[p]['name']
        name = ''.join(e for e in name if e.isalnum())
        fn_old = fn_dir + 'mtd{id}_{name}.old'.format(id=p, name=name)
        fn_local = fn_dir + 'mtd{id}_{name}.bin'.format(id=p, name=name)
        pid = p

if pid is None and a_part != 'a':
    for p, part in enumerate(dev.partlist):
        if part['addr'] == 0 and part['size'] > 0x00800000:  # 8MiB
            pid = p
            name = dev.partlist[p]['name']
            name = ''.join(e for e in name if e.isalnum())
            break

def backup_and_download(pid, filename, die_on_error=True):
    global fn_dir
    os.remove(filename) if os.path.exists(filename) else None
    with open(filename, 'wb') as file:
        pass
    part_size = dev.partlist[pid]["size"]
    fn_remote = f'/tmp/dump_mtd.bin'
    blk_size = 20*1024*1024
    dump_size = 0
    
    while dump_size < part_size:
        skip = dump_size // blk_size
        fn_local = fn_dir + f'dump_mtd{pid}_{skip}.bin'
        os.remove(fn_local) if os.path.exists(fn_local) else None
        
        cmd = f"rm -f {fn_remote} ; dd if=/dev/mtd{pid} of={fn_remote} bs={blk_size} count=1 skip={skip}"
        ret = gw.run_cmd(cmd, timeout=25, die_on_error=False)

        if not ret:
            print(f'ERROR al ejecutar el comando: "{cmd}"')
            if die_on_error:
                sys.exit(1)
            return False

        print(f'Descargando archivo "./{fn_local}"...')
        try:
            ret = gw.download(fn_remote, fn_local, verbose=0)
        except Exception:
            print(f'ERROR: ¡Archivo remoto "{fn_remote}" no encontrado!')
            if die_on_error:
                sys.exit(1)
            return False

        if not os.path.exists(fn_local):
            print(f'ERROR: ¡Archivo "{fn_local}" no encontrado!')
            if die_on_error:
                sys.exit(1)
            return False

        chunk_size = os.path.getsize(fn_local)
        if chunk_size:
            with open(fn_local, 'rb') as file:
                data = file.read()
            with open(filename, 'ab+') as file:
                file.write(data)

        dump_size += chunk_size
        os.remove(fn_local)

    gw.run_cmd("rm -f " + fn_remote)
    print(f'¡Archivo "{filename}" creado!')
    return True

if pid is not None:
    if os.path.exists(fn_dir):
        if os.path.exists(fn_local):
            if os.path.exists(fn_old):
                os.remove(fn_old)
            os.rename(fn_local, fn_old)

    if a_part is None:
        print("Creando respaldo completo...")

    backup_and_download(pid, fn_local)
    print(" ")

    if a_part is None:
        print('Respaldo completo guardado en "./{}"'.format(fn_local))
    else:
        print('Respaldo de "{}" guardado en "./{}"'.format(name, fn_local))

else:
    print("Creando respaldo completo...")
    for p, part in enumerate(dev.partlist):
        if part['addr'] == 0 and part['size'] > 0x00800000:
            continue  # omitir partición "ALL"

        name = dev.partlist[p]['name']
        name = ''.join(e for e in name if e.isalnum())
        fn_old = fn_dir + 'mtd{id}_{name}.old'.format(id=p, name=name)
        fn_local = fn_dir + 'mtd{id}_{name}.bin'.format(id=p, name=name)

        if os.path.exists(fn_dir):
            if os.path.exists(fn_local):
                if os.path.exists(fn_old):
                    os.remove(fn_old)
                os.rename(fn_local, fn_old)

        backup_and_download(p, fn_local)

        print('Respaldo de "{}" guardado en "./{}"'.format(name, fn_local))

    print(" ")
    print("¡Respaldo completado!")
