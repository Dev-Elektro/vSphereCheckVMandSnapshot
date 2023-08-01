import configparser
import os
import sys


def create_default_config(path: str):
    """
    Создает шаблон конфигурационного файла.
    """

    config = configparser.ConfigParser()
    config.add_section("vCenter")
    config.set("vCenter", "host", "host.vcenter.ru")
    config.set("vCenter", "port", "443")
    config.set("vCenter", "user", "login")
    config.set("vCenter", "password", "****")
    config.set("vCenter", "ssl", "False")

    config.add_section("Alert")
    config.set("Alert", "lvl_day", "15")

    config.add_section("Mail")
    config.set("Mail", "smtp", "smtp.mail.ru")
    config.set("Mail", "subject", "Warning. vSphereCheckVM")
    config.set("Mail", "from", "from@mail.ru")
    config.set("Mail", "to", "to@mail.ru")
    config.set("Mail", "login", "smtp_login")
    config.set("Mail", "password", "smtp_pass")

    config.add_section("Logging")
    config.set("Logging", "path", "/path/to/logs.log")
    config.set("Logging", "rotation", "5 MB")

    with open(path, "w") as config_file:
        config.write(config_file)


def open_config(path: str):
    """
    Открыть на редактирование файл конфига, если его нет создать по шаблону.
    """

    if not os.path.exists(path):
        create_default_config(path)

    if sys.platform.startswith("win32"):
        os.system(f"start {path}")
    else:
        cmd = "nano" if os.path.exists("/bin/nano") else "vi"
        os.system(f"{cmd} {path}")


def get_config(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path}: not found")

    config = configparser.ConfigParser(interpolation=None)
    config.read(path)
    return config
