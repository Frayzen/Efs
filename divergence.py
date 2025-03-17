from consts import HEIGHT, OVERRELAXATION, WIDTH
import numpy as np
from mac import MacGrid


def clear_divergence(mac: MacGrid):
    n = 20
    u = mac.xgrid
    v = mac.ygrid

    s = mac.s
    # div = np.zeros((HEIGHT, WIDTH))
    for _ in range(n):
        for i in range(0, WIDTH):
            for j in range(0, HEIGHT):
                if (
                    # i == 0
                    # and j == 0
                    # and i == WIDTH - 1
                    # and j == HEIGHT - 1
                    s[j + 1, i + 1]
                    == 0
                ):
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
