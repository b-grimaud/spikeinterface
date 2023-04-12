import numpy as np

try:
    import numba
    from spikeinterface.sortingcomponents.clustering.isocut5 import isocut5

    HAVE_NUMBA = True
except ImportError:
    HAVE_NUMBA = False


def test_isocut5():
    print("hi", HAVE_NUMBA)
    if not HAVE_NUMBA:
        return

    # test cases generated by calling the matlab implementation
    dipscore, cutpoint = isocut5(np.array([0, 1, 1, 2]))
    assert dipscore == 0
    assert cutpoint == 1.5

    z = np.array(
        [
            0.3012,
            0.4709,
            0.2305,
            0.8443,
            0.1948,
            0.2259,
            0.1707,
            0.2277,
            0.4357,
            0.3111,
        ]
    )
    dipscore, cutpoint = isocut5(z)
    assert dipscore == 0
    assert np.abs(cutpoint - 0.2685) < 0.001

    t = np.array(
        [
            5.32339539, 3.72514244, 6.06074439, 4.72039874, 5.28503105, 5.43523798,
            3.52389432, 4.90105762, 6.04214636, 5.22912762, 5.62638777, 4.37264862,
            5.35692268, 5.85697279, 5.90419288, 3.42153125, 4.83902449, 3.86442812,
            4.3487476, 5.02337161, 6.43031621, 5.20781653, 6.50916649, 3.49466062,
            6.10005906, 4.97149243, -6.68120837, -3.77983954, -4.48224226, -4.43533774,
            -5.28264468, -5.10141726, -4.72195037, -4.30517775, -3.61894388, -3.22391089,
            -4.93935508, -4.13938463, -5.71609654, -4.03895828, -4.86202822, -4.03284017,
            -6.78072313, -5.55439593, -4.5964243, -6.23230336, -5.28762918, -6.78708774,
            -4.2274206, -5.20307468, -6.86372755, -6.67979293,
        ]
    )
    dipscore, cutpoint = isocut5(t)
    assert np.abs(dipscore - 1.4456) < 0.001
    assert np.abs(cutpoint - 0.9920) < 0.001


if __name__ == "__main__":
    test_isocut5()