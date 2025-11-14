import numpy as np
from scipy.io import mmread
from scipy.sparse.linalg import LinearOperator

def bicgstab_unpreconditioned(A, b, num_iters):
    """
    Unpreconditioned BiCGSTAB with:
      - x0 = 0
      - r0 = b
      - r_hat0 = r0
      - fixed number of iterations (no stopping test)

    Parameters
    ----------
    A : scipy.sparse matrix, NumPy array, or LinearOperator
        Represents the matrix in Ax = b.
    b : 1D NumPy array
        Right-hand side vector.
    num_iters : int
        Number of BiCGSTAB iterations to perform.

    Returns
    -------
    x : 1D NumPy array
        Approximate solution after num_iters iterations.
    """
    b = np.asarray(b, dtype=float).ravel()
    n = b.shape[0]

    # Initial guess x0 = 0
    x = np.zeros_like(b)

    # r0 = b - A x0 = b
    r = b.copy()
    r_hat = r.copy()  # r_hat0 = r0

    # Scalars
    rho_prev = 1.0
    alpha = 1.0
    omega = 1.0

    # Vectors
    v = np.zeros_like(b)
    p = np.zeros_like(b)

    def matvec(vec):
        # Support sparse matrices, dense arrays, or LinearOperators
        return A @ vec

    for k in range(num_iters):
        rho = np.dot(r_hat, r)
        if rho == 0.0:
            # Breakdown: can't continue
            # For benchmarking you can just break or raise
            # Here we'll break and return current x
            break

        if k == 0:
            p = r.copy()
        else:
            beta = (rho / rho_prev) * (alpha / omega)
            p = r + beta * (p - omega * v)

        v = matvec(p)
        denom = np.dot(r_hat, v)
        if denom == 0.0:
            # Another possible breakdown
            break
        alpha = rho / denom

        s = r - alpha * v

        # Optionally, you could check ||s|| here, but PI said no stopping tests
        t = matvec(s)
        t_norm_sq = np.dot(t, t)
        if t_norm_sq == 0.0:
            # Degenerate case, avoid division by zero
            break
        omega = np.dot(t, s) / t_norm_sq

        # Update solution and residual
        x = x + alpha * p + omega * s
        r = s - omega * t

        rho_prev = rho

    return x



# 1. Load the matrix
A_sp = mmread("fidap005.mtx.gz").tocsr()
n = A_sp.shape[0]

# (Optional) Wrap as a LinearOperator if you want a matvec-based interface:
A = LinearOperator(shape=(n, n), matvec=lambda x: A_sp @ x)

# 2. Pick or (load) a right-hand side b
b = mmread("fidap005_rhs1.mtx.gz")
b = np.asarray(b).ravel()

# 3. Run your BiCGSTAB for, say, 100 iterations
x_approx = bicgstab_unpreconditioned(A, b, num_iters=100)

# 4. Check the residual norm
residual = b - (A @ x_approx)
print("||b - A x|| =", np.linalg.norm(residual))