#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2013 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

from nicos import session
from nicos.core import UsageError, LimitError, ConfigurationError, \
     ComputationError, NicosError, status
from nicos.commands.tas import qscan, qcscan, Q, calpos, pos, rp, \
     acc_bragg, ho_spurions, alu, copper, rescal, _resmat_args
from nicos.devices.tas import spacegroups


from test.utils import raises, assertAlmostEqual, ErrorLogged

def setup_module():
    session.loadSetup('scanning')
    session.setMode('master')
    sample = session.getDevice('sample')
    sample.lattice = [2.77, 2.77, 2.77]
    sample.angles = [90, 90, 90]
    sample.orient1 = [1, 0, 0]
    sample.orient2 = [0, 1, 1]

def teardown_module():
    session.unloadSetup()


def assertPos(pos1, pos2):
    for v1, v2 in zip(pos1, pos2):
        assertAlmostEqual(v1, v2, 3)

def test_mono_device():
    mono = session.getDevice('t_mono')
    mth = session.getDevice('t_mth')
    # unit switching
    mono.unit = 'A-1'
    mono.maw(1.4)
    assertAlmostEqual(mono.read(0), 1.4, 3)
    assertAlmostEqual(mono.target, 1.4, 3)
    mono.unit = 'meV'
    assertAlmostEqual(mono.read(0), 4.061, 3)
    assertAlmostEqual(mono.target, 4.061, 3)
    assert mono.status()[0] == status.OK
    mono.unit = 'A-1'
    assert mono.status()[0] == status.OK
    # mth/mtt mismatch
    mth.maw(mth()+5)
    assert mono.status(0)[0] == status.NOTREACHED

def test_tas_device():
    tas = session.getDevice('Tas')
    mono = session.getDevice('t_mono')
    ana = session.getDevice('t_ana')
    phi = session.getDevice('t_phi')
    psi = session.getDevice('t_psi')
    ki = session.getDevice('t_ki')
    kf = session.getDevice('t_kf')

    tas.scanmode = 'CKF'
    tas.scanconstant = 2.662
    mono.unit = ana.unit = 'A-1'

    # test the correct driving of motors
    tas([1, 0, 0, 1])
    assertAlmostEqual(ana(), 2.662, 3)
    assertAlmostEqual(mono(), 3.014, 3)
    assertAlmostEqual(phi(), -46.6, 1)
    assertAlmostEqual(psi(), 105.1, 1)
    assertPos(tas(), [1, 0, 0, 1])

    # cannot go to position out of scattering triangle
    assert raises(LimitError, tas, [5, 0, 0, 0])
    # cannot go to position out of scattering plane
    assert raises(LimitError, tas, [1, 2, 1, 0])
    # cannot go beyond motor limits
    old_limits = psi.userlimits
    psi.userlimits = (0, 50)
    assert raises(LimitError, tas, [1, 0, 0, 1])
    psi.userlimits = old_limits

    # test scattering sense
    tas.scatteringsense = [-1, 1, -1]
    tas([1, 0, 0, 1])
    assertAlmostEqual(phi(), 46.6, 1)  # now with "+" sign
    assert raises(ConfigurationError, setattr, tas, 'scatteringsense', [2, 0, 2])

    # test energytransferunit
    mono(1)
    ana(2)
    tas.energytransferunit = 'meV'
    assertAlmostEqual(tas()[3], -6.216, 3)
    tas.energytransferunit = 'THz'
    assertAlmostEqual(tas()[3], -1.503, 3)
    assert raises(ConfigurationError, setattr, tas, 'energytransferunit', 'A-1')

    # test scanmode
    tas.scanmode = 'CKI'
    tas.scanconstant = 2.662
    tas([1, 0, 0, 1])
    assertAlmostEqual(mono(), 2.662, 3)
    tas.scanmode = 'CKF'
    tas([1, 0, 0, 1])
    assertAlmostEqual(ana(), 2.662, 3)
    tas.scanmode = 'DIFF'
    tas.scanconstant = 2.5
    ana(2.5)
    tas([1, 0, 0, 0])
    assertAlmostEqual(ana(), 2.5, 3)
    assertAlmostEqual(mono(), 2.5, 3)
    assertPos(tas(), [1, 0, 0, 0])
    # XXX shouldn't this result in an error?
    # assert raises(tas, [1, 0, 0, 1])
    assert raises(ConfigurationError, setattr, tas, 'scanmode', 'BLAH')


    # test sub-devices and wavevector devices
    kf(2.662)
    tas([1, 0, 0, 1])
    assertAlmostEqual(ki(), 3.014, 3)
    assertAlmostEqual(kf(), 2.662, 3)
    assertAlmostEqual(tas.h(), 1, 3)
    assertAlmostEqual(tas.k(), 0, 3)
    assertAlmostEqual(tas.l(), 0, 3)
    assertAlmostEqual(tas.E(), 1, 3)
    tas.h.maw(1.5)
    assertAlmostEqual(tas.h(), 1.5, 3)

def test_Q_object():
    assert all(Q() == Q(0, 0, 0, 0))
    assert all(Q(1) == Q(1, 0, 0, 0))
    assert all(Q(1, 1) == Q(1, 1, 0, 0))
    assert all(Q(1, 1, 1) == Q(1, 1, 1, 0))
    q1 = Q(1, 2, 3, 4)
    for q2 in [
        Q(Q(1, 4, 3, 0), k=2, e=4),
        Q(1, 2, 3, e=4),
        Q(h=1, k=2, l=3, e=4),
        Q(H=1, K=2, L=3, E=4)
    ]:
        assert all(q2 == q1)
    assert raises(UsageError, Q, 1, 2, 3, 4, 5)
    assert repr(Q()) == '[ 0.  0.  0.  0.]'

def test_qscan():
    mot = session.getDevice('motor2')
    qscan((1, 0, 0), Q(0, 0, 0, 0.1), 10, mot, 'scaninfo', t=1)
    qscan((0, 0, 0), (0, 0, 0), 10, 2.5, t_kf=2.662, manual=1,
          h=1, k=1, l=1, e=0, dH=0, dk=0, dl=0, dE=.1)
    qcscan((1, 0, 0), Q(0, 0, 0, 0.1), 5, manual=[1, 2])
    qscan((1, 0, 0), Q(0, 0, 0, 0), 1)

    assert raises(UsageError, qscan, 1, 1, 1)
    assert raises(UsageError, qscan, (1, 0, 0, 0, 0), (0, 0, 0), 10)
    assert raises(UsageError, qscan, (1, 0, 0), (0, 0, 0), 10)
    assert raises(UsageError, qcscan, (1, 0, 0), (0, 0, 0), 10)

def test_tas_commands():
    tas = session.getDevice('Tas')
    tas.scanmode = 'CKI'
    tas.scanconstant = 1.57

    # calpos()/pos()
    for args in [
        (0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5, 0),
        (0.5, 0.5, 0.5, 0, 1.57),
        ((0.5, 0.5, 0.5, 0),),
        (Q(0.5, 0.5, 0.5, 0),),
        (Q(0.5, 0.5, 0.5, 0), 1.57)
    ]:
        calpos(*args)
        pos()
        assertPos(tas(), [0.5, 0.5, 0.5, 0])
        pos(*args)
        assertPos(tas(), [0.5, 0.5, 0.5, 0])

    assert session.testhandler.warns(calpos, 0.7, 0.7, 0.7, 0)
    calpos(0.5, 0.5, 0.5, 0)
    assert raises(ErrorLogged, calpos, 1, 0, 0, 1)
    pos()  # still goes to last successful calpos()
    assertPos(tas(), [0.5, 0.5, 0.5, 0])
    rp()  # just check that it works

    assert raises(ComputationError, pos, (1, 2, 3))
    assert raises(LimitError, pos, (0.7, 0.7, 0.7))

    assert raises(UsageError, calpos, 1, 0, 0, 0, 0, 0)
    assert raises(UsageError, pos, 1, 0, 0, 0, 0, 0)

def test_helper_commands():
    # just check that they are working
    acc_bragg(1, 0, 0, 0)
    ho_spurions()
    alu(phi=50)
    copper(phi=50)

def test_resolution():
    tas = session.getDevice('Tas')
    tas.collimation = '20 30 40 50'
    cell = tas._adevs['cell']
    cfg, par = _resmat_args((1,1,0,0), {})
    assert len(cfg) == 30
    assert par['qx'] == 1
    assert par['en'] == 0
    assert par['as'] == cell.lattice[0]
    assert par['alpha1'] == 20
    assert par['alpha4'] == 50
    assert par['beta1'] == 6000

    rescal()
    rescal(1, 1, 0)
    rescal(1, 1, 0, 1)

def test_getspacegroup():

    # Good cases:
    assert spacegroups.get_spacegroup(1) == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert spacegroups.get_spacegroup('Pbca') == [3, 2, 2, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    # Error cases
    assert raises(NicosError, spacegroups.get_spacegroup, 'Pbbb')
    assert raises (NicosError, spacegroups.get_spacegroup, 300)

def test_canreflect():
    # P1 all reflection types are allowed
    sg = spacegroups.get_spacegroup('P1')
    assert spacegroups.can_reflect(sg, 0, 0 , 0) == True
    assert spacegroups.can_reflect(sg, 1, 0 , 0) == True
    assert spacegroups.can_reflect(sg, 0, 1 , 0) == True
    assert spacegroups.can_reflect(sg, 0, 0 , 1) == True
    assert spacegroups.can_reflect(sg, 1, 1 , 1) == True
