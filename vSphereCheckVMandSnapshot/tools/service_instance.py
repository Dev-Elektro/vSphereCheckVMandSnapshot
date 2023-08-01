import atexit
from pyVim.connect import SmartConnect, Disconnect
from loguru import logger


def connect(args):
    service_instance = None

    try:
        service_instance = SmartConnect(host=args.get('host'),
                                        user=args.get('user'),
                                        pwd=args.get('password'),
                                        port=args.get('port'),
                                        disableSslCertValidation=args.get('ssl'))
        atexit.register(Disconnect, service_instance)
    except IOError as io_error:
        logger.info(io_error)

    if not service_instance:
        raise SystemExit("Не удалось подключится к хосту.")

    return service_instance
