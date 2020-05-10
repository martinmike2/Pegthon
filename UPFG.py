import CSE
import Globals
import numpy as np

import Vehicle
import helpers
from Guidance import Guidance


class UPFG:
    def __init__(self):
        pass

    def iterate(self, vehicle, target, state, previous):
        gamma = target.angle
        iy = target.normal
        rdval = target.radius
        vdval = target.velocity
        t = state.time
        m = state.mass
        r = state.radius
        v = state.velocity
        cser = previous.cser
        rbias = previous.rbias
        rd = previous.rd
        rgrav = previous.rgrav
        tp = previous.time
        vprev = previous.velocity
        vgo = previous.vgo

        sm = []
        al = []
        md = []
        ve = []
        ft = []
        at = []
        tu = []
        tb = []

        for stage in vehicle.stages:
            sm.append(stage.mode)
            al.append(stage.gLim * Globals.g0)
            pack = stage.get_thrust()
            ft.append(pack[0])
            md.append(pack[1])
            ve.append(pack[2] * Globals.g0)
            at.append(ft[len(ft) - 1] / stage.massTotal)
            tu.append(ve[len(ve) - 1] / at[len(at) - 1])
            tb.append(stage.maxT)

        dt = t - tp
        dvsensed = v - vprev
        vgo = vgo - dvsensed
        tb[0] = tb[0] - previous.tb

        if sm[0] == 1:
            at[0] = ft[0] / m
        elif sm[0] == 2:
            at[0] = al[0]

        tu[0] = ve[0] / at[0]
        l = 0
        li = []

        i = 0
        n = len(vehicle.stages) - 1
        while i < n:

            if sm[i] == 1:
                li.append(ve[i] * np.log(tu[i] / (tu[i] + tb[i])))
            elif sm[i] == 2:
                li.append(al[i] * tb[i])
            else:
                li.append(0)

            l += li[i]

            if l > np.linalg.norm(vgo):
                v1 = vehicle
                v1.stages.pop()
                i += 1
                return self.iterate(v1, target, state, previous)

            i += 1

        li.append(np.linalg.norm(vgo) - l)
        tgoi = []
        n = len(vehicle.stages)
        i = 0

        while i < n:
            if sm[i] == 1:
                tb[i] *= 1 - np.e**(-li[i] / ve[i])
            elif sm[i] == 2:
                tb[i] = li[i] / al[i]

            if i == 0:
                tgoi.append(tb[i])
            else:
                tgoi.append(tgoi[i - 1] + tb[i])
            i += 1

        l1 = li[0]
        tgo = tgoi[n-1]

        l = 0
        j = 0
        s = 0
        q = 0
        h = 0
        p = 0
        ji = []
        si = []
        qi = []
        pi = []
        tgoi1 = 0

        i = 0
        while i < n:
            if i > 0:
                tgoi1 = tgoi[i - 1]

            if sm[i]:
                ji.append(tu[i] * li[i] - ve[i] * tb[i])
                si.append(-ji[i] + tb[i] * li[i])
                qi.append(si[i] * (tu[i] + tgoi1) - 0.5 * 0.5 * ve[i] * tb[i]**2)
                pi.append(qi[i] * (tu[i] + tgoi) - 0.5 * ve[i] * tb[i]**2 * (tb[i] / 3 + tgoi1))
            elif sm[i] == 2:
                ji.append(0.5 * li[i] * tb[i])
                si.append(ji[i])
                qi.append(si[i] * (tb[i] / 3 + tgoi1))
                pi.append((1/6) * si[i] * (tgoi[i]**2 + 2 * tgoi[i] * tgoi1 + 3 * tgoi1**2))

            ji[i] += li[i] * tgoi1
            si[i] += l * tb[i]
            qi[i] += j * tb[i]
            pi[i] += h * tb[i]

            l += li[i]
            j += ji[i]
            s += si[i]
            q += qi[i]
            p += pi[i]
            h = j * tgoi[i] - q

            i += 1

        lbda = helpers.unit_vector(vgo)
        if previous.tgo > 0:
            rgrav = (tgo / previous.tgo)**2 * rgrav

        rgo = rd - (r + v * tgo + rgrav)
        iz = helpers.unit_vector(np.cross(rd, iy))
        rgoxy = rgo - np.dot(iz, rgo) * iz
        rgoz = (s - np.dot(lbda, rgoxy)) / np.dot(lbda, iz)
        rgo = rgoxy + rgoz * iz + rbias
        lambdade = q - s * j / l
        lambdadot = (rgo - s * lbda) / lambdade
        if_ = lbda - lambdadot * j / l
        if_ = helpers.unit_vector(if_)
        phi = helpers.angle(if_, lbda) * Globals.rad_to_degree
        phidot = -phi * l / j
        vthrust = (l - 0.5 * l * phi**2 - j * phi * phidot - 0.5 * h * phidot**2) * lbda
        rthrust = s - 0.5 * s * phi**2 - q * phi * phidot - 0.5 * p * phidot**2
        rthrust *= lbda - (s * phi + q * phidot) * helpers.unit_vector(lambdadot)
        vbias = vgo - vthrust
        rbias = rgo - rthrust

        _up = helpers.unit_vector(r)
        _east = helpers.unit_vector(np.cross(np.array([0, 0, 1]), _up))
        pitch = helpers.angle(if_, _up)
        inplane = helpers.project(_up, if_)
        yaw = helpers.angle(inplane, _east)
        tangent = np.cross(_up, _east)

        if np.dot(inplane, tangent) < 0:
            yaw = -yaw

        rc1 = r - 0.1 * rthrust - (tgo / 30) * vthrust
        vc1 = v + 1.2 * rthrust / tgo - 0.1 * vthrust
        pack = CSE.cse(rc1, vc1, tgo)
        cser = pack[2]
        rgrav = pack[0] - rc1 - vc1 * tgo
        vgrav = pack[1] - vc1

        rp = r + v * tgo + rgrav + rthrust
        rp -= np.dot(rp, iy) * iy
        rd = rdval * helpers.unit_vector(rp)
        ix = helpers.unit_vector(rd)
        iz = np.cross(ix, iy)

        vv1 = np.array([ix[0], iy[0], iz[0]])
        vv2 = np.array([ix[1], iy[1], iz[1]])
        vv3 = np.array([ix[2], iy[2], iz[2]])
        vop = np.array([
            np.sin(gamma),
            0,
            np.cos(gamma)
        ])
        vd = np.array([
            np.dot(vv1, vop),
            np.dot(vv2, vop),
            np.dot(vv3, vop)
        ]) * vdval
        vgo = vd - v - vgrav + vbias

        current = Vehicle.State(
            time=t,
            cser=cser,
            rbias=rbias,
            rd=rd,
            rgrav=rgrav,
            tb=previous.tb + dt,
            tgo=tgo,
            velocity=v,
            vgo=vgo,
            mass=None,
            radius=None
        )

        guidance = Guidance(if_, pitch, yaw, 0, 0, tgo)

        return current, guidance, dt