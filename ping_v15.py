import socket     #Libreria para obtener la IP del equipo
import subprocess #Libreria para enviar el ping por la entrada estandar
import asyncio    #Libreria de TIMER asincrono
import platform   #Libreria para la detección del SO
import os         #Libreria para caprutar la salida estandar de la consol
from tqdm.asyncio import tqdm #Libreria para la barra de progreso

async def obtener_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

async def obtener_rango(ip):
    partes_ip = ip.split('.')[:3]
    rango = '.'.join(partes_ip) + '.'
    return rango

async def ping_equipo(ip):
    try:
        if platform.system().lower() == 'windows':
            proceso = await asyncio.create_subprocess_shell(f"ping -n 1 {ip}", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            proceso = await asyncio.create_subprocess_shell(f"ping -c 1 {ip}", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        await asyncio.wait_for(proceso.communicate(), timeout=0.25)
        return proceso.returncode == 0
    except asyncio.TimeoutError:
        return False

async def escanear_ips(rango, archivo, barra_progreso):
    ips_responden = []


    for i in tqdm(range(1, 256), desc="Escaneando IPs", position=0, leave=True, disable=not barra_progreso):
        ip = f"{rango}{i}"
        if await ping_equipo(ip):
            ips_responden.append(ip)

   
    with open("scan.txt", "w") as archivo_scan:
        for ip in ips_responden:
            archivo_scan.write(ip + "\n")

    return ips_responden

async def main():

    mi_ip = await obtener_ip()
    print(f"Mi IP: {mi_ip}")

    rango = await obtener_rango(mi_ip)
    print(f"Escaneando el rango: {rango}1-255")
    barra_progreso = True
    ips_responden = await escanear_ips(rango, None, barra_progreso)
    print("""
          """)
    print("IPs de equipos que responden al ping:")
    print()
    for ip in ips_responden:
        print(f'>>> {ip}')
    print()
    print(f'Se ha creado un archivo scan.txt con la lista de IPs en el directorio {os.getcwd()}')
    print()

def intro():
    print("""
┌──────────────────────────────────────────────────┐
│                                                  │
│  ASIR 1        PYTHON PING v 1.5                 │
│                                                  │
│                                                  │
│            CREADO POR VÍCTOR JIMÉNEZ             │
│                                                  │
│                  Licencia GPL                    │
│                                                  │
└──────────────────────────────────────────────────┘""")
    
if __name__ == "__main__":
    intro()
    print()
    asyncio.run(main())



