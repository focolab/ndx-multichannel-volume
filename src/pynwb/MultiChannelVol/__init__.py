import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
MultiChannelVol_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-multichannel-volume.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(MultiChannelVol_specpath):
    MultiChannelVol_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-multichannel-volume.namespace.yaml'
    ))

# Load the namespace
load_namespaces(MultiChannelVol_specpath)

# TODO: import your classes here or define your class using get_class to make
# them accessible at the package level
TetrodeSeries = get_class('TetrodeSeries', 'ndx-multichannel-volume')
