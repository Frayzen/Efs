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
    for c in range(n):
        cur = (WIDTH * HEIGHT) // 2
        if c % 2 == 0 and (WIDTH * HEIGHT) % 2 == 1:
            cur += 1
        for p in range(0, cur):
            p *= 2
            if c % 2 == 1:
                p += 1
            i = p % WIDTH
            j = p // WIDTH
            # draw_circle((i + 0.5, j + 0.5), GREEN if c % 2 == 0 else RED, 8)

            if s[j + 1, i + 1] == 0:
                u[j, i] = 0
                u[j, i + 1] = 0
                v[j, i] = 0
                v[j + 1, i] = 0
                continue
            d = u[j, i + 1] - u[j, i] + v[j + 1, i] - v[j, i]
            if OVERRELAXATION:
                d *= 1.9
            si = i + 1
            sj = j + 1
            curs = s[sj, si + 1] + s[sj, si - 1] + s[sj + 1, si] + s[sj - 1, si]
            u[j, i] += d * s[sj, si - 1] / curs
            u[j, i + 1] -= d * s[sj, si + 1] / curs
            v[j, i] += d * s[sj - 1, si] / curs
            v[j + 1, i] -= d * s[sj + 1, si] / curs
