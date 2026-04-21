from dash import html


def get_steps_number(steps_config):
    return len(steps_config)


def make_text_steps(steps_config, step_class: str, start_index: int = 1):
    return [
        html.Div(
            className=f"story-step {step_class}",
            **{"data-step": str(step_index)},
            children=[
                html.Div(
                    className="text-card",
                    children=[
                        html.H3(step_config.title, className="text-card-title"),
                        html.P(step_config.text, className="text-card-paragraph")
                        if isinstance(step_config.text, str)
                        else step_config.text,
                    ],
                )
            ],
        )
        for step_index, step_config in enumerate(steps_config, start=start_index)
    ]


def make_graph_panels(steps_config, image_prefix: str, load_img, start_index: int = 1):
    return [
        html.Div(
            className="section-graph-frame active" if i == 0 else "section-graph-frame",
            **{"data-step": str(start_index + i)},
            children=[
                html.Img(
                    src=load_img(image_prefix, i),
                    style={
                        "width": "100%",
                        "height": "100%",
                        "objectFit": "contain",
                    },
                )
            ],
        )
        for i in range(len(steps_config))
    ]


def make_section_layout(
    *,
    steps,
    graph_panels,
    section_id: str,
    section_class: str,
    data_section: str,
    panel_class: str,
):
    return html.Section(
        id=section_id,
        className=f"story-section {section_class}",
        **{"data-section": data_section},
        children=[
            html.Div(
                className="story-text-column",
                children=steps,
            ),
            html.Div(
                className="story-graph-column",
                children=[
                    html.Div(
                        className="story-graph-sticky",
                        children=[
                            html.Div(
                                className=f"graph-panel {panel_class}",
                                children=[
                                    html.Div(
                                        className="graph-panel-inner section-graph-stack",
                                        children=graph_panels,
                                    )
                                ],
                            )
                        ],
                    )
                ],
            ),
        ],
    )