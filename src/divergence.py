from consts import GREEN, HEIGHT, OVERRELAXATION, RED, WIDTH
import numpy as np
from mac import MacGrid
from ui import draw_circle

def compute_divergence(u, v):
    """
    Compute the divergence at cell centers from MAC grid velocities.
    u.shape = (H, W+1), v.shape = (H+1, W)
    Returns: divergence of shape (H, W)
    """
    du_dx = u[:, 1:] - u[:, :-1]  # difference in x-direction
    dv_dy = v[1:, :] - v[:-1, :]  # difference in y-direction
    return du_dx + dv_dy

def print_max_divergence(mac):
    divergence = compute_divergence(mac.xgrid, mac.ygrid)
    max_div = np.max(np.abs(divergence))
    print(f"Max abs divergence after projection: {max_div:.6e}")

def clear_divergence(mac: MacGrid, n=100, tol=1e-5):
    u, v, s = mac.xgrid, mac.ygrid, mac.s
    for _ in range(n):
        max_d = 0.0
        for parity in [0, 1]:
            for j in range(HEIGHT):
                for i in range((j + parity) % 2, WIDTH, 2):
                    if s[j + 1, i + 1] == 0:
                        continue
                    d = u[j, i + 1] - u[j, i] + v[j + 1, i] - v[j, i]
                    if OVERRELAXATION:
                        d *= 1.9
                    si, sj = i + 1, j + 1
                    curs = (
                        s[sj, si + 1]
                        + s[sj, si - 1]
                        + s[sj + 1, si]
                        + s[sj - 1, si]
                    )
                    if curs == 0:
                        continue
                    u[j, i] += d * s[sj, si - 1] / curs
                    u[j, i + 1] -= d * s[sj, si + 1] / curs
                    v[j, i] += d * s[sj - 1, si] / curs
                    v[j + 1, i] -= d * s[sj + 1, si] / curs
                    max_d = max(max_d, abs(d))
        if max_d < tol:
            break
    print_max_divergence(mac)


# def clear_divergence(mac: MacGrid):
#     n = 100
#     u = mac.xgrid
#     v = mac.ygrid

#     s = mac.s
#     # div = np.zeros((HEIGHT, WIDTH))
#     for c in range(n):
#         cur = (WIDTH * HEIGHT) // 2
#         if c % 2 == 0 and (WIDTH * HEIGHT) % 2 == 1:
#             cur += 1
#         for p in range(0, cur):
#             p *= 2
#             if c % 2 == 1:
#                 p += 1
#             i = p % WIDTH
#             j = p // WIDTH
#             # draw_circle((i + 0.5, j + 0.5), GREEN if c % 2 == 0 else RED, 8)

#             if s[j + 1, i + 1] == 0:
#                 u[j, i] = 0
#                 u[j, i + 1] = 0
#                 v[j, i] = 0
#                 v[j + 1, i] = 0
#                 continue
#             d = u[j, i + 1] - u[j, i] + v[j + 1, i] - v[j, i]
#             if OVERRELAXATION:
#                 d *= 1.9
#             si = i + 1
#             sj = j + 1
#             curs = s[sj, si + 1] + s[sj, si - 1] + s[sj + 1, si] + s[sj - 1, si]
#             u[j, i] += d * s[sj, si - 1] / curs
#             u[j, i + 1] -= d * s[sj, si + 1] / curs
#             v[j, i] += d * s[sj - 1, si] / curs
#             v[j + 1, i] -= d * s[sj + 1, si] / curs
