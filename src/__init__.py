"""
W-5 Football Prediction Framework

A research implementation of the W-5 Multi-Agent AI Consensus Framework
for football match outcome prediction.

For more information, see:
- Research Paper: https://zenodo.org/records/17367739
- Documentation: https://github.com/yourusername/w5-football-prediction
- Commercial Product: https://winner12.com
"""

__version__ = '0.1.0'
__author__ = 'W-5 Research Team'
__license__ = 'MIT'

from src.models.baseline import BaselinePredictor, SimpleELOPredictor
from src.consensus.debate import ConsensusEngine
from src.data.loader import MatchDataLoader, load_sample_data

__all__ = [
    'BaselinePredictor',
    'SimpleELOPredictor',
    'ConsensusEngine',
    'MatchDataLoader',
    'load_sample_data'
]

