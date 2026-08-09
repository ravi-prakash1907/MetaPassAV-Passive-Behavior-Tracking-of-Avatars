import numpy as np
import pandas as pd

class AvatarFeatureEngineer:
    """
    Position-only VR kinematic and angular feature engineering.
    All angular quantities are environment-relative (trajectory-based).
    """

    ORIGIN = np.array([-22.96, 0.38, -31.33])

    def __init__(
        self,
        df: pd.DataFrame,
        session_col="SessionID",
        time_col="StartTime",
        coord_cols=("HeadX", "HeadY", "HeadZ"),
        eps=1e-6
    ):
        self.df = df.copy()
        self.session_col = session_col
        self.time_col = time_col
        self.coord_cols = coord_cols
        self.eps = eps

    # ---------- helpers ----------

    def _coords(self):
        return self.df[list(self.coord_cols)].values

    def _dt(self):
        dt = (
            self.df
            .groupby(self.session_col)[self.time_col]
            .diff()
            .fillna(0.0)
            .values
        )
        dt[dt == 0] = self.eps
        return dt

    # ---------- distance features ----------

    def add_distance_from_previous(self):
        diff = (
            self.df
            .groupby(self.session_col)[list(self.coord_cols)]
            .diff()
            .fillna(0.0)
            .values
        )
        self.df["DistanceFromPrevious"] = np.linalg.norm(diff, axis=1)
        return self

    def add_distance_from_start(self):
        coords = self._coords()
        self.df["DistanceFromStart"] = np.linalg.norm(
            coords - self.ORIGIN, axis=1
        )
        return self

    def add_distance_so_far(self):
        self.df["DistanceSoFar"] = (
            self.df
            .groupby(self.session_col)["DistanceFromPrevious"]
            .cumsum()
        )
        return self

    # ---------- directional features ----------


    ######   overcomes above problem by angular direction  #######
    def add_direction_symbol(self, eps_dir=1e-4):
        """
        Adds an 8-direction + Stable categorical column based on
        angular zoning of movement direction in X–Z plane.

        Directions:
        {R, RF, F, LF, L, LB, B, RB, S}
        """

        dx = (
            self.df
            .groupby(self.session_col)["HeadX"]
            .diff()
            .fillna(0.0)
            .values
        )

        dz = (
            self.df
            .groupby(self.session_col)["HeadZ"]
            .diff()
            .fillna(0.0)
            .values
        )

        # Movement magnitude
        mag = np.sqrt(dx**2 + dz**2)

        # Initialize all as Stable
        direction = np.full(len(self.df), "S", dtype=object)

        # Mask for actual movement
        moving = mag > eps_dir

        # Compute movement angle in degrees [0, 360)
        theta = np.degrees(np.arctan2(dz[moving], dx[moving]))
        theta = (theta + 360) % 360

        # Assign zones
        dirs = np.empty(len(theta), dtype=object)

        dirs[(theta >= 337.5) | (theta < 22.5)] = "R"
        dirs[(theta >= 22.5) & (theta < 67.5)] = "RF"
        dirs[(theta >= 67.5) & (theta < 112.5)] = "F"
        dirs[(theta >= 112.5) & (theta < 157.5)] = "LF"
        dirs[(theta >= 157.5) & (theta < 202.5)] = "L"
        dirs[(theta >= 202.5) & (theta < 247.5)] = "LB"
        dirs[(theta >= 247.5) & (theta < 292.5)] = "B"
        dirs[(theta >= 292.5) & (theta < 337.5)] = "RB"

        direction[moving] = dirs
        self.df["Direction"] = direction

        return self


    # ---------- angular features ----------

    def add_bearing_from_origin(self):
        coords = self._coords()
        v = coords - self.ORIGIN

        self.df["bearing_azimuth"] = np.arctan2(v[:, 0], v[:, 2])
        self.df["bearing_elevation"] = np.arctan2(
            v[:, 1], np.linalg.norm(v[:, [0, 2]], axis=1)
        )
        return self

    def add_3d_angular_change(self):
        self.df["3DAngularChange"] = np.sqrt(
            self.df["bearing_azimuth"]**2 +
            self.df["bearing_elevation"]**2
        )
        return self

    def add_angular_shift(self):
        da = (
            self.df
            .groupby(self.session_col)["bearing_azimuth"]
            .diff()
            .fillna(0.0)
        )
        de = (
            self.df
            .groupby(self.session_col)["bearing_elevation"]
            .diff()
            .fillna(0.0)
        )
        self.df["AngularShift"] = np.sqrt(da**2 + de**2)
        return self

    # ---------- linear kinematics ----------

    def add_linear_velocity(self):
        self.df["LinVelocity"] = (
            self.df["DistanceFromPrevious"] / self._dt()
        )
        return self

    def add_linear_acceleration(self):
        self.df["LinAcceleration"] = (
            self.df
            .groupby(self.session_col)["LinVelocity"]
            .diff()
            .fillna(0.0)
            / self._dt()
        )
        return self

    def add_jerk(self):
        self.df["Jerk"] = (
            self.df
            .groupby(self.session_col)["LinAcceleration"]
            .diff()
            .fillna(0.0)
            / self._dt()
        )
        return self

    def add_snap(self):
        self.df["Snap"] = (
            self.df
            .groupby(self.session_col)["Jerk"]
            .diff()
            .fillna(0.0)
            / self._dt()
        )
        return self

    # ---------- angular dynamics ----------

    def add_angular_shift_rate(self):
        self.df["AngularShiftRate"] = (
            self.df["AngularShift"] / self._dt()
        )
        return self

    def add_angular_shift_jerk_rate(self):
        self.df["AngularShiftJerkRate"] = (
            self.df
            .groupby(self.session_col)["AngularShiftRate"]
            .diff()
            .fillna(0.0)
            / self._dt()
        )
        return self

    # ---------- pipeline ----------

    def transform(self):
        return (
            self.add_distance_from_previous()
                .add_distance_from_start()
                .add_direction_symbol()
                .add_distance_so_far()
                .add_bearing_from_origin()
                .add_3d_angular_change()
                .add_angular_shift()
                .add_linear_velocity()
                .add_linear_acceleration()
                .add_jerk()
                .add_snap()
                .add_angular_shift_rate()
                .add_angular_shift_jerk_rate()
                .df
        )
