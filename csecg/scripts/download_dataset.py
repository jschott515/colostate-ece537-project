import csecg.util

if __name__ == "__main__":
    if csecg.util.dataset_exists():
        print(f"Dataset exists at {csecg.util.DATASET.as_posix()}, skipping...")
    else:
        print(f"Downloading dataset to {csecg.util.DATASET.as_posix()}...")
        assert csecg.util.download_dataset()
