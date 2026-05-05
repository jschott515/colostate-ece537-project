import numpy

class Ecg:
    def __init__(
        self,
        channel_names: numpy.typing.NDArray[numpy.str_],
        signals: numpy.typing.NDArray[numpy.float64],
    ) -> None:
        self.channel_names = channel_names
        self.signals = signals
        self.length, self.channels = signals.shape

    def get(self, name: str) -> numpy.typing.NDArray[numpy.float64]:
        assert name in self.channel_names
        return self.signals[:, numpy.where(self.channel_names == name)]
