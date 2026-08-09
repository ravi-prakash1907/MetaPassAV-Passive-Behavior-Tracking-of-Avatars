import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Union

class AvatarVisualizer:
    """
    Visualization utilities for VR avatar / user behavioral data.
    Designed for exploratory analysis BEFORE cleaning or normalization.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        user_id: Union[str, None] = None,
        session_id: Union[int, None] = None,
        image_name: Union[str, None] = None,
    ):
        self.df = df.copy()

        self.user_id = user_id or df["UserID"].iloc[0]
        self.session_id = session_id
        self.image_name = image_name

        self._filter_data()

    # ---------- filtering ----------

    def _filter_data(self):
        data = self.df[self.df["UserID"] == self.user_id]

        if self.session_id is not None:
            data = data[data["SessionID"] == self.session_id]

        if self.image_name is not None:
            data = data[data["ImageName"] == self.image_name]

        self.data = data.sort_values("StartTime")

    # ---------- helpers ----------

    def _require_cols(self, *cols):
        missing = [c for c in cols if c not in self.data.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    # ---------- trajectory & spatial ----------

    def plot_trajectory_xz(self):
        """Top-down (X–Z) trajectory"""
        self._require_cols("HeadX", "HeadZ")

        plt.figure()
        plt.plot(self.data["HeadX"], self.data["HeadZ"], "-o", markersize=2)
        plt.xlabel("HeadX")
        plt.ylabel("HeadZ")
        plt.title("Top-Down Trajectory (X–Z)")
        plt.axis("equal")
        plt.show()

    def plot_distance_progress(self):
        """Distance from start and cumulative distance"""
        self._require_cols("DistanceFromStart", "DistanceSoFar")

        plt.figure()
        plt.plot(self.data["StartTime"], self.data["DistanceFromStart"], label="From Start")
        plt.plot(self.data["StartTime"], self.data["DistanceSoFar"], label="So Far")
        plt.xlabel("Time")
        plt.ylabel("Distance")
        plt.title("Distance Progression")
        plt.legend()
        plt.show()

    # ---------- temporal ----------

    def plot_dwell_time(self):
        """Total time spent per image"""
        self._require_cols("ImageName", "TotalTimeSpent")

        dwell = (
            self.data
            .groupby("ImageName")["TotalTimeSpent"]
            .mean()
            .sort_values()
        )

        plt.figure(figsize=(8, 4))
        dwell.plot(kind="bar")
        plt.ylabel("Mean Dwell Time")
        plt.title("Dwell Time per Image")
        plt.show()

    # ---------- kinematic ----------

    def plot_velocity_acceleration(self):
        self._require_cols("LinVelocity", "LinAcceleration")

        plt.figure()
        plt.plot(self.data["StartTime"], self.data["LinVelocity"], label="Velocity")
        plt.plot(self.data["StartTime"], self.data["LinAcceleration"], label="Acceleration")
        plt.xlabel("Time")
        plt.title("Velocity & Acceleration")
        plt.legend()
        plt.show()

    def plot_jerk_snap(self):
        self._require_cols("Jerk", "Snap")

        plt.figure()
        plt.plot(self.data["StartTime"], self.data["Jerk"], label="Jerk")
        plt.plot(self.data["StartTime"], self.data["Snap"], label="Snap")
        plt.xlabel("Time")
        plt.title("Higher-Order Motion (Raw)")
        plt.legend()
        plt.show()

    # ---------- angular behavior ----------

    def plot_bearing(self):
        self._require_cols("bearing_azimuth", "bearing_elevation")

        plt.figure()
        plt.plot(self.data["StartTime"], self.data["bearing_azimuth"], label="Azimuth")
        plt.plot(self.data["StartTime"], self.data["bearing_elevation"], label="Elevation")
        plt.xlabel("Time")
        plt.title("Bearing Angles")
        plt.legend()
        plt.show()

    def plot_angular_dynamics(self):
        self._require_cols("AngularShift", "AngularShiftRate")

        plt.figure()
        plt.plot(self.data["StartTime"], self.data["AngularShift"], label="Angular Shift")
        plt.plot(self.data["StartTime"], self.data["AngularShiftRate"], label="Shift Rate")
        plt.xlabel("Time")
        plt.title("Angular Dynamics")
        plt.legend()
        plt.show()

    # ---------- directional ----------

    def plot_direction_sequence(self):
        """Visualize direction symbols as a time sequence"""
        self._require_cols("Direction")

        mapping = {
            "S": 0, "F": 1, "B": -1,
            "R": 2, "L": -2,
            "RF": 3, "RB": 4,
            "LF": -3, "LB": -4
        }

        y = self.data["Direction"].map(mapping)

        plt.figure(figsize=(10, 2))
        plt.scatter(self.data["StartTime"], y, s=8)
        plt.yticks(list(mapping.values()), list(mapping.keys()))
        plt.xlabel("Time")
        plt.title("Directional Behavior (Symbolic)")
        plt.show()

    # ---------- distribution diagnostics ----------

    def plot_feature_histogram(self, feature, log_scale=True):
        self._require_cols(feature)

        plt.figure()
        plt.hist(self.data[feature], bins=100)
        if log_scale:
            plt.yscale("log")
        plt.xlabel(feature)
        plt.title(f"Distribution of {feature}")
        plt.show()

    def plot_pairwise_scatter(self, x, y):
        self._require_cols(x, y)

        plt.figure()
        plt.scatter(self.data[x], self.data[y], s=5)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f"{x} vs {y}")
        plt.show()
