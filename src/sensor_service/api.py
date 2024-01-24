from collections import deque

import numpy as np
import pydaq
from fastapi import APIRouter

from src.sensor_service.config import Config

router = APIRouter()

data_deque = deque(maxlen=1000)
config = Config()

device = config.DAQ_DEVICE


@router.post("/daq")
async def daq(num_samples: int = 1000):
    """
    Collects data from the DAQ device and returns it as a list
    """
    data = device.read(num_samples=num_samples)

    data = data.squeeze().tolist()

    # fft
    sample_rate = device.sample_rate
    fft = np.abs(np.fft.rfft(data)).tolist()
    fft_freq = np.fft.rfftfreq(len(data), 1 / sample_rate).tolist()

    return {
        "code": 200,
        "message": "success",
        "data": {"data": data, "fft": {"amplitude": fft, "frequency": fft_freq}},
    }
