# vSphereCheckVMandSnapshot

Проверка сбойных хостов и наличие снапшотов старше указанного времени.

## Установка

Windows `pip install git+https://github.com/Dev-Elektro/vSphereCheckVMandSnapshot.git#egg=vSphereCheckVMandSnapshot`

Linux, Mac `sudo pip install git+https://github.com/Dev-Elektro/vSphereCheckVMandSnapshot.git#egg=vSphereCheckVMandSnapshot`

## Использование

### Создание или редактирование конфигурационного файла

`check_vm_and_snapshot --config config.ini -edit`

### Запуск проверки 

`check_vm_and_snapshot --config config.ini`
