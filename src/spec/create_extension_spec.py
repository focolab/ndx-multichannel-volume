# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec
# TODO: import other spec classes as needed
from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec
from datetime import datetime, timedelta
import re

def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""extension to allow use of multichannel volumetric images""",
        name="""ndx-multichannel-volume""",
        version="""0.1.11""",
        author=list(map(str.strip, """Daniel Sprague""".split(','))),
        contact=list(map(str.strip, """daniel.sprague@ucsf.edu""".split(',')))
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found.
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types.
    # all types included or used by the types specified here will also be
    # included. 
    ns_builder.include_type('OpticalChannel', namespace='core')
    ns_builder.include_type('RGBImage', namespace='core')
    ns_builder.include_type('Image', namespace='core')
    ns_builder.include_type('NWBData', namespace='core')
    ns_builder.include_type('Data', namespace='hdmf-common')
    ns_builder.include_type('Device', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='core')
    ns_builder.include_type('ImageSeries', namespace='core')
    ns_builder.include_type('VectorData', namespace='core')
    ns_builder.include_type('VectorIndex', namespace='core')
    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('TimeSeries', namespace='core')
    ns_builder.include_type('Subject', namespace='core')
    ns_builder.include_type('ImagingPlane', namespace='core')
    ns_builder.include_type('PlaneSegmentation', namespace='core')
    ns_builder.include_type('LabMetaData', namespace= 'core')
    ns_builder.include_type('ImageSegmentation', namespace='core')

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information

    CElegansSubject = NWBGroupSpec(
        neurodata_type_def = 'CElegansSubject',
        neurodata_type_inc = 'Subject',
        doc = 'Subject object with support for C. Elegans specific attributes',
        datasets = [
            NWBDatasetSpec(
                name = 'growth_stage',
                dtype = 'text',
                doc = 'Growth stage of C. elegans. One of two-fold, three-fold, L1-L4, YA, OA, duaer, post-dauer L4, post-dauer YA, post-dauer OA',
   
            ),
            NWBDatasetSpec(
                name = 'cultivation_temp',
                dtype = 'float32',
                doc = 'Worm cultivation temperature in C',
                quantity = '?'
            )
        ],
        attributes = [
            NWBAttributeSpec(
                name = 'growth_stage_time',
                dtype = 'text',
                doc = 'amount of time in current growth stage in ISO 8601 duration format',
                required = False
            )
        ]
    )

    SegmentationLabels = NWBGroupSpec(
        neurodata_type_def = 'SegmentationLabels',
        neurodata_type_inc = 'NWBDataInterface',
        doc = 'Segmentation labels',
        datasets = [
            NWBDatasetSpec(
                name = 'labels',
                dtype = 'text',
                dims = ['labels'],
                shape = [None],
                doc = 'ROI labels. Should be the same length as the number of ROIs'
            ),
            NWBDatasetSpec(
                name = 'description',
                doc = 'description of what ROIs represent',
                dtype = 'text',
            ),
        ],
        links = [
            NWBLinkSpec(
                name = 'ImageSegmentation',
                target_type = 'ImageSegmentation',
                doc = 'Link to ImageSegmentation object that the labels apply to.',
                quantity = '?'
            ),
            NWBLinkSpec(
                name = 'MCVSegmentation',
                target_type = 'MultiChannelVolume',
                doc = 'Link to MultiChannelVolume holding indexed mask of ROIs.',
                quantity = '?'
            ),
            NWBLinkSpec(
                name = 'MCVSeriesSegmentation',
                target_type = 'MultiChannelVolumeSeries',
                doc = 'Link to MultiChannelVolumeSeries holding series of indexed masks of ROIs.',
                quantity = '?'
            )
        ]
    )

    MultiChannelVolumeSeries = NWBGroupSpec(
        neurodata_type_def = 'MultiChannelVolumeSeries',
        neurodata_type_inc = 'TimeSeries',
        doc = 'Image series of volumetric data with multiple channels',
        datasets = [
            NWBDatasetSpec(
                name = 'data',
                dtype = 'uint16',
                doc = 'Data representing multichannel volumetric images across frames',
                dims = [['frame','x','y','z'],['frame','x', 'y', 'z', 'channel']],
                shape = [[None, None, None, None],[None, None, None, None, None]],
            ),
            NWBDatasetSpec(
                name = 'pmt_gain',
                dtype = 'float32',
                dims = ['channels'],
                shape = [None],
                doc = 'Photomultiplier gain for each channel',
                quantity = '?'
            ),
            NWBDatasetSpec(
                name = 'exposure_time',
                dtype = 'float32',
                doc = 'Exposure time of the sample, in seconds; often the inverse of the frequency.',
                dims = ['channels'],
                shape = [None],
                quantity = '?'
            ),
            NWBDatasetSpec(
                name = 'power',
                dtype = 'float32',
                doc = 'Power of the excitation in mW, if known.',
                dims = ['channels'],
                shape = [None],
                quantity = '?'
            ),
            NWBDatasetSpec(
                name = 'intensity',
                dtype = 'float32',
                doc = 'Intensity of the excitation in mW/mm^2, if known.',
                quantity = '?'
            ),
            NWBDatasetSpec(
                name = 'dimension',
                dtype = 'int32',
                dims = ['num_dims'],
                shape = [None],
                doc = 'Number of pixels on x, y, and z axes',
            ),
            NWBDatasetSpec(
                name = 'external_file',
                dtype = 'text',
                dims = ['num_files'],
                shape = [None],
                doc = "Paths to one or more external file(s). Field is only present if format ='external'. This is only relevant if the image series is stored in the file system as one or more image file(s). This field should NOT be used if the image is stored in another NWB file and that file is linked to this file",
                quantity = '?'
            )
        ],
        attributes = [
            NWBAttributeSpec(
                name = 'scan_line_rate',
                dtype = 'float32',
                doc = 'Lines imaged per second.',
                required = False
            ),
            NWBAttributeSpec(
                name = 'binning',
                dtype = 'uint8',
                doc = 'Amount of pixels combined into bins; could be 1, 2, 4, 8, etc.',
                required = False
            ),
            NWBAttributeSpec(
                name = 'starting_frame',
                dtype = 'int32',
                dims = ['num_files'],
                shape = [None],
                doc = re.sub("[\t ]{2,}", " ","""Each external image may contain one or more consecutive frames of the full
                ImageSeries. This attribute serves as an index to indicate which frames each file
                contains, to faciliate random access. The 'starting_frame' attribute, hence,
                contains a list of frame numbers within the full ImageSeries of the first frame
                of each file listed in the parent 'external_file' dataset. Zero-based indexing is
                used (hence, the first element will always be zero). For example, if the
                'external_file' dataset has three paths to files and the first file has 5 frames,
                the second file has 10 frames, and the third file has 20 frames, then this
                attribute will have values [0, 5, 15]. If there is a single external file that
                holds all of the frames of the ImageSeries (and so there is a single element in
                the 'external_file' dataset), then this attribute should have value [0].""".replace('\n',' ')),
                required = False
            ),
            NWBAttributeSpec(
                name = 'format',
                dtype = 'text',
                default_value = 'raw',
                doc = re.sub("[\t ]{2,}", " ","""Format of image. If this is 'external', then the attribute 'external_file'
                contains the path information to the image files. If this is 'raw', then the raw
                (single-channel) binary data is stored in the 'data' dataset. If this attribute
                is not present, then the default format='raw' case is assumed.""".replace('\n',' '))
            )
        ],

        links = [
            NWBLinkSpec(
                name = 'imaging_volume',
                target_type = 'ImagingVolume',
                doc = 'Link to ImagingVolume object from which this data was generated.'
            ),
            NWBLinkSpec(
                name = 'device',
                target_type = 'Device',
                doc = 'Link to the Device object that was used to capture these images'
            )
        ]
    )

    MultiChannelVolume = NWBGroupSpec(
        neurodata_type_def='MultiChannelVolume',
        neurodata_type_inc='NWBDataInterface',
        doc='An extension of the base NWBData type to allow for multichannel volumetric images',
        datasets = [
            NWBDatasetSpec(
                name = 'description',
                doc = 'description of image',
                dtype = 'text',
            ),
            NWBDatasetSpec(
                name = 'RGBW_channels',
                doc = 'which channels in image map to RGBW',
                dtype = 'int8',
                dims = ['channels'],
                shape = [4],
                quantity = '?'
            ),
            NWBDatasetSpec(
                name = 'data',
                doc = 'Volumetric multichannel data',
                dims = ['x','y','z','channel'],
                shape = [None, None,None,None],
                dtype = 'uint16',
            )
        ],

        groups = [
                NWBGroupSpec(
                name = 'order_optical_channels',
                doc = 'Ordered list of names of the optical channels in the data',
                neurodata_type_inc = 'OpticalChannelReferences',
            )
        ],

        links = [
            NWBLinkSpec(
                name = 'imaging_volume',
                target_type = 'ImagingVolume',
                doc = 'Link to ImagingVolume object from which this data was generated.'
            )
        ]
    )

    ImagingVolume = NWBGroupSpec(
        neurodata_type_def = 'ImagingVolume',
        neurodata_type_inc = 'ImagingPlane',
        doc = 'An Imaging Volume and its Metadata',

        groups = [
            NWBGroupSpec(
                neurodata_type_inc = 'OpticalChannelPlus',
                doc = 'An optical channel used to record from an imaging volume',
                quantity = '*'
            ),
            NWBGroupSpec(
                name = 'order_optical_channels',
                doc = 'Ordered list of names of the optical channels in the data',
                neurodata_type_inc = 'OpticalChannelReferences',
            )

        ]
    )

    OpticalChannelPlus = NWBGroupSpec(
        neurodata_type_def = 'OpticalChannelPlus',
        neurodata_type_inc = 'OpticalChannel',
        doc = 'An optical channel used to record from an imaging volume. Contains both emission and excitation bands.',
        datasets = [
            NWBDatasetSpec(
                name = 'emission_range',
                dtype = 'float32',
                dims = ['start and end'],
                shape = [2],
                doc = 'boundaries of emission wavelength for channel, in nm'
            ),
            NWBDatasetSpec(
                name = 'excitation_range',
                dtype = 'float32',
                dims = ['start and end'],
                shape = [2],
                doc = 'boundaries of excitation wavelength for channel, in nm'
            ),
            NWBDatasetSpec(
                name = 'excitation_lambda',
                dtype = 'float32',
                doc = 'Excitation wavelength for channle, in nm.'
            )
        ]
    )

    OpticalChannelReferences = NWBGroupSpec(
        neurodata_type_def = 'OpticalChannelReferences',
        neurodata_type_inc = 'NWBDataInterface',
        doc = 'wrapper for optical channel references dataset',
        datasets = [
            NWBDatasetSpec(
                name = 'channels',
                dtype = 'text',
                dims = ['NumChannels'],
                shape = [None],
                doc = 'Ordered list of names of optical channels'
            )     
        ]
    )

    VolumeSegmentation = NWBGroupSpec(
        neurodata_type_def = 'VolumeSegmentation',
        neurodata_type_inc = 'PlaneSegmentation',
        doc = 'Results from image segmentation of a specific imaging volume',

        datasets= [
            NWBDatasetSpec(
                name = 'labels',
                dims = ['num_ROI'],
                shape = [None],
                dtype = 'text',
                doc = 'Ordered list of labels for ROIs',
                quantity = '?'
            ),
            NWBDatasetSpec(
                name = 'color_voxel_mask',
                neurodata_type_inc = 'VectorData',
                dtype= [
                    NWBDtypeSpec(
                        name = 'x',
                        dtype = 'uint32',
                        doc = 'Voxel x-coordinate'
                    ),
                    NWBDtypeSpec(
                        name = 'y',
                        dtype = 'uint32',
                        doc = 'Voxel y-coordinate'
                    ),
                    NWBDtypeSpec(
                        name = 'z',
                        dtype = 'uint32',
                        doc = 'Voxel z-coordinate'
                    ),
                    NWBDtypeSpec(
                        name = 'R',
                        dtype = 'uint32',
                        doc = 'Voxel red value'
                    ),
                    NWBDtypeSpec(
                        name = 'G',
                        dtype = 'uint32',
                        doc = 'Voxel green value'
                    ),
                    NWBDtypeSpec(
                        name = 'B',
                        dtype = 'uint32',
                        doc = 'Voxel blue value'
                    ),
                    NWBDtypeSpec(
                        name = 'W',
                        dtype = 'uint32',
                        doc = 'voxel white value'
                    ),
                    NWBDtypeSpec(
                        name = 'weight',
                        dtype = 'float32',
                        doc = 'Weight of the voxel'
                    )
                ],
                doc = 'Voxel masks for each ROI including RGBW color values for each pixel',
                quantity = '?'
            )
        ],
        links = [
            NWBLinkSpec(
                name = 'imaging_volume',
                target_type = 'ImagingVolume',
                doc = 'Link to ImagingVolume object from which this data was generated.'
            )
        ]
    )

    PlaneExtension = NWBGroupSpec(
        neurodata_type_def = 'PlaneExtension',
        neurodata_type_inc = 'PlaneSegmentation',
        doc = 'Results from image segmentation of a specific imaging volume'
    )

    # TODO: add all of your new data types to this list
    new_data_types = [CElegansSubject, MultiChannelVolumeSeries, MultiChannelVolume, ImagingVolume, OpticalChannelReferences, OpticalChannelPlus, VolumeSegmentation, SegmentationLabels, PlaneExtension]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)
    print('Spec files generated. Please make sure to rerun `pip install .` to load the changes.')


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
