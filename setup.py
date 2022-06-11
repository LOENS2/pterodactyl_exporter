from setuptools import setup, find_packages
import pterodactyl_exporter

setup(
    name='pterodactyl_exporter',
    version=pterodactyl_exporter.__version__,
    packages=find_packages(),
    url='https://github.com/LOENS2/pterodactyl_exporter',
    license=pterodactyl_exporter.__license__,
    author=pterodactyl_exporter.__author__,
    author_email='info@loens2.com',
    description='Metrics exporter for Pterodactyl',
    install_requires=open('requirements.txt').readlines(),
    entry_points={
            'console_scripts': [
                'pterodactyl_exporter=pterodactyl_exporter:main'
            ]
        }
)
