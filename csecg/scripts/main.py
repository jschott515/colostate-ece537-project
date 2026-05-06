import matplotlib.pyplot

import csecg
import csecg.loader.ptbdb
import csecg.util


def main() -> None:
    if not csecg.util.dataset_exists():
        print("Missing dataset... Download via `python -m csecg.util.download_dataset`")
        return

    record_name = csecg.util.DATASET / "patient104" / "s0306lre"
    channel_names, signals = csecg.loader.ptbdb.load_12_lead_record(
        record_name,
        sampfrom=2250,
        sampto=3250,
    )
    ecg = csecg.Ecg(channel_names, signals)

    # Compress the signal!
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449 Equation 10
    cr = 10
    phi = csecg.sensing_matrix(ecg, cr)
    compressed_data = phi @ signals

    # Compute the basis matrix and solve for the sparse coefficient matrix
    psi = csecg.basis_matrix(ecg.length)
    reconstructed_coefs = csecg.group_lasso_solver(compressed_data, phi, psi)

    # Recover the signal!
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449 Equation 15
    reconstructed_signal = psi @ reconstructed_coefs

    for lead, recovered_lead in zip(ecg.signals.T, reconstructed_signal.T):
        matplotlib.pyplot.plot(lead, "b-")
        matplotlib.pyplot.plot(recovered_lead, "r--")
        matplotlib.pyplot.show()


if __name__ == "__main__":
    main()
