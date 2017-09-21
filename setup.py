from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='tile-wells',
    url='git@github.com:joelostblom/tile-wells.git',
    author='Joel Ostblom',
    author_email='joel.ostblom@gmail.com',
    # Needed to actually package something
    packages=['tile-wells'],
    # Needed for dependencies
    install_requires=['matplotlib', 'joblib'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='''Place the well images of tiled fields in a layout similar to a multiwell
plate. This makes it easy to get an overview of the different conditions in
the plate.''',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
