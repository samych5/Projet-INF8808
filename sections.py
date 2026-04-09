
from typing import Callable
from dash import Dash, html
from pandas import DataFrame

from graphs.scatter.template import make_section as make_scatter_section, get_steps_number as scatter_steps

from graphs.jitter.template import make_section as make_jitter_section, get_steps_number as jitter_steps

from graphs.box_plot.template import make_section as make_box_plot_steps_section, get_steps_number as box_plot_steps

from graphs.bar_chart.template import make_section as make_bar_chart_steps_section, get_steps_number as bar_chart_steps

from graphs.heat_map.callbacks import register_callbacks as register_heat_map_callbacks
from graphs.heat_map.template import make_section as make_heat_map_steps_section, get_steps_number as heat_map_steps

from graphs.bee_swarm.callbacks import register_callbacks as register_bee_swarm_callbacks
from graphs.bee_swarm.template import make_section as make_bee_swarm_steps_section, get_steps_number as bee_swarm_steps

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
    SectionParameters(make_scatter_section, scatter_steps, lambda app, df, step: None),
    SectionParameters(make_jitter_section, jitter_steps, lambda app, df, step: None),
    SectionParameters(make_box_plot_steps_section, box_plot_steps, lambda app, df, step: None),
    SectionParameters(make_heat_map_steps_section, heat_map_steps, register_heat_map_callbacks),
    SectionParameters(make_bar_chart_steps_section, bar_chart_steps, lambda app, df, step: None),
    SectionParameters(make_bee_swarm_steps_section, bee_swarm_steps, register_bee_swarm_callbacks),
]

DEFAULT_STEP = 1