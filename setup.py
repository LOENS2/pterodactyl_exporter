from setuptools import setup
import pterodactyl_exporter

setup(
    name='pterodactyl_exporter',
    version=pterodactyl_exporter.__version__,
    packages=['pterodactyl_exporter'],
    url='https://github.com/LOENS2/pterodactyl_exporter',
    license='MIT',
    author=pterodactyl_exporter.__version__,
    author_email='info@loens2.com',
    description='Metrics exporter for Pterodactyl',
    entry_points={
            'console_scripts': [
                'pterodactyl_exporter=pterodactyl_exporter.pterodactyl_exporter:main'
            ]
        }
)
