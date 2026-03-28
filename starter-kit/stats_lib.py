#!/usr/bin/env python3
"""
Community Data Lab — Shared Statistics Library
stdlib only (math module). No pandas, numpy, scipy.

Provides:
  - pearson_r: Pearson correlation coefficient
  - ols_2pred: Two-predictor OLS regression via normal equations
  - compute_t_stat: t-statistic for OLS coefficients
  - t_significant: Approximate significance test
  - normalize_01: Min-max normalization to [0, 1]
  - composite_score: Weighted composite scoring with A-F grades
"""

import math


def safe_float(v):
    """Convert a value to float, returning None if not possible."""
    if v is None or v == "*" or v == "":
        return None
    try:
        f = float(v)
        return None if f == -666666666 else f
    except (ValueError, TypeError):
        return None


def pearson_r(xs, ys):
    """Pearson correlation coefficient for two equal-length lists.
    Returns None if n < 3 or either variable has zero variance."""
    n = len(xs)
    if n < 3:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def ols_2pred(y_vec, x1_vec, x2_vec):
    """
    OLS regression: y = b0 + b1*x1 + b2*x2
    Solves normal equations via 3x3 matrix inversion (Cramer's rule).

    Returns dict with:
      intercept, b1, b2, r_squared, r_squared_x2_only, r_squared_added

    Returns None if n < 4 or matrix is singular.
    """
    n = len(y_vec)
    if n < 4:
        return None

    # Build X'X (3x3) and X'y (3x1)
    s1 = sum(x1_vec)
    s2 = sum(x2_vec)
    s11 = sum(a * a for a in x1_vec)
    s22 = sum(a * a for a in x2_vec)
    s12 = sum(a * b for a, b in zip(x1_vec, x2_vec))
    sy = sum(y_vec)
    s1y = sum(a * b for a, b in zip(x1_vec, y_vec))
    s2y = sum(a * b for a, b in zip(x2_vec, y_vec))

    A = [
        [n, s1, s2],
        [s1, s11, s12],
        [s2, s12, s22],
    ]

    def det3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    d = det3(A)
    if abs(d) < 1e-12:
        return None

    def minor(m, i, j):
        return [[m[r][c] for c in range(3) if c != j] for r in range(3) if r != i]

    def det2(m):
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    cof = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            cof[i][j] = ((-1) ** (i + j)) * det2(minor(A, i, j))

    inv = [[cof[j][i] / d for j in range(3)] for i in range(3)]

    rhs = [sy, s1y, s2y]
    b = [sum(inv[i][j] * rhs[j] for j in range(3)) for i in range(3)]
    b0, b1, b2 = b

    # R-squared (full model)
    y_mean = sy / n
    ss_tot = sum((yi - y_mean) ** 2 for yi in y_vec)
    ss_res = sum((yi - (b0 + b1 * x1i + b2 * x2i)) ** 2
                 for yi, x1i, x2i in zip(y_vec, x1_vec, x2_vec))
    r_sq = 1 - ss_res / ss_tot if ss_tot > 0 else None

    # R-squared (x2 only — for computing what x1 adds beyond x2)
    x2_mean = s2 / n
    x2_var = sum((a - x2_mean) ** 2 for a in x2_vec)
    if x2_var > 0:
        x2_cov = sum((a - x2_mean) * (yi - y_mean) for a, yi in zip(x2_vec, y_vec))
        b2_only = x2_cov / x2_var
        b0_only = y_mean - b2_only * x2_mean
        ss_res_x2 = sum((yi - (b0_only + b2_only * x2i)) ** 2
                        for yi, x2i in zip(y_vec, x2_vec))
        r_sq_x2 = 1 - ss_res_x2 / ss_tot if ss_tot > 0 else None
    else:
        r_sq_x2 = None

    r_sq_added = None
    if r_sq is not None and r_sq_x2 is not None:
        r_sq_added = r_sq - r_sq_x2

    return {
        "intercept": round(b0, 6),
        "b1": round(b1, 6),
        "b2": round(b2, 6),
        "r_squared": round(r_sq, 4) if r_sq is not None else None,
        "r_squared_control_only": round(r_sq_x2, 4) if r_sq_x2 is not None else None,
        "r_squared_added": round(r_sq_added, 4) if r_sq_added is not None else None,
        "n": n,
    }


def compute_t_stat(b_tuple, y_vec, x1_vec, x2_vec, predictor_idx):
    """Compute t-statistic for a coefficient in 2-predictor OLS.
    b_tuple = (b0, b1, b2). predictor_idx: 0=intercept, 1=b1, 2=b2."""
    n = len(y_vec)
    if n <= 3:
        return None
    b0, b1, b2 = b_tuple
    residuals = [yi - (b0 + b1 * x1i + b2 * x2i)
                 for yi, x1i, x2i in zip(y_vec, x1_vec, x2_vec)]
    mse = sum(r * r for r in residuals) / (n - 3)

    s1 = sum(x1_vec)
    s2 = sum(x2_vec)
    s11 = sum(a * a for a in x1_vec)
    s22 = sum(a * a for a in x2_vec)
    s12 = sum(a * b for a, b in zip(x1_vec, x2_vec))

    A = [[n, s1, s2], [s1, s11, s12], [s2, s12, s22]]

    def det3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    d = det3(A)
    if abs(d) < 1e-12:
        return None

    def minor(m, i, j):
        return [[m[r][c] for c in range(3) if c != j] for r in range(3) if r != i]

    def det2(m):
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    cof = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            cof[i][j] = ((-1) ** (i + j)) * det2(minor(A, i, j))

    inv = [[cof[j][i] / d for j in range(3)] for i in range(3)]

    var_b = inv[predictor_idx][predictor_idx]
    if var_b <= 0:
        return None
    se_b = math.sqrt(mse * var_b)
    if se_b == 0:
        return None
    return b_tuple[predictor_idx] / se_b


def t_significant(t_val, n, alpha=0.05):
    """Approximate significance test using conservative critical values."""
    if t_val is None:
        return None
    df = n - 3
    if df >= 30:
        crit = 2.0
    elif df >= 15:
        crit = 2.13
    elif df >= 10:
        crit = 2.23
    else:
        crit = 2.57
    return abs(t_val) > crit


def normalize_01(values):
    """Min-max normalize a list of numbers to [0, 1]. Returns list of floats.
    None values in input are preserved as None in output."""
    nums = [v for v in values if v is not None]
    if not nums:
        return [None] * len(values)
    lo, hi = min(nums), max(nums)
    rng = hi - lo
    if rng == 0:
        return [0.5 if v is not None else None for v in values]
    return [(v - lo) / rng if v is not None else None for v in values]


def composite_score(indicators, weights):
    """Compute weighted composite score from normalized indicators.

    Args:
        indicators: dict of {name: [values_per_tract]}
        weights: dict of {name: weight} (must sum to ~1.0)

    Returns: list of composite scores (0-1 scale), one per tract.
    """
    n = len(next(iter(indicators.values())))
    # Normalize each indicator
    normed = {}
    for name, vals in indicators.items():
        normed[name] = normalize_01(vals)

    scores = []
    for i in range(n):
        total = 0.0
        w_sum = 0.0
        for name, w in weights.items():
            if name in normed and normed[name][i] is not None:
                total += w * normed[name][i]
                w_sum += w
        scores.append(round(total / w_sum, 4) if w_sum > 0 else None)
    return scores


def assign_grades(scores, thresholds):
    """Assign A-F grades based on percentile thresholds.

    Args:
        scores: list of composite scores (0-1)
        thresholds: dict with keys A, B, C, D as percentile cutoffs

    Returns: list of grade strings.
    """
    valid = sorted([s for s in scores if s is not None])
    if not valid:
        return ["N/A"] * len(scores)

    def pct_value(p):
        idx = int(p * (len(valid) - 1))
        return valid[idx]

    cuts = {
        "A": pct_value(thresholds["A"]),
        "B": pct_value(thresholds["B"]),
        "C": pct_value(thresholds["C"]),
        "D": pct_value(thresholds["D"]),
    }

    grades = []
    for s in scores:
        if s is None:
            grades.append("N/A")
        elif s >= cuts["A"]:
            grades.append("A")
        elif s >= cuts["B"]:
            grades.append("B")
        elif s >= cuts["C"]:
            grades.append("C")
        elif s >= cuts["D"]:
            grades.append("D")
        else:
            grades.append("F")
    return grades
