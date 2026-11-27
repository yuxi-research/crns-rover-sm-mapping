#%% This is a module to calculate the vertical weights based on the Schron et al. (2017) method.

# Reference: Schrön, M., Köhli, M., Scheiffele, L., Iwema, J., Bogena, H. R., Lv, L.,…Zacharias, S. (2017). Improving calibration and validation of cosmic-ray neutron sensors in the light of spatial sensitivity. Hydrol. Earth Syst. Sci., 21(10), 5009-5030. https://doi.org/10.5194/hess-21-5009-2017 
# Appendix A.

# Note: All theta in these functions expects in volumetric water content (m3/m3). 
# The conventional method (Franz 2012) specifies theta in volumetric water content (m3/m3).
# But Schron 2017 paper didn't specify wheather the unit of theta is in % or not.
# I compared the result of both units and found that the result of theta in m3/m3 (not in Vol%) is more reasonable and consist with Schron's Figure 1b.

# Procedure to calculate the vertical weights based on the Schron et al. (2017) method:
# 1. Air pressure factor, Fp =p0/ (p1−exp(−p/1013)) , air pressure p in mbar
# 2. Vegetation factor, Fveg(Hveg, θ) = 1−p0 (1−exp(−p1* Hveg)) * (1+exp(−p2* θ)), asuming no vegetation for the calculation, Hveg = 0.
# 3. Scaled distance, r_rescaled = calc_r_rescaled(r, p, theta, H_veg) = r/Fp/Fveg(Hveg,θ)  
# 4. Effective penetration depth, d86 = calc_d86(r_rescaled, theta, rho_bulk)
# 5. Unnormalized vertical weights, unvweights = calc_wd(d, d86)
# 6. Normalized vertical weights, vweights_norm = unvweights / sum(unvweights)

from os import name

import numpy as np

def calc_F0():
    para = [3.7]
    value = para[0]
    return value


def calc_F1(h, theta):
    para = [8735, 22.689, 11720, 0.00978, 9306, 0.003632]

    value = (
            para[0] * (1 + para[3] * h) * np.exp(-para[1] * theta)
            + para[2] * (1 + para[5] * h)
            - para[4] * theta
            )
    return value


def calc_F2(h, theta):
    para = [0.027925, 6.6577, 0.028544, 0.002455, 6.851e-5, 12.2755]

    value = (
                (para[4] * h - para[0])
                * np.exp(-para[1] * theta / (1 + para[5] * theta))
                + para[2]
            ) * (1 + para[3] * h)
    return value


def calc_F3(h, theta):
    para = [247970, 23.289, 374655, 0.00191, 258552]

    value = (
            para[0] * (1 + para[3] * h) * np.exp(-para[1] * theta)
            + para[2]
            - para[4] * theta
            )
    return value


def calc_F4(h, theta):
    para = [0.054818, 21.032, 0.6373, 0.0791, 5.425e-4]

    value = (
            para[0] * np.exp(-para[1] * theta)
            + para[2]
            - para[3] * theta
            + para[4] * h
            )
    return value

def calc_F5(h, theta):
    para = [39006, 15002330, 2009.24, 0.01181, 3.146, 16.7417, 3727]

    value = (
            (para[0] - para[1] / (para[2] * theta + h - 0.13))
            * (para[3] - theta)
            * np.exp(-para[4] * theta)
            - para[5] * h * theta
            + para[6]
            )
    return value

def calc_F6(h, theta):
    para = [6.031e-5, 98.5, 0.0013826]
    value = para[0] * (h + para[1]) + para[2] * theta
    return value


def calc_F7(h, theta):
    para = [11747, 55.033, 4521, 0.01998, 0.00604, 3347.4, 0.00475]
    value = (
        para[0]
        * (1 - para[6] * h)
        * np.exp(-para[1] * theta * (1 - para[4] * h))
        + para[2]
        - para[5] * theta
    ) * (2 + para[3] * h)

    return value


def calc_F8(h, theta):
    para = [0.01543, 13.29, 0.01807, 0.0011, 8.81e-5, 0.0405, 26.74]
    value = (
        (para[4] * h - para[0]) * np.exp(
            -para[1] * theta / (1 + para[5] * h + para[6] * theta)
        ) + para[2]
        ) * (2 + para[3] * h)
    return value

def calc_Fp(p = 1013):
    '''
    Calculate the pressure factor Fp based on the given pressure p in mbar.
    Parameters:
    p (float): The pressure value in mbar. Default is 1013 mbar.
    Returns:
    float: The calculated pressure factor Fp.
    '''

    para = [0.4922, 0.86]
    value = para[0] / (para[1] - np.exp(-p / 1013))
    return value

def calc_Fveg(theta, H_veg):
    para = [0.17, 0.41, 9.25]
    value = 1 - para[0] * (1 - np.exp(-para[1] * H_veg)) * (1 + np.exp(-para[2] * theta))
    return value


def calc_r_rescaled(r, p, theta, H_veg):
    '''
    Calculate the rescaled radius.
    Parameters:
    r (float): The radius value.
    p (float): The pressure value in mbar.
    H_veg (float): The vegetation height value in meters.
    theta (float): The soil moisture value in volumetric water content (m3/m3).
    Returns:
    float: The rescaled radius.'''
    return r / calc_Fp(p) / calc_Fveg(theta, H_veg)

def calc_d86(r_rescaled, theta, rho_bulk):
    para = [8.321, 0.14249, 0.96655, 0.01, 20.0, 0.0429]
    value = (
            para[0]
            + para[1] * (para[2] + np.exp(-para[3] * r_rescaled)) * ((para[4] + theta) / (para[5] + theta))
            ) / rho_bulk
    return value

# Conventional method
def calc_wd(d, d86):
    # Schron et al. (2017) method for calculating vertical weights based on depth and d86.
    # This is a placeholder for the actual implementation of the Schron et al. method.
    # The actual formula should be implemented here based on the reference.
    wd = np.exp(-2 * d / d86)  # Example implementation, replace with actual formula
    return wd



def do_calc_wd(d, theta, p, rho_bulk, H_veg=0):
    # COSMOS Guide: . It is recommend to set r =1 as a proxy for the average measurement depth in the footprint. 
    r_rescaled = calc_r_rescaled(r=1, p=p, theta=theta, H_veg=H_veg)
    d86 = calc_d86(r_rescaled=r_rescaled, theta=theta, rho_bulk=rho_bulk)
    wd = calc_wd(d=d, d86=d86)
    return wd


#%% This is a module to calculate the vertical weights based on the conventional method (Franz 2012), as described in the Schron et al. (2017) paper.


# Conventional method
# Reference: Franz, T. E., Zreda, M., Ferre, T., Rosolem, R., Zweck, C., Stillman, S.,…Shuttleworth, W. (2012). Measurement depth of the cosmic ray soil moisture probe affected by hydrogen from various sources. Water Resources Research, 48(8). https://doi.org/10.1029/2012WR011871 
# Procedures:
# 1. Calculate D86 using the conventional method based on the initial soil moisture (theta). calc_D86_conv(theta)
# 2. Calculate the vertical weight (wd) using the conventional method based on the initial soil moisture (theta). calc_wd_conv(d, d86)
# 3. Normalize the vertical weights by dividing by the sum of all weights. vweights_norm = vweights / sum(vweights)

def calc_D86_conv(theta):
    '''
    Calculate the D86 value using the conventional method based on the initial soil moisture (theta).
    Parameters:
    theta (float): The initial soil moisture value in volumetric water content (m3/m3).
    Returns:
    float: The calculated D86 value in centimeters.
    '''
    return 5.8 / (theta + 0.0829)

assert abs(calc_D86_conv(0.4) - 12) < 1
assert abs(calc_D86_conv(0) - 70) < 1

def calc_wd_conv(d, d86):
    '''
    Calculate the vertical weight (wd) using the conventional method based on the initial soil moisture (theta).
    Note the weights are not normalized.
    Parameters:
    d86 (float): The D86 value in centimeters.
    Returns:
    float: The calculated vertical weight (wd) at the given depth (d) in centimeters.
    '''
    wd = 1 - d/d86 if d < d86 else 0
    return wd

def do_calc_wd_conv(d, theta):
    '''
    Calculate the vertical weight (wd) using the conventional method based on the initial soil moisture (theta).
    Note the weights are not normalized.
    Parameters:
    theta (float): The initial soil moisture value in volumetric water content (m3/m3).
    d (float): The depth value in centimeters.
    Returns:
    float: The calculated vertical weight (wd) at the given depth (d) in centimeters.
    '''
    d86 = calc_D86_conv(theta)
    wd = calc_wd_conv(d, d86)
    return wd


#%% Test

# %%
def test_calc_wd():
    import matplotlib.pyplot as plt

    test_theta = 0.12
    test_pressure = 1013
    test_bd = 1.4
    test_h_veg = 0
    r = 0

    test_ds = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])

    weights = [do_calc_wd(d=d, theta=test_theta, p=test_pressure, rho_bulk=test_bd, H_veg=test_h_veg) for d in test_ds]
    weights_norm = weights / np.sum(weights)

    weights_conv = [do_calc_wd_conv(d, test_theta) for d in test_ds]
    weights_conv_norm = weights_conv / np.sum(weights_conv)

    plt.plot(test_ds, weights, color='blue', label='Schron2017 Method')
    plt.plot(test_ds, weights_conv, color='orange', label='Conventional Method')
    plt.legend()


if __name__ == '__main__':
    test_calc_wd()