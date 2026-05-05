import numpy

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
        sampto=4250,
    )
    ecg = csecg.Ecg(channel_names, signals)

    # Compress the signal!
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC8587449 Equation 10
    cr = 4
    compressed_data = numpy.matmul(csecg.sensing_matrix(ecg, cr), signals)


if __name__ == "__main__":
    main()
