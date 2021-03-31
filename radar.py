import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


class RadarAxes(PolarAxes):

    name = 'radar'

    def __init__(self, figure=None, rect=None, spoke_count=0, radar_patch_type="polygon", radar_spine_type="circle", *args, **kwargs):
        resolution = kwargs.pop("resolution", 1)
        self.spoke_count = spoke_count
        self.radar_patch_type = radar_patch_type
        self.radar_spine_type = radar_spine_type
        if figure == None:
            figure = plt.gcf()
        if rect == None:            
            rect = figure.bbox_inches
        self.radar_theta = (
            1.75 * np.pi *
            np.linspace(0, 1 - 1.0 / self.spoke_count, self.spoke_count))
        self.radar_theta += np.pi / 2

        super(RadarAxes, self).__init__(figure, rect, *args, **kwargs)

    def draw_patch(self):
        if self.radar_patch_type == "polygon":
            return self.draw_poly_patch()
        elif self.radar_patch_type == "circle":
            return draw_circle_patch()

    def draw_poly_patch(self):
        verts = unit_poly_verts(self.radar_theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def fill(self, *args, **kwargs):
        closed = kwargs.pop('closed', True)
        return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

    def plot(self, *args, **kwargs):
        lines = super(RadarAxes, self).plot(*args, **kwargs)
        for line in lines:
            self._close_line(line)

    def _close_line(self, line):
        x, y = line.get_data()
        if x[0] != x[-1]:
            x = np.concatenate((x, [x[0]]))
            y = np.concatenate((y, [y[0]]))
            line.set_data(x, y)

    def set_varlabels(self, labels):
        self.set_thetagrids(self.radar_theta * 180 / np.pi, labels)

    def _gen_axes_patch(self):
        return self.draw_patch()

    def _gen_axes_spines(self):
        if self.radar_patch_type == 'circle':
            return PolarAxes._gen_axes_spines(self)
        spine_type = 'circle'
        verts = unit_poly_verts(self.radar_theta)
        verts.append(verts[0])
        path = Path(verts)
        spine = Spine(self, self.radar_spine_type, path)
        spine.set_transform(self.transAxes)
        return {'polar': spine}

    def _as_mpl_axes(self):
        return RadarAxes, {"spoke_count": self.spoke_count,
                           "radar_patch_type": self.radar_patch_type,
                           "radar_spine_type": self.radar_spine_type}


def draw_circle_patch(self):
    return plt.Circle((0.5, 0.5), 0.5)


def unit_poly_verts(theta):
    x0, y0, r = [0.5] * 3
    verts = [(r * np.cos(t) + x0, r * np.sin(t) + y0) for t in theta]
    return verts


