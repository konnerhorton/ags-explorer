import math

import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def rqd_by_depth(ags):
    df = ags.rqd_table()
    fig = px.scatter(
        df,
        x="CORE_RQD",
        y="Elevation Mid",
    ).update(
        layout=dict(
            xaxis=dict(title="RQD"),
            yaxis=dict(title="Elevation, ft"),
        )
    )
    return fig


def spt_histogram(ags, elevation=None):

    df = ags.spt_table()
    if elevation:
        df["Below Elevation"] = df["Top Elevation"] < elevation
    else:
        df["Below Elevation"] = True
    fig = px.histogram(
        df.sort_values("Category"),
        x="Category",
        y="ISPT_NVAL",
        color="Below Elevation",
        histnorm="percent",
        barmode="group",
    ).update(layout=dict(xaxis=dict(title="N"), yaxis=dict(title="Frequency")))

    if elevation:
        fig.update(layout=dict(showlegend=True))
    else:
        fig.update(layout=dict(showlegend=False))
    return fig


def spt_by_depth(ags):
    df = ags.spt_table()
    fig = px.scatter(df, x="ISPT_NVAL", y="Top Elevation", color="GEOL_LEG").update(
        layout=dict(
            xaxis=dict(title="N"),
            yaxis=dict(title="Elevation, ft"),
        )
    )

    return fig


def empty_grain_size_distribution_detail() -> object:
    """
    Plots a Grain Size Distribution curve plot.

    Parameters
    ----------
    None

    Returns
    -------
    fig
        Plotly fig object
    """
    x_max = 2  # log scale
    x_min = -3  # log scale

    fig = go.Figure()
    fig.update_layout(
        height=612,
        width=792,
        margin=dict(l=40, r=20, t=20, b=40),
        plot_bgcolor="white",
        legend=dict(yanchor="bottom", xanchor="right", y=0.4, x=1),
    )
    axes_update = dict(
        color="black",
        linewidth=1,
        linecolor="black",
        mirror=True,
        gridwidth=1,
        gridcolor="black",
        minor=dict(showgrid=True, gridcolor="black", gridwidth=1),
    )

    fig.update_xaxes(
        axes_update, range=[x_min, x_max], title="<b>Particle Size, mm</b>", type="log"
    )
    fig.update_yaxes(
        axes_update,
        range=[0, 120],
        title="<b>Percentage Passing, %</b>",
        tickvals=np.arange(0, 110, 10),
    )

    lines_linear = [
        ("Gravel", 100),
        ("Sand", 4.75),
        ("Silt", 0.075),
        ("Clay", 0.002),
    ]

    lines = {}

    for index, line in enumerate(lines_linear):
        key = line[0]
        linear_x = line[1]
        if index == 0:
            next = lines_linear[index + 1][1]
            text_log_x = (math.log10(next) + x_max) / 2

        elif index == len(lines_linear) - 1:
            text_log_x = (math.log10(line[1]) + x_min) / 2

        else:
            current = line[1]
            next = lines_linear[index + 1][1]
            text_log_x = (math.log10(current) + math.log10(next)) / 2

        lines[key] = {"linear_x": linear_x, "text_log_x": text_log_x}

    fig.add_hrect(
        y0=100, y1=110, line_width=3, fillcolor="white", line_color="white", opacity=1
    )
    fig.add_hrect(
        y0=110, y1=120, line_width=1, fillcolor="white", line_color="black", opacity=1
    )
    fig.add_hline(y=100, line_width=1, line_color="black")

    for k, v in lines.items():
        if k != "Gravel":
            fig.add_shape(
                type="line",
                x0=v["linear_x"],
                x1=v["linear_x"],
                y0=110,
                y1=120,
                line_width=1,
            )

        if k in ["Sand", "Gravel"]:
            y = 117.5
        else:
            y = 115
        fig.add_annotation(text=k, showarrow=False, x=v["text_log_x"], y=y)

    fig.add_shape(
        type="line",
        x0=lines["Silt"]["linear_x"],
        x1=lines["Sand"]["linear_x"],
        y1=115,
        y0=115,
        line_width=1,
        line_color="black",
    )
    fig.add_shape(
        type="line",
        x0=lines["Sand"]["linear_x"],
        x1=lines["Gravel"]["linear_x"],
        y1=115,
        y0=115,
        line_width=1,
        line_color="black",
    )

    fig.add_shape(
        type="line",
        x0=lines["Sand"]["linear_x"],
        x1=lines["Gravel"]["linear_x"],
        y1=115,
        y0=115,
        line_width=1,
        line_color="black",
    )

    fig.add_shape(
        type="line",
        x0=0.475,
        x1=0.475,
        y1=110,
        y0=115,
        line_width=1,
        line_color="black",
    )

    fig.add_shape(
        type="line",
        x0=2,
        x1=2,
        y1=110,
        y0=115,
        line_width=1,
        line_color="black",
    )

    fig.add_shape(
        type="line",
        x0=20,
        x1=20,
        y1=110,
        y0=115,
        line_width=1,
        line_color="black",
    )

    # sand
    fig.add_annotation(text="Fine", showarrow=False, x=-0.8, y=112.5)
    fig.add_annotation(text="Medium", showarrow=False, x=0, y=112.5)
    fig.add_annotation(text="Coarse", showarrow=False, x=0.5, y=112.5)

    # gravel
    fig.add_annotation(text="Fine", showarrow=False, x=1, y=112.5)
    fig.add_annotation(text="Coarse", showarrow=False, x=1.65, y=112.5)

    # add sieve numbers
    sieve_numbers = [
        ("1&mu;m", 0.001),
        ("3&mu;m", 0.003),
        ("5&mu;m", 0.005),
        ("10&mu;m", 0.01),
        ("30&mu;m", 0.03),
        ("50&mu;m", 0.05),
        ("#200<br>75&mu;m", 0.075),
        ("#100", 0.15),
        ("#50", 0.3),
        ("#16", 1.18),
        ("#8", 2.36),
        ("#4", 4.75),
        ('3/8"', 9.5),
        ('1/2"', 12.5),
        ('1"', 25),
        ('1.5"', 37.5),
    ]
    for s in sieve_numbers:
        fig.add_annotation(
            text=s[0],
            y=103,
            x=math.log10(s[1]),
            showarrow=False,
            font=dict(color="black", size=8),
        )

    return fig


def plot_grain_size_distribution_detail(df, sample_ids):
    df = df[(df["Sample ID"].isin(sample_ids))]

    fig = plot_empty_grain_size_distribution_detail()
    for sample in sample_ids:
        dfx = df[df["Sample ID"] == sample]
        x = dfx["Particle Size"].sort_values()
        y = dfx["Percentage Passing"].sort_values()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=sample))
    return fig


def plot_empty_uscs_plot() -> object:
    """
    Plots an empty USCS plot showing boundary lines (A-Line, U-Line, B-Line)

    :return fig: fig, plotly figure showing the USCS plotting space
    """

    def a_line():
        x = np.arange(4, 100, 0.01)
        ll_limit = 4 / 0.73 + 20
        y = np.piecewise(
            x, [x < ll_limit, x >= ll_limit], [4, lambda x: 0.73 * (x - 20)]
        )
        return x, y

    def u_line():
        x = np.arange(16, 100, 0.01)
        y = 0.9 * (x - 8)
        return x, y

    def limit_line():
        x = np.arange(0, 100, 0.01)
        y = x
        return x, y

    def dual_symbol_line():
        x_max = 7 / 0.73 + 20
        x = np.arange(7, x_max, 0.01)
        y = [7 for i in x]
        return x, y

    def high_ll_line():
        y = np.arange(0, 61, 1)
        x = [50 for i in y]
        return x, y

    def a_line_dict():
        return dict(zip(a_line))

    fig = go.Figure()
    fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=40, b=40))

    axes_style = {
        "linecolor": "black",
        "linewidth": 2,
        "mirror": True,
        "showgrid": True,
        "gridcolor": "gray",
        "tickmode": "linear",
        "tick0": 0,
        "dtick": 10,
    }
    fig.update_xaxes(
        axes_style, title="Liquid Limit, %", range=[0, 100], constrain="domain"
    )
    fig.update_yaxes(
        axes_style,
        title="Plasticity Index",
        range=[0, 60],
        scaleanchor="x",
        scaleratio=1,
        constrain="domain",
    )

    plot_lines = {
        "A-Line": {"Function": a_line, "Color": "black", "Dash": None},
        "U-Line": {"Function": u_line, "Color": "black", "Dash": "dash"},
        "Limit Line": {"Function": limit_line, "Color": "black", "Dash": None},
        "Dual Symbol": {
            "Function": dual_symbol_line,
            "Color": "black",
            "Dash": None,
        },
        "High LL": {"Function": high_ll_line, "Color": "black", "Dash": None},
    }

    for k, v in plot_lines.items():
        x = v["Function"]()[0]
        y = v["Function"]()[1]
        color = v["Color"]
        dash = v["Dash"]
        fig.add_trace(
            go.Scatter(
                x=x, y=y, name=k, line=dict(dash=dash, color=color), showlegend=False
            )
        )

    annotations = [
        dict(text="<b>CL-ML</b>", x=15, y=5.5, textangle=0, showarrow=False),
        dict(text="<b>ML or OL</b>", x=42, y=5.5, textangle=0, showarrow=False),
        dict(text="<b>CL or OL</b>", x=30, y=13, textangle=0, showarrow=False),
        dict(text="<b>CH or OH</b>", x=68, y=44, textangle=0, showarrow=False),
        dict(text="<b>OH or MH</b>", x=72, y=23, textangle=0, showarrow=False),
        dict(
            text="A-Line",
            x=65,
            y=35,
            textangle=math.degrees(math.atan(-0.73)),
            showarrow=False,
        ),
        dict(
            text="U-Line",
            x=35,
            y=26,
            textangle=math.degrees(math.atan(-0.9)),
            showarrow=False,
        ),
    ]

    fig.update_layout(annotations=annotations, margin=dict(l=40, r=20, t=20, b=40))
    return fig
