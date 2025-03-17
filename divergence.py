from consts import GREEN, HEIGHT, OVERRELAXATION, RED, WIDTH
import numpy as np
from mac import MacGrid
from ui import draw_circle


def clear_divergence(mac: MacGrid):
    n = 20
    u = mac.xgrid
    v = mac.ygrid

    s = mac.s
    # div = np.zeros((HEIGHT, WIDTH))
    for _ in range(n):
        for i in range(0, WIDTH):
            for j in range(0, HEIGHT):
                si = i + 1
                sj = j + 1
                d = u[j, i + 1] - u[j, i] + v[j + 1, i] - v[j, i]
                d *= s[sj, si]
                if OVERRELAXATION:
                    d *= 1.9
                curs = s[sj, si + 1] + s[sj, si - 1] + s[sj + 1, si] + s[sj - 1, si]
                if curs == 0:
                    continue
                u[j, i] += d * s[sj, si - 1] / curs
                u[j, i + 1] -= d * s[sj, si + 1] / curs
                v[j, i] += d * s[sj - 1, si] / curs
                v[j + 1, i] -= d * s[sj + 1, si] / curs

                # if curs == 3:
                #     draw_circle((i + 0.5, j + 0.5), GREEN, s[sj, si] * 10)
                # draw_circle((i - 1 + 0.5, j - 1 + 0.5), RED, s[sj - 1, si - 1] * 5)
                # draw_circle((i + 1 + 0.5, j - 1 + 0.5), RED, s[sj + 1, si - 1] * 5)
                # draw_circle((i - 1 + 0.5, j + 1 + 0.5), RED, s[sj - 1, si + 1] * 5)
                # draw_circle((i + 1 + 0.5, j + 1 + 0.5), RED, s[sj + 1, si + 1] * 5)
