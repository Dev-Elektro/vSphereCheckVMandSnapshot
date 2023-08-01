from setuptools import setup

setup(
    name='vSphereCheckVMandSnapshot',
    version='0.1',
    packages=['vSphereCheckVMandSnapshot', 'vSphereCheckVMandSnapshot.tools'],
    include_package_data=True,
    url='https://github.com/Dev-Elektro/vSphereCheckVMandSnapshot',
    license='MIT license',
    author='Dev-Elektro',
    author_email='elektro.linux@gmail.com',
    description='Dev-Elektro',

    install_requires=[
        'colorama~=0.4.6',
        'loguru~=0.7.0',
        'prettytable~=3.8.0',
        'pyvmomi~=8.0.1.0.2'
    ],

    entry_points={
        'console_scripts':
            ['check_vm_and_snapshot = vSphereCheckVMandSnapshot.main:main']
    },
    python_requires=">=3.11",
    zip_safe=True
)
