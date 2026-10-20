"""Request/response schemas for the heart disease prediction API."""
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: float = Field(..., description="Age in years")
    sex: float = Field(..., ge=0, le=1, description="1 = male, 0 = female")
    cp: float = Field(..., description="Chest pain type (1-4)")
    trestbps: float = Field(..., description="Resting blood pressure")
    chol: float = Field(..., description="Serum cholesterol")
    fbs: float = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dl")
    restecg: float = Field(..., description="Resting ECG results (0-2)")
    thalach: float = Field(..., description="Max heart rate achieved")
    exang: float = Field(..., ge=0, le=1, description="Exercise induced angina")
    oldpeak: float = Field(..., description="ST depression induced by exercise")
    slope: float = Field(..., description="Slope of peak exercise ST segment (1-3)")
    ca: float = Field(..., description="Number of major vessels colored by fluoroscopy (0-3)")
    thal: float = Field(..., description="Thalassemia (3, 6, or 7)")


class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0 = no heart disease, 1 = heart disease")
    confidence: float = Field(..., description="Model confidence in the predicted class")
