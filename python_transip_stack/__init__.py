__version__ = '1.3.3'

import warnings

from python_transip_stack.exceptions import StackException
from python_transip_stack.http import StackHTTP
from python_transip_stack.stack import Stack

# Log deprecation warning
warnings.warn(
    'Due to the decision of TransIP to end support for free accounts '
    'the package "transip-stack-api" will no longer be maintained.',
    DeprecationWarning)
