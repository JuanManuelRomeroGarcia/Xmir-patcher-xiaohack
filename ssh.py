import xmir_base
import paramiko
import sys
import threading
import gateway
import xqmodel

def receive_output(channel):
    """Lee y muestra la salida en tiempo real"""
    while True:
        try:
            if channel.recv_ready():
                output = channel.recv(1024).decode("utf-8", errors="ignore")
                print(output, end="", flush=True)
            if channel.exit_status_ready():
                break
        except Exception as e:
            print(f"\nError recibiendo datos: {e}")
            break

def interactive_ssh(ip):
    try:
        gw = gateway.Gateway(detect_device=False, detect_ssh=False)  # Cargar configuración del gateway
        # Detectar el dispositivo y obtener el nombre y modelo
        gw.detect_device()
        device_name = gw.device_name
        model_id = xqmodel.get_modelid_by_name(device_name)

        
        username = "root"  # Usuario por defecto
        password = gw.passw if gw.passw else input("Ingrese la contraseña SSH: ")
        port = gw.ssh_port if gw.ssh_port else 22  # Puerto por defecto 22

        # Crear cliente SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"\n🔗 Conectando a {ip}:{port} como {username}...\n")
        print(f"🖥️ Modelo detectado: {device_name} (ID: {model_id})\n")

        try:
            client.connect(ip, port, username, password, timeout=5)
        except paramiko.AuthenticationException:
            print("❌ Error: Autenticación fallida. Verifica la contraseña.")
            sys.exit(1)
        except paramiko.SSHException as e:
            print(f"⚠️ Error SSH: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            sys.exit(1)

        # Abrir una sesión interactiva
        channel = client.invoke_shell()
        print("=" * 75)
        print(f"✅ Conectado a {ip}:{port}")
        print("🖥️  Escribe comandos para interactuar con el router")
        print("❌ Para salir, escribe: exit o quit")
        print("=" * 75)

        # Crear un hilo para recibir la salida
        threading.Thread(target=receive_output, args=(channel,), daemon=True).start()
        
        # Leer la entrada del usuario y enviarla al shell
        while True:
            try:
                command = input("> ")
                if command.lower() in ["exit", "quit"]:
                    print("🔴 Cerrando la conexión SSH...")
                    break
                channel.send(command + "\n")
            except KeyboardInterrupt:
                print("\n🔴 Desconectando...")
                break

        # Cerrar la sesión
        channel.close()
        client.close()
        print("✅ Desconectado correctamente.")
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ssh.py <IP>")
        sys.exit(1)
    
    ip_addr = sys.argv[1]  # Recibe la IP desde el menú
    interactive_ssh(ip_addr)
