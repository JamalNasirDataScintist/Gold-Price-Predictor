"""
Voice module for gold price predictor
"""
from .voice_listener import listen
from .voice_responder import speak

__all__ = ['listen', 'speak']
__version__ = '1.0.0'