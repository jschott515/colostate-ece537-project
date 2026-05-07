import numpy
import numpy.typing
import matplotlib.pyplot


def show_compression(
    title: str,
    source: numpy.typing.NDArray[numpy.float64],
    compressed: numpy.typing.NDArray[numpy.float64],
) -> None:
    fig, axes = matplotlib.pyplot.subplots(1, 2, figsize=(14, 5))

    n = source.shape[0]
    m = compressed.shape[0]

    fig.suptitle(title + f" (CR = {n // m})")
    axes[0].plot(numpy.arange(len(source)), numpy.squeeze(source), color='blue')
    axes[0].set_title(f"Uncompressed (N = {n})")
    axes[0].set_xlabel("Sample")
    axes[0].set_ylabel("Amplitude")

    axes[1].plot(numpy.arange(len(compressed)), numpy.squeeze(compressed), color='red')
    axes[1].set_title(f"Compressed (M = {compressed.shape[0]})")
    axes[1].set_xlabel("Sample")
    axes[1].set_ylabel("Amplitude")

    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.show()