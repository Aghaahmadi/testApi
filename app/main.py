from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
import pandas as pd

app = FastAPI()


@app.get("/")
def marketwatch():
    mw: pd.DataFrame = pd.read_pickle('../marketwatch.pkl')
    mw = mw.nlargest(20, 'ارزش بازار')
    rename_cols = {'اولین': 'open', 'بیشترین': 'high', 'کمترین': 'low', 'آخرین': 'close', 'حجم': 'volume'}
    mw = mw.rename(columns=rename_cols)
    mw = mw[rename_cols.values()]
    mw.dropna(inplace=True)
    return Response(content=mw.to_json(force_ascii=False), media_type="application/json")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
