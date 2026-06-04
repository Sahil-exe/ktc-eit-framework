"""
training_data_plugin.py
-----------------------
Loads the KTC training data from the local Codes_Matlab/ layout:

    Codes_Matlab/TrainingData/data{N}.mat  -- voltages + Inj + Mpat
    Codes_Matlab/TrainingData/ref.mat       -- Uelref (empty-tank reference)
    Codes_Matlab/GroundTruths/true{N}.mat   -- ground_truth

Samples are numbered 1-4.  The runner maps them via the config:
    samples: ["1", "2", "3", "4"]
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import scipy.io

from src.ktc_framework.loaders.ktc_loader import PluginRegistry
from src.ktc_framework.types import DataBatch


@PluginRegistry.register('TrainingDataPlugin')
class TrainingDataPlugin:
    """Loads KTC training samples from Codes_Matlab/ folder layout.

    Parameters
    ----------
    dataset_root : str
        Path to the folder that contains TrainingData/ and GroundTruths/.
        Typically ``Codes_Matlab/``.
    """

    def __init__(self, dataset_root: str = "Codes_Matlab") -> None:
        self.root = Path(dataset_root)

    def load_sample(self, level: int, sample: str) -> DataBatch:
        """Load one training sample with its reference voltages and Mpat.

        The reference voltages (``Uelref``) and measurement pattern
        (``Mpat``) live in ``TrainingData/ref.mat``, shared across all
        training samples.  Loading them here populates the batch so the
        reconstruction methods do not need a second .mat lookup.
        """
        data_path = self.root / "TrainingData" / f"data{sample}.mat"
        truth_path = self.root / "GroundTruths" / f"true{sample}.mat"
        ref_path = self.root / "TrainingData" / "ref.mat"

        if not data_path.exists():
            raise FileNotFoundError(f"Voltage file not found: {data_path}")
        if not truth_path.exists():
            raise FileNotFoundError(f"Ground truth file not found: {truth_path}")
        if not ref_path.exists():
            raise FileNotFoundError(
                f"Empty-tank reference not found: {ref_path}. "
                f"Linear difference reconstruction requires Uelref."
            )

        data_mat = scipy.io.loadmat(str(data_path), squeeze_me=True)
        truth_mat = scipy.io.loadmat(str(truth_path), squeeze_me=True)
        ref_mat = scipy.io.loadmat(str(ref_path), squeeze_me=True)

        voltages = np.asarray(data_mat['Uel'], dtype=np.float64)
        injection = np.asarray(data_mat['Inj'], dtype=np.float64)
        ground_truth = np.asarray(truth_mat['truth'], dtype=np.uint8)

        ref_voltages = np.asarray(ref_mat['Uelref'], dtype=np.float64).ravel()
        mpat = np.asarray(ref_mat['Mpat'], dtype=np.float64)

        return DataBatch(
            voltages=voltages,
            injection_patterns=injection,
            ground_truth=ground_truth,
            level=level,
            sample_id=f"training_{sample}",
            reference_voltages=ref_voltages,
            measurement_patterns=mpat,
        )
