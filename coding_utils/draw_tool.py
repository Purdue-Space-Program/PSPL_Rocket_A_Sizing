import pyqtgraph.examples

import numpy as np
import pyqtgraph as pg

# this shits impossible
# def ReorderPointsClockwise(points_list):
#     # there's multiple ways to draw points in a continuous line in a clockwise order so ill make some assumptions that should work for our cases:
#     # 1. the first point is the leftmost one (most bottom one if there's a tie) (not really an assumption but helps to specify)
#     # 2. the next point is the first one to the right of the last point (most bottom one if there's a tie)
#     # 3. once there are not points
#     undrawn_points = points_list
#     drawn_points = []


def DrawEngine(chamber_radius, chamber_length, converging_length, throat_radius, throat_length, diverging_radius, diverging_length):
    engine_points = EngineDimensionsToPoints(chamber_radius, chamber_length, converging_length, throat_radius, throat_length, diverging_radius, diverging_length)
    DrawPoints(engine_points)

def EngineDimensionsToPoints(chamber_radius, chamber_length,converging_length, throat_radius, throat_length, diverging_radius, diverging_length):
    engine_points = [
                        (0                                                              , -chamber_radius ),
                        (chamber_length                                                 , -chamber_radius ),
                        (chamber_length+converging_length                               , -throat_radius   ),
                        (chamber_length+converging_length+throat_length                 , -throat_radius   ),
                        (chamber_length+converging_length+throat_length+diverging_length, -diverging_radius),
                    ]
    # mirror the first points across the x-axis
    # holy fuck i need to find a better way to do this
    engine_points = [*engine_points, *([(engine_point[0],engine_point[1]*(-1)) for engine_point in [engine_points[len(engine_points) - i - 1] for i in range(len(engine_points))]])]

    return(engine_points)

def DrawPoints(points_list):
    # assume points are given in clockwise order
    points_list = np.array(points_list)

    points_positions = np.array(points_list)
    lines_end_points = np.array([[n, (n + 1 ) % len(points_list)] for n in range(len(points_list))]) # creates a list like [0,1], [1,2], [2,3], [3,4] for each point
    # (n + 1 ) % len(points_list) lets the final set of end points wrap back around to the first point
    symbols = np.array(('o',) * len(points_list))

    line_style = np.array([(255, 255, 255, 255, 10)] * len(points_list),
                          dtype = [
                                    ('red',   np.ubyte),
                                    ('green', np.ubyte),
                                    ('blue',  np.ubyte),
                                    ('alpha', np.ubyte),
                                    ('width', float)
                                  ]
                         )

    symbol_fill_color = np.array([(0, 0, 255)] * len(points_list),
                          dtype = [
                                    ('red',   np.ubyte),
                                    ('green', np.ubyte),
                                    ('blue',  np.ubyte),
                                  ]
                         )

    symbol_outline_color = symbol_fill_color # np.array([(0, 0, 255)] * len(points_list),
                        #   dtype = [
                        #             ('red',   np.ubyte),
                        #             ('green', np.ubyte),
                        #             ('blue',  np.ubyte),
                        #           ]
                        #  )


    # drawing shit
    pg.setConfigOptions(antialias=True) # Enable antialiasing for prettier plots

    window = pg.GraphicsLayoutWidget(show=True)
    window.setWindowTitle('pyqtgraph GraphItem')
    v = window.addViewBox()
    v.setAspectLocked()

    g = pg.GraphItem()


    v.addItem(g)

    #Update the graph
    g.setData(pos=points_positions, adj=lines_end_points, pen=line_style, size=0.3, symbol=symbols, pxMode=False, symbolBrush=symbol_fill_color, symbolPen=symbol_outline_color)

    pg.exec() # Runs it


if __name__ == '__main__':
    # pyqtgraph.examples.run()
    DrawEngine(3,5,1.5,1.5,2,6,10)
