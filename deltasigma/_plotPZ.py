# -*- coding: utf-8 -*-
# _plotPZ.py
# Module providing the plotPZ function
# Copyright 2013 Giuseppe Venturini

import numpy as np
import matplotlib.pyplot as plt


from ._utils import _get_zpk

def plotPZ(H, color='b', markersize=5, showlist=False):
    """Plot the poles and zeros of a transfer function.

    Parameters:
    -----------
    H : transfer function
        Any supported transfer function representation, 
        e.g., num/den, zpk, lti...

    color : matplotlib-compatible color descriptor or tuple (poles, zeros)
        For example, 'r' for red, or ('r', 'b') for poles and zeros.

    markersize : scalar
        Marker size in points.

    showlist : bool
        If True, displays a legend with pole and zero values.
    """
    
    z, p, _ = _get_zpk(H)
    p = np.real_if_close(np.round(p, 5)) # type: ignore
    z = np.real_if_close(np.round(z, 5)) # type: ignore


    pole_fmt = {'marker': 'x', 'markersize': markersize}
    zero_fmt = {'marker': 'o', 'markersize': markersize}

    if isinstance(color, (list, tuple)):
        pole_fmt['color'] = color[0]
        zero_fmt['color'] = color[1]
    else:
        pole_fmt['color'] = color
        zero_fmt['color'] = color

    plt.grid(True)

    # Plot poles
    plt.plot(p.real, p.imag, linestyle='None', **pole_fmt)

    # Plot zeros
    if len(z) > 0:
        plt.plot(z.real, z.imag, linestyle='None', **zero_fmt)

    # Plot unit circle
    circle = np.exp(2j * np.pi * np.linspace(0, 1, 100))
    plt.plot(circle.real, circle.imag) # type: ignore

    ax = plt.gca()
    ax.set_autoscale_on(False)

    if showlist:
        x1, x2, y1, y2 = ax.axis()
        x2 = np.round((x2 - x1) * 1.48 + x1, 1)
        ax.axis((x1, x2, y1, y2))

        markers = []
        descr = []

        ps = p[p.imag >= 0]
        for pi in ps:
            markers.append(plt.Line2D((), (), linestyle='None', **pole_fmt)) # type: ignore
            if np.allclose(pi.imag, 0, atol=1e-5):
                descr.append('%+.4f' % pi.real)
            else:
                descr.append('%+.4f +/- j%.4f' % (pi.real, pi.imag))

        if len(z) > 0:
            for zi in z[z.imag >= 0]:
                markers.append(plt.Line2D((), (), linestyle='None', **zero_fmt)) # type: ignore
                if np.allclose(zi.imag, 0, atol=1e-5):
                    descr.append('%+.4f' % zi.real)
                else:
                    descr.append('%+.4f +/- j%.4f' % (zi.real, zi.imag))

        plt.legend(markers, descr, title="Poles (x) and zeros (o)",
                   ncol=1, loc='best', handlelength=.55, prop={'size': 10})
    else:
        plt.xlim((-1.1, 1.1))
        plt.ylim((-1.1, 1.1))

    plt.gca().set_aspect('equal')
    plt.ylabel('Imag')
    plt.xlabel('Real')
