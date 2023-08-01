from datetime import datetime, timezone
import sys
from pyVmomi import vim
from vSphereCheckVMandSnapshot.tools import cli, mail, config_utils, service_instance
from prettytable import PrettyTable
from loguru import logger


def get_status_hosts(content):
    container_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], recursive=True)
    children = container_view.view
    table_hosts = PrettyTable(['Хост', 'Статус', 'Связь с vCenter'])
    host_count = 0
    for child in children:
        power_state = child.summary.runtime.powerState
        conn_state = child.summary.runtime.connectionState
        if conn_state != 'connected' or power_state != 'poweredOn':
            host_count += 1
            table_hosts.add_row([child.summary.config.name, power_state, conn_state])
    return table_hosts, host_count


def get_snapshots(snapshots):
    snap_obj = []
    for snapshot in snapshots:
        snap_obj.append(snapshot)
        snap_obj = snap_obj + get_snapshots(snapshot.childSnapshotList)
    return snap_obj


def get_status_snapshots(content, trigger):
    container_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], recursive=True)
    children = container_view.view
    table_snapshots = PrettyTable(['Имя машины', 'Название', 'Описание', 'Дата создания', 'Возраст'])
    snapshot_count = 0
    for child in children:
        if child.snapshot:
            snapshot_list = list(filter(lambda s: (datetime.now(timezone.utc) - s.createTime).days >= trigger,
                                        get_snapshots(child.snapshot.rootSnapshotList)))
            for snapshot in snapshot_list:
                snapshot_count += 1
                table_snapshots.add_row([
                    child.name,
                    snapshot.name,
                    snapshot.description,
                    snapshot.createTime,
                    datetime.now(timezone.utc) - snapshot.createTime
                ])
    return table_snapshots, snapshot_count


def main():
    parser = cli.Parser()
    args = parser.get_args()

    if args.edit:
        config_utils.open_config(args.config)
        sys.exit(0)

    config = config_utils.get_config(args.config)
    logger.add(config['Logging'].get('path'), rotation=config['Logging'].get('rotation'))
    buf_msg = ""

    logger.info("Connect to vCenter...")
    si = service_instance.connect(config["vCenter"])
    content = si.RetrieveContent()

    logger.info("Проверка статуса хостов")
    table_hosts, host_count = get_status_hosts(content)
    logger.info(f"Количество сбойных хостов: {host_count}")
    logger.info(f"\n{table_hosts}")
    if host_count:
        buf_msg += f"Количество сбойных хостов: {host_count}<br>"
        buf_msg += f"{table_hosts.get_html_string(attributes={'border': 1, 'style': 'border-width: 1px;'})}<br><br>"
    logger.info("Проверка snapshots")
    table_snapshots, snapshot_count = get_status_snapshots(content, int(config['Alert'].get('lvl_day')))
    logger.info(f"Количество snapshot старше {config['Alert'].get('lvl_day')} дней: {snapshot_count}")
    logger.info(f"\n{table_snapshots}")
    if snapshot_count:
        buf_msg += f"Количество snapshot старше {config['Alert'].get('lvl_day')} дней: {snapshot_count}<br>"
        buf_msg += table_snapshots.get_html_string(attributes={'border': 1, 'style': 'border-width: 1px;'})

    if buf_msg:
        logger.info("Отправка письма.")
        mail.send_mail(config['Mail'], buf_msg)


if __name__ == '__main__':
    main()
