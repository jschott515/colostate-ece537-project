import cvxpy
import numpy
import numpy.typing


def prd(
    x: numpy.typing.NDArray[numpy.float64],
    x_hat: numpy.typing.NDArray[numpy.float64],
) -> float:
    """
    Calculate PRD for a given lead.
    https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449 Equation 16
    """
    return (numpy.linalg.norm(x - x_hat, 2) / numpy.linalg.norm(x, 2)) * 100

def lasso_solver(
    compressed_data: numpy.typing.NDArray[numpy.float64],
    phi: numpy.typing.NDArray[numpy.float64],
    psi: numpy.typing.NDArray[numpy.float64],
    regularization: float = 1e-3
) -> numpy.typing.NDArray[numpy.float64]:
    """
    Lasso (L1 Norm) - https://stat.ethz.ch/Manuscripts/buhlmann/logistic-grouplasso-final.pdf
    Recover the sparse coefficient matrix given the compressed data, sensing matrix phi and sparsity matrix psi
    Encourages sparsity in the coefficient matrix
    """
    c_var = cvxpy.Variable((psi.shape[1], compressed_data.shape[1]))
    cost_func = regularization * cvxpy.norm(c_var, 1)
    prob = cvxpy.Problem(
        cvxpy.Minimize(
            cvxpy.norm(compressed_data - (phi @ psi @ c_var), "fro") ** 2 + cost_func
        )
    )
    prob.solve(solver=cvxpy.SCS)
    return c_var.value


def group_lasso_solver(
    compressed_data: numpy.typing.NDArray[numpy.float64],
    phi: numpy.typing.NDArray[numpy.float64],
    psi: numpy.typing.NDArray[numpy.float64],
    regularization: float = 1e-3
) -> numpy.typing.NDArray[numpy.float64]:
    """
    Group Lasso (L2-L1 Norm) - https://stat.ethz.ch/Manuscripts/buhlmann/logistic-grouplasso-final.pdf
    Recover the sparse coefficient matrix given the compressed data, sensing matrix phi and sparsity matrix psi
    Encourages row sparsity, rather than independent sparsity
    Implements https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449/ Equation 13, 14 with p = 1
    """
    c_var = cvxpy.Variable((psi.shape[1], compressed_data.shape[1]))
    cost_func = regularization * cvxpy.sum(cvxpy.norm(c_var, 2, axis=1))
    prob = cvxpy.Problem(
        cvxpy.Minimize(
            cvxpy.norm(compressed_data - (phi @ psi @ c_var), "fro") ** 2 + cost_func
        )
    )
    prob.solve(solver=cvxpy.SCS)
    return c_var.value
