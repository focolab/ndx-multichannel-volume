import os
from pynwb import load_namespaces, get_class
from pynwb.file import MultiContainerInterface, NWBContainer
import skimage.io as skio
from collections.abc import Iterable
import numpy as np
from pynwb import register_class
from hdmf.utils import docval, get_docval, popargs, getargs
from pynwb.ophys import ImageSeries 
from pynwb.core import NWBDataInterface, NWBData
from hdmf.common import DynamicTable
from hdmf.utils import docval, popargs, get_docval, get_data_shape, popargs_to_dict
from pynwb.file import Device
import pandas as pd
import numpy as np
from pynwb import NWBFile, TimeSeries, NWBHDF5IO
from pynwb.epoch import TimeIntervals
from pynwb.file import Subject
from pynwb.behavior import SpatialSeries, Position
from pynwb.image import ImageSeries
from pynwb.ophys import OnePhotonSeries, OpticalChannel, ImageSegmentation, Fluorescence, CorrectedImageStack, MotionCorrection, RoiResponseSeries, PlaneSegmentation, ImagingPlane
from datetime import datetime
from dateutil import tz
import pandas as pd
import scipy.io as sio
from datetime import datetime, timedelta
import warnings

from nwbinspector.register_checks import available_checks, register_check, Importance, InspectorMessage

@register_check(importance=Importance.CRITICAL, neurodata_type=NWBFile)
def check_has_neuroPAL(nwbfile: NWBFile):

    try: 
        NPimage = NWBFile.acquisition['NeuroPALImageRaw']
        return InspectorMessage(
            message=(
                f"NeuroPALImageRaw object found"
            )
        )

    except:
        return InspectorMessage(
            message=(
                f"No NeurPALImageRaw object in file. Please add"
            )
        )
    
@register_check(importance=Importance.CRITICAL, neurodata_type=NWBFile)
def test_check(nwbfile: NWBFile):

    return InspectorMessage(
        message=(
            f"Check triggered"
        )
    )