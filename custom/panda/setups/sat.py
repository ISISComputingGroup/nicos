#  -*- coding: utf-8 -*-

description = 'setup for sample attenuator'

includes = []

devices = dict(
    sat = device('nicos.panda.satbox.SatBox',
                  tacodevice = 'panda/modbus/sat',
                  unit = 'mm',
                  fmtstr = '%d',
                  #~ blades = [1, 2, 5, 10, 20],
                  blades = [0, 2, 5, 10, 20], # blade gets stuck until repair -> disable it here
                  slave_addr = 1, # WUT
                  addr_out = 0x1020,
                  addr_in = 0x1000,
                  ),
)

startupcode="""
printwarning('Disabling 1mm blade of sat as it gets stuck until repair....')
sat.blades[0]=0
"""

