import numpy

from ._ecg import Ecg


def sensing_matrix(ecg: Ecg, compression_ratio: int) -> numpy.typing.NDArray[numpy.float64]:
    # Construct a reference signal from Leads II, aVF
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449 Equation 7
    x0 = numpy.sqrt(0.5 * (ecg.get('ii') ** 2 + ecg.get('avf') ** 2))

    # Center the reference signal and apply thresholding
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449 Equation 8, 9
    xp = numpy.abs(x0 - numpy.mean(x0))
    p = (xp >= numpy.percentile(xp, 60)).astype(int).flatten()

    # Construct the sensing matrix
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449 Equation 10
    compressed_len = ecg.length // compression_ratio
    phi = numpy.zeros((compressed_len, ecg.length), dtype=int)
    for i in range(compressed_len):
        phi[i, :] = numpy.roll(p, -i * compression_ratio)

    return phi
