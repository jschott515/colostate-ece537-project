import matplotlib.pyplot
import numpy
import numpy.typing


def show_recovery_all(
    source: numpy.typing.NDArray[numpy.float64],
    recovered: numpy.typing.NDArray[numpy.float64],
) -> None:
    fig, axes = matplotlib.pyplot.subplots(3, 4, figsize=(14, 5))

    t = numpy.arange(source.shape[0])
    leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']

    for i, (lead, source_lead, recovered_lead) in enumerate(zip(leads, source.T, recovered.T)):
        axes[i // 4, i % 4].plot(t, source_lead, 'b-', label='source')
        axes[i // 4, i % 4].plot(t, recovered_lead, 'r--', label='recovered')
        axes[i // 4, i % 4].set_title(f"Lead {lead}")
        axes[i // 4, i % 4].set_xlabel("Sample")
        axes[i // 4, i % 4].set_ylabel("Amplitude")

    fig.legend(*axes[0, 0].get_legend_handles_labels(), loc='lower right', ncols=2)

    matplotlib.pyplot.tight_layout()
    matplotlib.pyplot.show()


def show_recovery_single(
    title: str,
    source: numpy.typing.NDArray[numpy.float64],
    recovered: numpy.typing.NDArray[numpy.float64],
) -> None:
    fig, ax = matplotlib.pyplot.subplots(1, 1, figsize=(14, 5))

    fig.suptitle(title)
    ax.plot(numpy.arange(len(source)), numpy.squeeze(source), 'b-', label="source")
    ax.plot(numpy.arange(len(recovered)), numpy.squeeze(recovered), 'r--', label="recovered")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")

    matplotlib.pyplot.show()
