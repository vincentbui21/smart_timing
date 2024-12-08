from setuptools import setup, Extension

module = Extension('time_module', sources = ['time_module.c'])

setup(
    name = 'TimeModule',
    version = '1.0',
    description = 'Python interface for C time-related functions',
    ext_modules = [module]
)
