import numpy as np
from scipy.interpolate import interp1d

# class Sample:
#     def __init__(
#         self,
#         id,
#         gsd_details=None,
#         gsd_general=None,
#         liquid_limit=None,
#         plastic_limit=None,
#     ):
#         self.id = id
#         self.gsd_details = gsd_details
#         self.gsd_general = gsd_general
#         self.liquid_limit = liquid_limit
#         self.plastic_limit = plastic_limit
#         self.plasticity_index = self.plastic_limit - self.liquid_limit


#     def get_gsd_general(
#         self,
#         gsd_upper_limits={"gravel": 30, "sand": 2, "silt": 0.05, "clay": 0.002},
#     ):
#         pass
def get_gsd_general(
    data,
):
    particle_size = data[:, 0]
    percentage_passing = data[:, 1]
    gravel_boundary = 4.75
    sand_boundary = 0.075
    silt_boundary = 0.002
    interpolate_percent_passing = interp1d(
        particle_size, percentage_passing, kind="linear", bounds_error=True
    )

    try:
        gravel_percent = 100 - interpolate_percent_passing(gravel_boundary)
    except:
        gravel_percent = None
    try:
        sand_percent = interpolate_percent_passing(
            gravel_boundary
        ) - interpolate_percent_passing(sand_boundary)
    except:
        sand_percent = None
    try:
        fines_percent = interpolate_percent_passing(
            sand_boundary
        ) - interpolate_percent_passing(silt_boundary)
    except:
        if sand_percent:
            if sand_percent + gravel_percent < 100:
                fines_percent = 100 - sand_percent - gravel_percent
        else:
            silt_percent = None
    try:
        clay_percent = interpolate_percent_passing(silt_boundary)
    except:
        clay_percent = None

    return {
        "Gravel": gravel_percent,
        "Sand": sand_percent,
        "Fines": fines_percent,
        # "clay": clay_percent,
    }
