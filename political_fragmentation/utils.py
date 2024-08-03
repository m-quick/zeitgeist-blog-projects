import pandas as pd
from typing import Optional, Sequence
import numpy as np


class GiniCalculator:

    def __init__(self) -> None:
        self.gini_coeff_col = "gini_coeff"

    @staticmethod
    def calculate_gini_coeff(x: list, weights: Optional[list] = None):
        if weights is None:
            weights = np.ones_like(x)
        if sum(weights) == 0:
            return 0
        weights_relative = [w / sum(weights) for w in weights]
        count = np.multiply.outer(weights_relative, weights_relative)
        mad = np.abs(np.subtract.outer(x, x) * count).sum() / count.sum()
        rmad = mad / np.average(x, weights=weights_relative)
        return 0.5 * rmad

    def gini_coeff_by_candidate(
        self,
        election_results_df: pd.DataFrame,
        election_year_col: str = "election_year",
        candidates_col: str = "candidate",
        votes_total_col: str = "votes_total",
        votes_pct_col: str = "votes_pct",
    ) -> pd.DataFrame:

        elections: Sequence[int] = election_results_df[election_year_col].unique()
        candidate_gini_scores = []

        for election in elections:
            candidates: Sequence[str] = election_results_df.loc[
                election_results_df[election_year_col] == election, candidates_col
            ].unique()
            for candidate in candidates:
                filter_condition = (
                    election_results_df[candidates_col] == candidate
                ) & (election_results_df[election_year_col] == election)
                vote_pct = election_results_df.loc[
                    filter_condition, votes_pct_col
                ].to_list()
                votes = election_results_df.loc[
                    filter_condition, votes_total_col
                ].to_list()
                gini_score = self.calculate_gini_coeff(vote_pct, votes)
                candidate_gini_scores.append(
                    {
                        election_year_col: election,
                        candidates_col: candidate,
                        self.gini_coeff_col: gini_score,
                        votes_total_col: sum(votes),
                    }
                )

        return pd.DataFrame(candidate_gini_scores)

    def gini_coeff_by_election(
        self,
        candidate_gini_scores_df: pd.DataFrame,
        group_by_cols: list[str] = ["election_year"],
        votes_total_col: str = "votes_total",
    ) -> pd.DataFrame:
        wm = lambda x: np.average(
            x, weights=candidate_gini_scores_df.loc[x.index, votes_total_col]
        )
        gini_by_election_df = (
            candidate_gini_scores_df.dropna(subset=[self.gini_coeff_col])
            .groupby(group_by_cols, as_index=False)
            .agg(gini_coeff=(self.gini_coeff_col, wm))
        )
        return gini_by_election_df
