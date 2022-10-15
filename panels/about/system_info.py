"""Module to fetch system information"""
import json
import subprocess
from dataclasses import dataclass
import platform

import psutil

@dataclass
class Hardware:
    """Hardware class"""
    processor: str
    cores: int
    memory: int
    disk: int
    product_name: str
    vendor: str
    graphics: str

@dataclass
class Software:
    """Software class"""
    os_name: str
    os_type: str
    kernel: str

def get_hostname():
    """Get hostname"""
    return platform.uname()[1]

def set_hostname(hostname):
    """Set hostname"""
    subprocess.check_output(['hostnamectl', 'set-hostname', hostname])

def validate_hostname(hostname):
    """Validate hostname"""
    if not 1 <= len(hostname) <= 63:
        return False

    if hostname[0] == "-":
        return False

    return hostname.replace("-", "").isalnum()

def _read(name):
    """Read file"""
    with open(f"/sys/devices/virtual/dmi/id/{name}", encoding="utf-8") as file:
        return file.read().strip()

def get_hardware_info():
    """Get hardware information"""
    cpu_info = json.loads(subprocess.check_output(['lscpu', '-J']))
    gpu_info = json.loads(subprocess.check_output(['lshw', '-c', 'video', '-json']))

    return Hardware(
        processor=cpu_info['lscpu'][7]['data'],
        cores=psutil.cpu_count(),
        memory=psutil.virtual_memory().total / 1024 ** 3,
        disk=psutil.disk_usage('/').total / 1024 ** 3,
        product_name=_read('product_name'),
        vendor=_read('sys_vendor'),
        graphics=gpu_info[0]["product"],
    )

def get_software_info():
    """Get software information"""
    with open('/etc/os-release', encoding="utf-8") as file:
        os_info = dict(line.strip().split('=', 1) for line in file if '=' in line)

        os_name = os_info['PRETTY_NAME'].strip('"')
        os_build = os_info['BUILD_ID'].strip('"')

    return Software(
        os_name=f"{os_name} ({os_build})",
        os_type=platform.architecture()[0],
        kernel=psutil.os.uname().release,
    )
