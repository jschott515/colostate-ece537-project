import csecg
import csecg.loader.ptbdb
import csecg.plot
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
    compressed_data = phi @ ecg.signals

    csecg.plot.show_compression(
        "ECG Lead II Channel",
        ecg.get("ii"),
        compressed_data[:, 1]
    )

    # Compute the basis matrix and solve for the sparse coefficient matrix
    psi = csecg.basis_matrix(ecg.length)
    reconstructed_coefs = csecg.group_lasso_solver(compressed_data, phi, psi)

    # Recover the signal!
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449 Equation 15
    recovered_signals = psi @ reconstructed_coefs

    # Calculate PRD per channel
    for lead, source, recovered in zip(ecg.channel_names, ecg.signals.T, recovered_signals.T):
        print(f"Lead {lead} - PRD = {csecg.prd(source, recovered):.2f}%")

    csecg.plot.show_recovery_single(
        f"ECG Lead II Source versus Recovered (CR = {cr})",
        ecg.get("ii"),
        recovered_signals[:, 1]
    )
    csecg.plot.show_recovery_all(ecg.signals, recovered_signals)


if __name__ == "__main__":
    main()
