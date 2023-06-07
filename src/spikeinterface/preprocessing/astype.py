import numpy as np

from ..core.core_tools import define_function_from_class
from .basepreprocessor import BasePreprocessor, BasePreprocessorSegment
from .filter import fix_dtype


class AstypeRecording(BasePreprocessor):
    """The spikeinterface analog of numpy.astype

    Converts a recording to another dtype on the fly.
    """

    name = "astype"

    def __init__(
        self,
        recording,
        dtype=None,
    ):
        dtype_ = fix_dtype(recording, dtype)
        BasePreprocessor.__init__(self, recording, dtype=dtype_)

        for parent_segment in recording._recording_segments:
            rec_segment = AstypeRecordingSegment(
                parent_segment,
                dtype,
            )
            self.add_recording_segment(rec_segment)

        self._kwargs = dict(
            recording=recording,
            dtype=dtype_.str,
        )


class AstypeRecordingSegment(BasePreprocessorSegment):
    def __init__(
        self,
        parent_recording_segment,
        dtype,
    ):
        BasePreprocessorSegment.__init__(self, parent_recording_segment)
        self.dtype = dtype

    def get_traces(self, start_frame, end_frame, channel_indices):
        if channel_indices is None:
            channel_indices = slice(None)
        traces = self.parent_recording_segment.get_traces(start_frame, end_frame, channel_indices)
        # if uint --> take care of offset
        traces_dtype = traces.dtype
        if traces_dtype.kind == "u" and np.dtype(self.dtype).kind == "i":
            itemsize = traces_dtype.itemsize
            assert itemsize < 8, "Cannot upcast uint64!"
            nbits = traces_dtype.itemsize * 8
            # upcast to int with double itemsize
            traces = traces.astype(f"int{2 * (traces_dtype.itemsize) * 8}") - 2 ** (nbits - 1)
        return traces.astype(self.dtype, copy=False)


# function for API
astype = define_function_from_class(source_class=AstypeRecording, name="astype")
