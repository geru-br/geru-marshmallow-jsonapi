from setuptools import setup

requires = [
    'marshmallow>=2.19',
]

extras_require = {
    'test': [
        'pytest==4.4.1',
        'mock==2.0.0',
        'mockredispy==2.9.3',
    ],
    'ci': [
        'python-coveralls==2.9.1',
    ]
}

with open('README.md') as f:
    long_description = f.read()

setup(
    name='geru.marshmallow_jsonapi',
    version='0.1.2',
    description='Marshmallow JsonAPI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    author='Marcelo Moraes',
    author_email='marcelo.moraes@geru.com.br',
    keywords=["Marshmallow JsonAPI", "JsonAPI", "Cornice JsonAPI"],
    include_package_data=True,
    zip_safe=False,
    extras_require=extras_require,
    install_requires=requires,
    packages=['geru.marshmallow_jsonapi']
)
