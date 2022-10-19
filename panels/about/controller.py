"""Controller for about panel."""
import json
import subprocess
import platform
import psutil


from .models import Hardware, Software


def _read(name):
    """Reads a system file with @name and returns its content."""
    with open(f"/sys/devices/virtual/dmi/id/{name}", encoding="utf-8") as file:
        return file.read().strip()

class Controller:
    """Controller for about panel."""
    def get_hostname(self):
        """Returns system's hostname."""
        return platform.uname()[1]

    def set_hostname(self, hostname):
        """
        Validates @hostname, then sets it as the system's hostname.
        Returns True if the hostname was set, False otherwise.
        """
        if not 1 <= len(hostname) <= 63:
            return False

        if hostname[0] == "-":
            return False

        if hostname.replace("-", "").isalnum():
            subprocess.check_output(['hostnamectl', 'set-hostname', hostname])
            return True

        return False

    def get_hardware_info(self):
        """Returns hardware information"""
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

    def get_software_info(self):
        """Returns software information"""
        with open('/etc/os-release', encoding="utf-8") as file:
            os_info = dict(line.strip().split('=', 1) for line in file if '=' in line)

            os_name = os_info['PRETTY_NAME'].strip('"')
            os_build = os_info['BUILD_ID'].strip('"')

        return Software(
            os_name=f"{os_name} ({os_build})",
            os_type=platform.architecture()[0],
            kernel=psutil.os.uname().release,
        )

