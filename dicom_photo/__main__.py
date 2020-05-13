"""

"""

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import dicom_photo.defaults as defaults
import dicom_photo.m_orthodontic_photograph
import dicom_photo.controller
import sys, os

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None):
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_version = "v%s" % defaults.VERSION
    program_version_message = '%%(prog)s %s' % (program_version)
    program_license = '''{short_description}

  Created by Toni Magni on {creation_date}.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
'''.format(
    short_description=defaults.__short_description__,
    creation_date=defaults.__creation_date__)

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", 
                            dest="verbose", 
                            action="store_true", 
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', 
                            action='version', 
                            version=program_version_message)
#         parser.add_argument("-u", "--username",
#                             dest="username",  
#                             help="specify the tops staff's username (eg.: msanchez)",
#                             metavar="<username>")
        parser.add_argument("-o", "--output-filename",
                            dest="output_filename",  
                            help="Where to store the DICOM file. ",
                            metavar='<filename>')
#         parser.add_argument("--tempserver", 
#                             dest="tempserver", 
#                             action="store_true",
#                             default=None,
#                             help="destination server is a temp server [default: %(default)s]")
        parser.add_argument(dest="input_filename", 
                            help="path of file to convert to DICOM",
                            metavar='<filename>')


        # Process arguments
        args = parser.parse_args()

        c = dicom_photo.controller.SimpleController(args)
        c.convert_image_to_dicom_photograph

        dicom_photograph = dicom_photo.m_orthodontic_photograph.PhotographBase()
        dicom_photograph.set_image(args.input_filename)
        dicom_photograph.set_dataset(filename=args.output_filename)

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        exit(120)
        return 0

if __name__ == "__main__":
    exit(main())