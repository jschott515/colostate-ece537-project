import numpy
import numpy.typing


def mexican_hat(length: int, a: float, b: float) -> numpy.typing.NDArray[numpy.float64]:
    n = numpy.arange(length)
    # Construct wavelet
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449/ Equation 5
    scalar = (2 / (numpy.sqrt(3 * a) * (numpy.pi ** 0.25)))
    n_min_b_ovr_a_sq = ((n - b) / a) ** 2
    wavelet = scalar * (1 - n_min_b_ovr_a_sq) * numpy.exp(-0.5 * n_min_b_ovr_a_sq)
    return wavelet


def basis_matrix(length: int) -> numpy.typing.NDArray[numpy.float64]:
    cols = []
    # Construt wavelet dictionary
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449/ Equation 4
    for m in range(1, int(numpy.floor(numpy.log2(length))) + 1):
        a = 2 ** m
        for k in range((length - 1) // a + 1):
            b = k * a
            psi = mexican_hat(length, a, b)
            cols.append(psi)
    # Pad with an additional column
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449/ Equation 12
    u = (1 / numpy.sqrt(length)) * numpy.ones(length)
    return numpy.column_stack(cols)
