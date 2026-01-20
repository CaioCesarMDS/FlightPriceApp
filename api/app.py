import pandas as pd
import joblib
import zipfile
from io import BytesIO

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from src.utils.preprocessing import preprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

@app.on_event("startup")
def load_model():
    global model
    model = joblib.load("models/flight_price_model.joblib")
    print("Modelo carregado com sucesso")

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="O arquivo precisa ser .xlsx")

    contents = await file.read()

    try:
        df = pd.read_excel(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler o arquivo: {str(e)}")

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Modelo não carregado"
        )

    try:
        predictions = predict_prices(df, model)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao gerar previsões")

    df["predicted_price"] = predictions

    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    txt_buffer = BytesIO()
    txt_buffer.write("\n".join(map(str, predictions)).encode())
    txt_buffer.seek(0)

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        zip_file.writestr("predictions.txt", txt_buffer.read())
        zip_file.writestr("flightprice_com_predicoes.xlsx", excel_buffer.read())
    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=resultado.zip"}
    )

def predict_prices(test_data: pd.DataFrame, model):
    test_df = preprocess(test_data)
    test_df = test_df.reindex(
        columns=model.feature_names_in_,
        fill_value=0
    )
    return model.predict(test_df)
