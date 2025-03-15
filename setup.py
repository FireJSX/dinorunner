from setuptools import setup, find_packages

setup(
    name="dinorunner",            # Name des Packages
    version="0.1",                # Version des Packages
    packages=find_packages(),     # Findet alle Unterpakete und Module
    install_requires=[            # Abhängigkeiten
        # Beispiel: 'numpy',
    ],
    package_data={                # Ressourcen, die mit dem Package verteilt werden sollen
        'dinorunner': [
            'resources/assets/*',  # Alle Dateien im 'assets' Ordner
            'resources/sound/*',   # Alle Dateien im 'sound' Ordner
            'resources/graphics/*' # Alle Dateien im 'graphics' Ordner
        ],
    },
    include_package_data=True,     # Stellt sicher, dass die package_data im Distribution-Paket enthalten ist
    test_suite='tests',            # Testverzeichnis
)
