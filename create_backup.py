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
sn = gw.device_info.get('id', None)

print("device_name =", gw.device_name)
print("rom_version = {} {}".format(gw.rom_version, gw.rom_channel))
print("SN = {}".format(sn))
print("----------------------------------")

# Verificar que el modelo esté disponible
if not gw.device_name:
    die("No se pudo obtener el modelo del router.")
    
if not sn:
    die("No se pudo obtener el número de serie (SN) del router.")


# Eliminar caracteres no alfanuméricos del modelo para usarlo como nombre de carpeta
router_model = ''.join(e for e in gw.device_name if e.isalnum())
sn_sanitized = sn.replace('/', '_')

# Crear el nombre de la carpeta basada en el modelo del router
fn_dir = f'backups/{router_model}/{sn_sanitized}/'
fn_old = fn_dir + 'full_dump.old'
fn_local = fn_dir + 'full_dump.bin'
fn_remote = '/tmp/mtd_dump.bin'
a_part = None
pid = None

if len(sys.argv) > 1:
    for p, part in enumerate(dev.partlist):
        print('  %2d > addr: 0x%08X  size: 0x%08X  name: "%s"' % (p, part['addr'], part['size'], part['name']))
    print(" ")
    a_part = input("Enter partition name or mtd number: ")
    if a_part != 'a':
        try:
            i_part = int(a_part)
        except:
            i_part = None
        if i_part is not None:
            p = i_part
            if p < 0 or p >= len(dev.partlist):
                die('Partition "mtd{}" not found!'.format(a_part))
        else:
            p = dev.get_part_num(a_part)
            if p < 0:
                die('Partition "{}" not found!'.format(a_part))
        name = dev.partlist[p]['name']
        name = ''.join(e for e in name if e.isalnum())
        fn_old = fn_dir + 'mtd{id}_{name}.old'.format(id=p, name=name)
        fn_local = fn_dir + 'mtd{id}_{name}.bin'.format(id=p, name=name)
        pid = p

# Crear la carpeta si no existe
os.makedirs(fn_dir, exist_ok=True)

if pid is None and a_part != 'a':
    for p, part in enumerate(dev.partlist):
        if part['addr'] == 0 and part['size'] > 0x00800000:  # 8MiB
            pid = p
            name = dev.partlist[p]['name']  # "ALL"
            name = ''.join(e for e in name if e.isalnum())
            addr = dev.partlist[p]['addr']
            size = dev.partlist[p]['size']
            break

if pid is not None:
    if os.path.exists(fn_dir): 
        if os.path.exists(fn_local): 
            if os.path.exists(fn_old):
                os.remove(fn_old)
            os.rename(fn_local, fn_old)
    if a_part is None:
        print("Full backup creating...")
    gw.run_cmd("dd if=/dev/mtd{id} of={o}".format(id=pid, o=fn_remote))
    print('Dump of partition "{}" created!'.format(name))
    print('Download dump to file "./{}"...'.format(fn_local))
    gw.download(fn_remote, fn_local, verbose=0)
    print("Completed!")
    gw.run_cmd("rm -f " + fn_remote)
    print(" ")
    if a_part is None:
        print('Full backup saved to file "./{}"'.format(fn_local))
    else:
        print('Backup of "{}" saved to file "./{}"'.format(name, fn_local))
else:
    print("Full backup creating...")
    for p, part in enumerate(dev.partlist):
        if part['addr'] == 0 and part['size'] > 0x00800000:  # 8MiB
            continue  # skip "ALL" part
        name = dev.partlist[p]['name']
        name = ''.join(e for e in name if e.isalnum())
        addr = dev.partlist[p]['addr']
        size = dev.partlist[p]['size']
        fn_old = fn_dir + 'mtd{id}_{name}.old'.format(id=p, name=name)
        fn_local = fn_dir + 'mtd{id}_{name}.bin'.format(id=p, name=name)    
        if os.path.exists(fn_dir): 
            if os.path.exists(fn_local): 
                if os.path.exists(fn_old):
                    os.remove(fn_old)
                os.rename(fn_local, fn_old)
        cmd = "dd if=/dev/mtd{id} of={o}".format(id=p, o=fn_remote)
        ret = gw.run_cmd(cmd, timeout=30, die_on_error=False)
        if not ret:
            print('ERROR on execute command: "{}"'.format(cmd))
        else:
            print('Download dump to file "./{}"...'.format(fn_local))
            try:
                gw.download(fn_remote, fn_local, verbose=0)
            except Exception:
                print('Remote file "{}" not found!'.format(fn_remote))
                continue
        gw.run_cmd("rm -f " + fn_remote)
        if ret:
            print('Backup of "{}" saved to file "./{}"'.format(name, fn_local))
    print(" ")
    print("Completed!")
