import numpy as np
import math

import Globals
import helpers


def snc(z):
    az = math.fabs(z)
    if az < 1e-4:
        return {
            "S": (1 - z * (0.05 - z / 840) / 6),
            "C": 0.5 - z * (1 - z / 30) / 25
        }
    else:
        saz = math.sqrt(az)
        if z > 0:
            x = helpers.rad_to_deg(saz)
            return {
                "S": (saz - math.sin(x)) / (saz * az),
                "C": (1 - math.cos(x)) / az
            }
        else:
            x = math.e**saz
            return {
                "S": (0.5 * (x - 1 / x) - saz) / (saz * az),
                "C": (0.5 * (x + 1 / x) - 1) / az
            }


def cse(r0, v0, dt, mu=Globals.mu, x0=0, tol=5e-9):
    rscale = np.linalg.norm(r0)
    vscale = math.sqrt(mu / rscale)
    r0s = r0 / rscale
    v0s = v0 / vscale
    dts = dt * vscale / rscale
    v2s = np.linalg.norm(v0)**2 * rscale / mu
    alpha = 2 - v2s
    armd1 = v2s - 1
    rvr0s = np.dot(r0, v0) / math.sqrt(mu * rscale)
    x = x0
    if x0 == 0:
        x = dts * math.fabs(alpha)
    ratio = 1
    x2 = x**2
    z = alpha * x2
    scz = snc(z)
    x2cz = x2 * scz["C"]
    f = 0
    df = 0

    while math.fabs(ratio) >= tol:
        f = x + rvr0s * x2cz + armd1 * x * x2 * scz["S"] - dts
        df = x * rvr0s * (1 - z * scz["S"]) + armd1 * x2cz + 1
        ratio = f / df
        x -= ratio
        x2 = x**2
        z = alpha * x2
        scz = snc(z)
        x2cz = x2 * scz["C"]

    lf = 1 - x2cz
    lg = dts - x2 * x * scz["S"]

    r1 = lf * r0s + lg * v0s
    ir1 = 1 / np.linalg.norm(r1)
    lfdot = ir1 * x * (z * scz["S"] - 1)
    lgdot = 1 - x2cz * ir1
    v1 = lfdot * r0s + lgdot * v0s

    return r1*rscale, v1*vscale, x
