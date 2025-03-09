from setuptools import setup

APP = ['nc_rapid.py']
OPTIONS = {
    'argv_emulation': True,
    'plist': {'Py2appCodesign': False},  # Deaktiviert Codesignierung
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
