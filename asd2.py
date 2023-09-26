from typing import NewType, Literal
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Pos:
    x: int
    y: int


PL = tuple[tuple[Pos, ...], ...]
Hash = NewType("Hash", int)
Image = list[list[int]]


def Build_Gkchp(w: int, h: int) -> PL:
    ret: list[tuple[Pos, ...]] = []
    for k in range(h):
        items = [Pos(i, round((k * i) / (h - 1)) % w) for i in range(h)]
        ret.append(tuple(items))
    return tuple(ret)


def Calculate_Patterns_ASD2(w: int, h: int, I: Image, pl: PL) -> Image:
    if h > 1:
        h_L = h // 2
        h_R = h - h_L
        I_L = I[:h_L]
        I_R = I[h_L:]
        pl_L, k_L = Get_Patterns_Section(pl, 0, h_L)
        pl_R, k_R = Get_Patterns_Section(pl, h_L, h_R)
        J_L = Calculate_Patterns_ASD2(w, h_L, I_L, pl_L)
        J_R = Calculate_Patterns_ASD2(w, h_R, I_R, pl_R)
        J: Image = [[0] * w for _ in range(len(pl))]
        for k, p in enumerate(pl):
            pos_R = p[h_L]
            for j in range(w):
                J[k][j] = J_L[k_L[k]][j] + J_R[k_R[k]][(j + pos_R.y) % w]
        return J
    else:
        return I


def Get_Patterns_Section(pl: PL, i0: int, w: int):
    tab: list[tuple[Hash, tuple[Pos], int]] = []
    for k, p in enumerate(pl):
        pos_0 = p[i0]
        sp_list: list[Pos] = []
        for i in range(w):
            pos = p[i0 + i]
            sp_list.append(Pos(i, pos.y - pos_0.y))
        sp = tuple(sp_list)
        tab.append((Hash(hash(sp)), sp, k))
    tab.sort(key=lambda r: r[0])
    spl: list[tuple[Pos]] = []
    ind: list[int | None] = [None] * len(pl)
    hash_prev: tuple[Hash, tuple[Pos]] | None = None
    n = 0
    for hsh, sp, k in tab:
        if (hsh, sp) != hash_prev:
            spl.append(sp)
            n += 1
        ind[k] = n - 1
        hash_prev = (hsh, sp)
    return tuple(spl), ind


def asd2(I: Image, sign: Literal[-1, 1]) -> Image:
    h, w = len(I), len(I[0])
    pl = Build_Gkchp(w, h)
    img = Calculate_Patterns_ASD2(w, h, I, pl)
    return img


# def asna(w: int, h: int, I: Image) -> Image:
#     pl = Build_Gkchp(w, h)
#     J = [[0] * w for _ in range(h)]
#     k = 0
#     for p in pl:
#         for pos in p:
#             i, dj = pos.x, pos.y
#             for j in range(h):
#                 J[j][k] += I[(j + dj) % h][i]
#         k += 1
#     return J
