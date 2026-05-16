import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-attendance-machine",
    description="Meta package for open-synergy-ssi-attendance-machine Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_attendance_machine',
        'odoo14-addon-ssi_attendance_machine_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
