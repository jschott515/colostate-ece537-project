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
        sampto=7250,
    )

if __name__ == "__main__":
    main()
