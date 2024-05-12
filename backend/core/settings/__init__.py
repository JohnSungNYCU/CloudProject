# -*- coding: utf-8 -*-
# author: itimor

import platform
from .base import *

os_type = platform.system()

if os_type == 'Windows':
    print('進入 dev ')
    from .dev import *
elif os_type == 'Linux':
    print('進入 prod ')
    from .prod import *
else:
    print('進入 mac')
    from .mac import *
