from setuptools import setup, find_packages

setup(
    name='repo2txt',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'repo2txt = repo2txt.repo2txt:main',  # maps `repo2txt` command to main() in repo2txt.py
        ],
    },
    install_requires=[
        'python-docx',
    ],
)
