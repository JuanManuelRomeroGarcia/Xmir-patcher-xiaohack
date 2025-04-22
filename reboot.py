#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import platform

import xmir_base
import gateway
from gateway import die


gw = gateway.Gateway(detect_ssh = False)

ssh = gw.detect_ssh(verbose = 1, interactive = True)
if ssh > 0:
  print('Enviando comando "reboot" vía SSH ...')
  gw.run_cmd("reboot", reboot = True)
  time.sleep(1)
else:
  if not gw.stok:
    gw.web_login()
  print('Enviando comando "reboot" vía API WEB ...')
  if not gw.reboot_device():
    die('No se puede ejecutar el comando de reinicio.')

if not gw.wait_shutdown(10):
  die('El comando "reboot" no apagó el dispositivo.')

print("¡Reinicio activado!")
