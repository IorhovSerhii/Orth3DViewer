"""
A.32.4 VL Photographic Image IOD 

"""
import os
import tempfile
import datetime

import pydicom
import pynetdicom
from pydicom.dataset import Dataset, FileDataset
import pydicom.sequence
import PIL
import dicom_photo.m_dicom_base

class PhotographBase(dicom_photo.m_dicom_base.DicomBase):

    def __init__(self):
        super().__init__()
        self.set_file_meta()


    def set_dataset(self,filename):
        super().set_dataset(filename)
        self.ds.Modality = 'XC'

    def set_image_type(self):
        """
        Define if this is a scanned image, or an original capture.
        C.8.12.1.1.6 Image Type
            The Image Type Attribute identifies important image characteristics in a multiple valued Data Element. For Visible Light, Image Type is specialized as follows:

            Value 1 shall identify the Pixel Data Characteristics in accordance with Section C.7.6.1.1.2.

                Enumerated Values:

                ORIGINAL

                DERIVED

            Value 2 shall identify the Patient Examination Characteristics in accordance with Section C.7.6.1.1.2.

                Enumerated Values:

                PRIMARY

                SECONDARY

            Value 3 may be absent, but if present shall identify the members of a stereo pair, in which case Referenced Image Sequence (0008,1140) is used to identify the other member of the pair.

                Enumerated Values:

                STEREO L
                Image is the left image (relative to the observer's left) of a stereo pair acquisition

                STEREO R
                Image is the right image (relative to the observer's right) of a stereo pair acquisition

            Other Values are implementation specific (optional).
        """
        self.ds.ImageType = ['ORIGINAL','PRIMARY']

    def is_digitized_image(self):
        """
        A digitized image is considered as secondary capture for DICOM. As an example, if the original photograph was taken with an analog camera, and the negative, positive or print was then scanned, the scanned image should be recorded in DICOM as secondary, and this method should be used.
        See C.7.6.1.1.2 Image Type
        """
        self.ds.ImageType[1] = 'SECONDARY'

    def is_primary_image(self):
        """
        A primary image is one that was generated by the device that was used to capture the original photograph from the patient. As an example, if the original photograph was taken with a digital camera, that image should be recorded in DICOM using this method.
        See C.7.6.1.1.2 Image Type
        """
        self.ds.ImageType[1] = 'PRIMARY'

    def is_original_image(self):
        self.ds.ImageType[0] = 'ORIGINAL'

    def is_derived_image(self):
        """
        A derived image is a manipulated image. It's not the original anymore, it's been most likely enhanced with some calculation or filters.
        """
        self.ds.ImageType[0] = 'DERIVED'

    def set_image(self,image_path):
        self.set_dataset('file1.dcm')

        with PIL.Image.open(image_path) as im:

            # Note

            self.ds.Rows = im.size[0]
            self.ds.Columns = im.size[1]

            if im.mode == '1': # (1-bit pixels, black and white, stored with one pixel per byte)
                self.ds.SamplesPerPixel = 1
                try:
                    del self.ds.PlanarConfiguration
                except AttributeError:
                    pass
                self.ds.BitsStored = 1
                self.ds.HighBit = 0
                self.ds.PhotometricInterpretation = 'MONOCHROME2'
            elif im.mode == 'L': # (8-bit pixels, black and white)
                self.ds.SamplesPerPixel = 1
                try:
                    del self.ds.PlanarConfiguration
                except AttributeError:
                    pass
                self.ds.BitsAllocated = 8
                self.ds.BitsStored = 8
                self.ds.HighBit = 7
                self.ds.PhotometricInterpretation = 'MONOCHROME2'
            elif im.mode == 'P': # (8-bit pixels, mapped to any other mode using a color palette)
                print("ERROR: mode [{}] is not yet implemented.".format(im.mode))
                raise NotImplementedError

                # self.ds.SamplesPerPixel = 1
                # self.ds.BitsAllocated = 8
                # self.ds.BitsStored = 8
                # self.ds.HighBit = 7
                # self.ds.PhotometricInterpretation = 'PALETTE COLOR'
            elif im.mode == 'RGB': # (3x8-bit pixels, true color)
                self.ds.SamplesPerPixel = 3
                # Planar Configuration (0028,0006) is not meaningful when a compression Transfer Syntax is used that involves reorganization of sample components in the compressed bit stream. In such cases, since the Attribute is required to be present, then an appropriate value to use may be specified in the description of the Transfer Syntax in PS3.5, though in all likelihood the value of the Attribute will be ignored by the receiving implementation.
                self.ds.PlanarConfiguration = 0
                self.ds.BitsAllocated = 8
                self.ds.BitsStored = 8
                self.ds.HighBit = 7
                self.ds.PhotometricInterpretation = 'RGB'
            elif im.mode == 'RGBA': # (4x8-bit pixels, true color with transparency mask)
                print("ERROR: mode [{}] is not yet implemented.".format(im.mode))
                raise NotImplementedError
                # self.ds.SamplesPerPixel = 4
                # self.ds.PlanarConfiguration = 0
                # self.ds.BitsAllocated = 8
                # self.ds.BitsStored = 8
                # self.ds.HighBit = 7
                # self.ds.PhotometricInterpretation = 'ARGB'
            elif im.mode == 'CMYK': #  (4x8-bit pixels, color separation)
                print("ERROR: mode [{}] is not yet implemented.".format(im.mode))
                raise NotImplementedError
                # self.ds.SamplesPerPixel = 4
                # self.ds.PlanarConfiguration = 0
                # self.ds.BitsAllocated = 8
                # self.ds.BitsStored = 8
                # self.ds.HighBit = 7
                # self.ds.PhotometricInterpretation = 'CMYK'
            elif im.mode == 'YCbCr': # (3x8-bit pixels, color video format) Note that this refers to the JPEG, and not the ITU-R BT.2020, standard
                print("ERROR: mode [{}] is not yet implemented.".format(im.mode))
                raise NotImplementedError
                # self.ds.SamplesPerPixel = 3
                # self.ds.PlanarConfiguration = 0
                # self.ds.BitsAllocated = 8
                # self.ds.BitsStored = 8
                # self.ds.HighBit = 7
                # self.ds.PhotometricInterpretation = 'YBR_FULL'
            elif im.mode == 'LAB': # (3x8-bit pixels, the L*a*b color space)
                print("ERROR: mode [{}] is not yet implemented.".format(im.mode))
                raise NotImplementedError
            elif im.mode == 'HSV': # (3x8-bit pixels, Hue, Saturation, Value color space)
                print("ERROR: mode [{}] is not yet implemented.".format(im.mode))
                raise NotImplementedError
            elif im.mode == 'I': # (32-bit signed integer pixels)
                print("ERROR: mode [{}] is not yet implemented.".format(im.mode))
                raise NotImplementedError
            elif im.mode == 'F': # (32-bit floating point pixels)
                print("ERROR: mode [{}] is not yet implemented.".format(im.mode))
                raise NotImplementedError

            px = im.load()
            self.ds.PixelRepresentation = 0x0
            # Image Pixel M
            # Pixel Data (7FE0,0010) for this image. The order of pixels encoded for each image plane is left to right, top to bottom, i.e., the upper left pixel (labeled 1,1) is encoded first followed by the remainder of row 1, followed by the first pixel of row 2 (labeled 2,1) then the remainder of row 2 and so on.
            # It's Planar Configuration which defines how the values are stored in the PixelData, which is defined to be 0, in this case.
            # C.7.6.3.1.3 Planar Configuration
            # Planar Configuration (0028,0006) indicates whether the color pixel data are encoded color-by-plane or color-by-pixel. This Attribute shall be present if Samples per Pixel (0028,0002) has a value greater than 1. It shall not be present otherwise.

            # Enumerated Values:

            # 0
            # The sample values for the first pixel are followed by the sample values for the second pixel, etc. For RGB images, this means the order of the pixel values encoded shall be R1, G1, B1, R2, G2, B2, …, etc.
            self.ds.PixelData = b''
            if self.ds.SamplesPerPixel == 1:
                for row in range(self.ds.Rows):
                    for column in range(self.ds.Columns):
                        self.ds.PixelData += bytes([px[row,column]])
            elif self.ds.SamplesPerPixel > 1:
                for row in range(self.ds.Rows):
                    for column in range(self.ds.Columns):
                        for sample in range(self.ds.SamplesPerPixel):
                            self.ds.PixelData += bytes([px[row,column][sample]])
            else:
                print("Error: Incorrect value for SamplesPerPixel {}".format(self.ds.SamplesPerPixel))


"""
    # General Image Module M
    ds.InstanceNumber = '1'
    ds.PatientOrientation = ''


    # Laterality (0020,0060) is a Series level Attribute and must be the same for
    # all Images in the Series, hence it must be absent if Image Laterality (0020,0062) 
    # has different values for Images in the same Series.
    # In the case of orthodontic photographic session, we need to identify if we 
    # should store one image per series, and entire set in the same study, 
    # or entire set in the same series.
    ds.ImageLaterality = ''



    # Note
    # Planar Configuration (0028,0006) is not meaningful when a compression Transfer Syntax is used that involves reorganization of sample components in the compressed bit stream. In such cases, since the Attribute is required to be present, then an appropriate value to use may be specified in the description of the Transfer Syntax in PS3.5, though in all likelihood the value of the Attribute will be ignored by the receiving implementation.
    ds.PlanarConfiguration = 0



    # Acquistion Context M
    ds.AcquisitionContextSequence = pydicom.sequence.Sequence([])
    ds.AnatomicRegionSequence = pydicom.sequence.Sequence([])

    # VL Image M
    ds.LossyImageCompression = '00'

    # SOP Common M
    ds.SOPClassUID = SOPClassUID
    ds.SOPInstanceUID = SOPInstanceUID

def dciodvfy(filename):
    print('\nValidating file {}'.format(filename))
    dicom3tools_path = '/Users/cdstaff/dev/open-ortho/dicom-photography/resources/dicom3tools_macexe_1.00.snapshot.20191225051647'
    os.system('{} {}'.format(
        os.path.join(dicom3tools_path,'dciodvfy'),
        filename))




# reopen the data just for checking
# for filename in (filename_little_endian):
print('Load file {} ...'.format(filename))
ds = pydicom.dcmread(filename)
print(ds)
dciodvfy(filename)

# remove the created file
print('Remove file {} ...'.format(filename))
os.remove(filename)
"""