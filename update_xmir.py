import os
import platform
import stat
import subprocess
import time
import webbrowser
import requests
import zipfile
import shutil
import sys
import importlib.util
import hashlib
from tqdm import tqdm

github_repo = "https://github.com/JuanManuelRomeroGarcia/Xmir-patcher-xiaohack.git"
local_repo_path = os.path.abspath(os.path.dirname(__file__))
version_file = os.path.join(local_repo_path, "VERSION")

EXCLUDED_FOLDERS = {"python12", "update_tmp", "tmp"}
EXCLUDED_FILES = {""}

def get_local_version():
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            return f.read().strip()
    return "0.0.0"

def get_remote_version():
    try:
        response = requests.get("https://raw.githubusercontent.com/JuanManuelRomeroGarcia/Xmir-patcher-xiaohack/main/VERSION")
        if response.status_code == 200:
            return response.text.strip()
    except requests.RequestException:
        return None
    return None

def check_for_update():
    local_version = get_local_version()
    remote_version = get_remote_version()
    
    if remote_version is None:
        return "No se pudo verificar la última versión. Verifique su conexión a Internet."
    elif local_version != remote_version:
        return f"\n[!] Nueva versión disponible ({remote_version}). Versión actual: {local_version}\nPor favor, actualice para mejorar las funciones."
    else:
        return ""

def download_with_progress(url, filepath):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    
    with open(filepath, "wb") as file, tqdm(
        desc="Descargando",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(block_size):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))

def get_file_hash(file_path):
    """ Calcula el hash SHA-256 de un archivo para verificar cambios """
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None  # Si el archivo no existe, es nuevo y debe ser extraído

def extract_modified_files(zip_path, extract_path, local_repo_path):
    """ Extrae solo archivos modificados comparando sus hashes y excluyendo carpetas específicas """
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        file_list = zip_ref.namelist()
        
        # 🔹 Filtrar archivos que pertenecen a carpetas excluidas
        filtered_files = [
            file for file in file_list 
            if not any(file.startswith(f"{folder}/") or file.startswith(f"{folder}\\") or f"/{folder}/" in file or f"\\{folder}\\" in file 
                       for folder in EXCLUDED_FOLDERS) and os.path.basename(file) not in EXCLUDED_FILES 
        ]
        
        modified_files = []  # Lista de archivos modificados

        with tqdm(total=len(filtered_files), desc="Verificando archivos", unit="archivo") as progress:
            for file in filtered_files:
                if file.endswith("/") or file.endswith("\\"):  # Ignorar directorios
                    progress.update(1)
                    continue
                
                extracted_file_path = os.path.join(extract_path, file)
                local_file_path = os.path.join(local_repo_path, file.replace("Xmir-patcher-xiaohack-main/", ""))

                zip_ref.extract(file, extract_path)  # Extrae temporalmente

                extracted_hash = get_file_hash(extracted_file_path)
                local_hash = get_file_hash(local_file_path)

                if extracted_hash == local_hash:
                    os.remove(extracted_file_path)  # Elimina el archivo extraído si no cambió
                else:
                    modified_files.append(file.replace("Xmir-patcher-xiaohack-main/", ""))  # Guarda el nombre del archivo

                progress.update(1)

        return modified_files  # Devuelve la lista de archivos modificadosificados

def update_repository():
    print("Descargando la última versión de Xmir Patcher...")

    zip_url = "https://github.com/JuanManuelRomeroGarcia/Xmir-patcher-xiaohack/archive/refs/heads/main.zip"
    zip_path = os.path.join(local_repo_path, "update.zip")
    extract_path = os.path.join(local_repo_path, "update_tmp")

    try:
        download_with_progress(zip_url, zip_path)  

        modified_files = extract_modified_files(zip_path, extract_path, local_repo_path)

        if not modified_files:
            print("✅ No se encontraron archivos nuevos o modificados. No es necesario actualizar.")
            return

        print(f"✅ Se actualizaron {len(modified_files)} archivos:")
        for file in modified_files:
            print(f"   📂 {file}")  # Muestra los archivos modificados

        extracted_folder = os.path.join(extract_path, "Xmir-patcher-xiaohack-main")
        for root, _, files in os.walk(extracted_folder):
            for file in files:
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, extracted_folder)
                dest_path = os.path.join(local_repo_path, relative_path)

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                try:
                    if os.path.exists(dest_path):
                        os.remove(dest_path)  # Eliminar antes de reemplazar
                    shutil.move(source_path, dest_path)
                except PermissionError:
                    print(f"⚠️ No se pudo sobrescribir: {dest_path} (Archivo en uso o sin permisos)")

        print("✅ Actualización archivos completada con éxito.")

        os.remove(zip_path)
        shutil.rmtree(extract_path, ignore_errors=True)
        
        latest_release_url = "https://github.com/JuanManuelRomeroGarcia/Xmir-patcher-xiaohack/releases/latest"
        print(f"🔗 Redirigiendo a la última versión en GitHub: {latest_release_url}")
        webbrowser.open(latest_release_url)
        
    except Exception as e:
        print(f"❌ Error al actualizar: {e}")
        
ESSENTIAL_PACKAGES = {"pip", "setuptools", "wheel", "requests", "urllib3", "certifi", "charset_normalizer", "idna", 
                      "paramiko", "pyftpdlib", "pyasyncore","pyasynchat", "cffi", "pycparser", "cryptography", 
                      "bcrypt", "pynacl", "ssh2-python"}

def get_python_executable():
    """ Devuelve la ruta correcta de Python dependiendo del sistema operativo y entorno virtual """
    if "VIRTUAL_ENV" in os.environ:
        return sys.executable
    
    base_path = os.path.dirname(__file__)

    if platform.system() == "Windows":
        return os.path.join(base_path, "python12", "python.exe")
    
    python_exe = os.path.join(base_path, "python12", "bin", "python3")
    
    if not os.path.exists(python_exe):
        return "python3"
    
    return python_exe

def ensure_executable(file_path):
    """ Asegura que el archivo tenga permisos de ejecución en Linux/macOS, excepto en venv """
    if platform.system() != "Windows" and os.path.exists(file_path):
        if "VIRTUAL_ENV" not in os.environ:
            st = os.stat(file_path)
            os.chmod(file_path, st.st_mode | stat.S_IEXEC)

def normalize_package_name(package_name):
    """ Normaliza el nombre del paquete para evitar errores de comparación """
    return package_name.replace("-", "_").lower()

def extract_package_name(requirement_line):
    """ Extrae el nombre del paquete sin versiones ni condiciones de Python """
    return normalize_package_name(requirement_line.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].split(";")[0].strip())

def get_installed_packages():
    """ Obtiene la lista de paquetes instalados en el entorno actual """
    python_exe = get_python_executable()

    try:
        result = subprocess.run(
            [python_exe, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True
        )
        installed_packages = {extract_package_name(line) for line in result.stdout.splitlines() if "==" in line}

        pip_check = subprocess.run(
            [python_exe, "-m", "pip", "--version"],
            capture_output=True,
            text=True
        )
        if "pip" in pip_check.stdout:
            installed_packages.add("pip")

        return installed_packages
    except subprocess.CalledProcessError:
        return set()

def install_requirements():
    """ Verifica, instala y evita la eliminación de paquetes esenciales con barra de progreso """
    python_exe = get_python_executable()
    ensure_executable(python_exe)
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

    if not os.path.exists(requirements_file):
        print("⚠️ No se encontró requirements.txt, saltando verificación de paquetes.")
        return
    
    try:
        print("🔍 Verificando dependencias...")

        pip_check = subprocess.run(
            [python_exe, "-m", "pip", "--version"],
            capture_output=True,
            text=True
        )
        if "pip" not in pip_check.stdout:
            print("⚠️ Pip no está instalado. Instalándolo...")
            subprocess.run([python_exe, "-m", "ensurepip"], check=True)
            subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], check=True)

        with open(requirements_file, "r") as f:
            required_packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        required_package_names = {extract_package_name(pkg) for pkg in required_packages}

        installed_packages = get_installed_packages()

        missing_packages = [pkg for pkg in required_packages if extract_package_name(pkg) not in installed_packages]
        
        packages_to_remove = installed_packages - required_package_names - {normalize_package_name(pkg) for pkg in ESSENTIAL_PACKAGES}

        cambios_realizados = False

        if missing_packages:
            print(f"📦 Instalando paquetes faltantes: {', '.join(missing_packages)}")
            with tqdm(total=len(missing_packages), desc="Instalando", unit="pkg") as progress:
                for pkg in missing_packages:
                    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "-q", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    progress.update(1)
            cambios_realizados = True

        if packages_to_remove:
            print(f"🗑️ Eliminando paquetes innecesarios: {', '.join(packages_to_remove)}")
            with tqdm(total=len(packages_to_remove), desc="Eliminando", unit="pkg") as progress:
                for pkg in packages_to_remove:
                    subprocess.run([python_exe, "-m", "pip", "uninstall", "-y", "-q", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    progress.update(1)
            cambios_realizados = True

        if not cambios_realizados:
            print("✅ Todos los paquetes necesarios ya están instalados.")
        else:
            print("✅ Actualización de dependencias completada.")

    except Exception as e:
        print(f"❌ Error verificando o instalando dependencias: {e}")


if __name__ == "__main__":
    update_message = check_for_update()
    
    if update_message:
        print(update_message)
    else:
        print("✅ No hay actualizaciones disponibles. El sistema está actualizado.")
        
        # 🔹 Preguntar si desea verificar archivos manualmente
        while True:
            verificar = input("¿Desea volver a verificar los archivos por si algo se borró? (s/n): ").strip().lower()
            if verificar in ["s", "n"]:
                break
            print("⚠️ Entrada no válida. Por favor, escriba 's' para verificar o 'n' para omitir.")
        
        if verificar == "s":
            print("\n🔍 Verificando archivos nuevamente...")
            update_repository()
            install_requirements()
            print("✅ Verificación de archivos completada.")
            sys.exit(0)
        else:
            print("🔹 No se realizó ninguna verificación adicional.")
            sys.exit(0)

    if "Nueva versión disponible" in update_message:
        while True:  # Bucle para validar la entrada del usuario
            actualizar = input("¿Desea actualizar ahora? (s/n): ").strip().lower()
            if actualizar in ["s", "n"]:
                break  # Salimos del bucle si la entrada es válida
            print("⚠️ Entrada no válida. Por favor, escriba 's' para actualizar o 'n' para omitir.")

        if actualizar == "s":
            update_repository()
            install_requirements()
            print("\n¡Actualización exitosa! Reiniciando el programa...")

            os.system("taskkill /F /IM cmd.exe")
            sys.exit(0)
            
        else:
            print("⏳ La actualización fue omitida. Regresando al menú principal...\n")
            sys.exit(0)