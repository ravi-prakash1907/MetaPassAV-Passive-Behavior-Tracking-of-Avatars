import pandas as pd
# import numpy as np
from scripts.AvatarFeatureEngineer import AvatarFeatureEngineer
from scripts.AvatarVisualizer import AvatarVisualizer
from typing import Union


class AvatarExperiment:
    """
    Single entry point for VR avatar behavioral analysis.

    Responsibilities:
    - Hold raw data
    - Perform feature engineering
    - Expose visualization utilities
    """

    def __init__(
        self,
        df: pd.DataFrame,
        session_col="SessionID",
        time_col="StartTime",
        coord_cols=("HeadX", "HeadY", "HeadZ")
    ):
        # Raw data (immutable reference)
        self.raw_df = df.copy()

        # Feature engineering
        self.feature_engineer = AvatarFeatureEngineer(
            self.raw_df,
            session_col=session_col,
            time_col=time_col,
            coord_cols=coord_cols
        )
        self.df_features = self.feature_engineer.transform()

    # ---------- accessors ----------

    def get_features(self) -> pd.DataFrame:
        """Return full feature-engineered dataframe"""
        return self.df_features.copy()

    def get_raw(self) -> pd.DataFrame:
        """Return raw dataframe"""
        return self.raw_df.copy()

    # ---------- visualizers ----------

    def get_visualizer(
        self,
        user_id: Union[str, None] = None,
        session_id: Union[int, None] = None,
        image_name: Union[str, None] = None
    ) -> AvatarVisualizer:
        """
        Returns a visualization helper operating on
        the FEATURE-ENGINEERED dataframe.
        """
        return AvatarVisualizer(
            self.df_features,
            user_id=user_id,
            session_id=session_id,
            image_name=image_name
        )