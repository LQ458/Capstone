# cython: boundscheck=False, wraparound=False, cdivision=True, language_level=3
from libc.stdint cimport uint64_t

cdef int width  = 7
cdef int height = 6
cdef int bits = 7

cdef uint64_t BOTTOM_MASK[7]
cdef uint64_t BOARD_MASK[7]
cdef uint64_t TOP_MASK[7]

for c in range(7):
    BOTTOM_MASK[c] = 1 << (c * bits)
    BOARD_MASK[c] = ((1 << height) - 1) << (c * bits)
    TOP_MASK[c] = 1 << (c * bits + height - 1)

cdef int ORDER[7]
ORDER[:] = [3, 2, 4, 1, 5, 0, 6]

cpdef bint win(uint64_t bb):
    cdef uint64_t m
    m = bb & (bb >> bits)
    if m & (m >> (2 * bits)):
        return True
    m = bb & (bb >> (bits + 1))
    if m & (m >> (2 * (bits + 1))):
        return True
    m = bb & (bb >> (bits - 1))
    if m & (m >> (2 * (bits - 1))):
        return True
    m = bb & (bb >> 1)
    if m & (m >> 2):
        return True
    return False

cdef uint64_t LINES[69]
cdef int idx = 0
cdef uint64_t mask

for r in range(height):
    for c in range(width - 3):
        mask = 0
        for i in range(4):
            mask |= 1 << ((c + i) * bits + r)
        LINES[idx] = mask; idx += 1

for c in range(width):
    for r in range(height - 3):
        mask = 0
        for i in range(4):
            mask |= 1 << (c * bits + r + i)
        LINES[idx] = mask; idx += 1

for c in range(width - 3):
    for r in range(height - 3):
        mask = 0
        for i in range(4):
            mask |= 1 << ((c + i) * bits + r + i)
        LINES[idx] = mask; idx += 1

for c in range(width - 3):
    for r in range(3, height):
        mask = 0
        for i in range(4):
            mask |= 1 << ((c + i) * bits + r - i)
        LINES[idx] = mask; idx += 1

cdef inline int pop64(uint64_t x):
    cdef int cnt = 0
    while x:
        x &= x - 1
        cnt += 1
    return cnt

cdef int eval_bb(uint64_t cur, uint64_t opp):
    cdef uint64_t occ = cur | opp
    cdef int score = 0
    score += 3 * pop64(cur & BOARD_MASK[3])

    cdef int c_cnt, o_cnt
    for mask in LINES:
        c_cnt = pop64(cur & mask)
        o_cnt = pop64(opp & mask)
        if c_cnt and o_cnt:
            continue
        if c_cnt == 4:
            score += 100
        elif c_cnt == 3 and (occ & mask) != mask:
            score += 5
        elif c_cnt == 2 and pop64(occ & mask) == 2:
            score += 2
        elif o_cnt == 3 and (occ & mask) != mask:
            score -= 4
    return score

cdef int nega(uint64_t cur, uint64_t opp, int depth, int alpha, int beta):
    cdef int best = -1_000_000
    if depth == 0 or win(cur) or win(opp):
        if win(cur):
            return  1_000_000 - (8 - depth)
        if win(opp):
            return -1_000_000 + (8 - depth)
        return eval_bb(cur, opp)

    cdef int i, col, score
    for i in range(7):
        col = ORDER[i]
        if (cur | opp) & TOP_MASK[col]:
            continue
        mask = ((cur | opp) + BOTTOM_MASK[col]) & BOARD_MASK[col]
        score = -nega(opp, cur | mask, depth - 1, -beta, -alpha)

        if score > best:
            best = score
        if score > alpha:
            alpha = score
        if alpha >= beta:
            break
    return best

cpdef int find_best(uint64_t cur, uint64_t opp, int depth = 8):
    cdef int best_col = -1
    cdef int best_score = -1_000_000
    cdef int i, col, score
    for i in range(7):
        col = ORDER[i]
        if (cur | opp) & TOP_MASK[col]:
            continue
        mask = ((cur | opp) + BOTTOM_MASK[col]) & BOARD_MASK[col]
        score = -nega(opp, cur | mask, depth - 1, -1_000_000, 1_000_000)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col
