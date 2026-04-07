__title__ = 'Magnecomp Email Client'
__description__ = 'Send email'
__version__ = '0.0.1'
__author__ = 'Magnecomp PCL'
__author_email__ = 'contact@magnecomp.com'
__url__ = 'https://github.com/mpt-ai/mpt-email-client'
__copyright__ = 'Copyright 2022 Magnecomp PCL'
__license__ = 'MIT'

VERSION = __version__

from .sendmail import sendEmail
from . import utils