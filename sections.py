
from typing import Callable
from dash import Dash, html
from pandas import DataFrame

from graphs.scatter.callbacks import register_callbacks as register_scatter_callbacks
from graphs.scatter.template import make_section as make_scatter_section, get_steps_number as scatter_steps

from graphs.jitter.callbacks import register_callbacks as register_jitter_callbacks
from graphs.jitter.template import make_section as make_jitter_section, get_steps_number as jitter_steps

class SectionParameters:
    def __init__(
        self,
        construction_function : Callable[[DataFrame, int], html.Section],
        n_steps : Callable[[], int],
        callback: Callable[[Dash,DataFrame,int], None]
    ):
        self.construction_function = construction_function
        self.get_steps_number = n_steps
        self.callback = callback

SECTIONS = [
    SectionParameters(make_scatter_section, scatter_steps, register_scatter_callbacks),
    SectionParameters(make_jitter_section, jitter_steps, register_jitter_callbacks),
]

DEFAULT_STEP = 1