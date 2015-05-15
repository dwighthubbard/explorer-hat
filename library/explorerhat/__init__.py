## @package ExplorerHAT
#  API library for Explorer HAT and Explorer HAT Pro, Raspberry Pi add-on boards
"""[explorerhat]

API library for Explorer HAT and Explorer HAT Pro, Raspberry Pi add-on boards"""

from eh_help import help
from eh_main import explorerhat_init

explorerhat_init()

from eh_main import input, output, light, analog, touch, motor, settings