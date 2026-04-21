from pandas import DataFrame

from .steps_config import STEPS_CONFIG
from .variables import *
from utils.loading_img import load_img
from utils.story_section import (
    get_steps_number as base_get_steps_number,
    make_text_steps as base_make_text_steps,
    make_graph_panels,
    make_section_layout,
)


def get_steps_number():
    return base_get_steps_number(STEPS_CONFIG)


def make_text_steps(start_index: int = 1):
    return base_make_text_steps(STEPS_CONFIG, "jitter-step", start_index)


def make_section(df: DataFrame, start_index: int = 1):
    steps = make_text_steps(start_index)
    graph_panels = make_graph_panels(STEPS_CONFIG, "jitter", load_img, start_index)

    return make_section_layout(
        steps=steps,
        graph_panels=graph_panels,
        section_id="section-jitter",
        section_class="jitter-section",
        data_section="jitter",
        panel_class="jitter-panel",
    )