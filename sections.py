
from graphs.scatter.callbacks import register_callbacks as register_scatter_callbacks
from graphs.scatter.template import make_section as make_scatter_section, get_steps_number as scatter_steps

from graphs.jitter.callbacks import register_callbacks as register_jitter_callbacks
from graphs.jitter.template import make_section as make_jitter_section, get_steps_number as jitter_steps

SECTIONS = [
    {"function": make_scatter_section, "n_steps": scatter_steps, "callback": register_scatter_callbacks},
    {"function": make_jitter_section, "n_steps": jitter_steps, "callback": register_jitter_callbacks},
]

DEFAULT_STEP = 1