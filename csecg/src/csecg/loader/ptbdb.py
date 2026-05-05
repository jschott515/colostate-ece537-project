import typing
import pathlib

import wfdb
import numpy
import numpy.typing


def load_12_lead_record(
        record_name: pathlib.Path,
        sampfrom: int = 0,
        sampto: int | None = None,
) -> typing.Tuple[numpy.typing.NDArray[numpy.str_], numpy.typing.NDArray[numpy.float64]]:
    record = wfdb.rdrecord(record_name, sampfrom=sampfrom, sampto=sampto)
    # Filter only the 12 lead data from .dat file
    dat_indices = [i for i, f in enumerate(record.file_name) if f.endswith('.dat')]
    dat_signals = record.p_signal[:, dat_indices]
    dat_names = numpy.array([record.sig_name[i] for i in dat_indices])
    return dat_names, dat_signals
