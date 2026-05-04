import csecg.util


def main() -> None:
    if not csecg.util.dataset_exists():
        print("Missing dataset... Download via `python -m csecg.util.download_dataset`")
        return


if __name__ == "__main__":
    main()
