from pydantic import BaseModel

class BiasScores(BaseModel):
    loss_aversion: dict
    overtrading: dict
    fomo: dict

class AnalysisResult(BaseModel):
    bias_scores: BiasScores
    features: dict
    cluster: int
    silhouette: float
