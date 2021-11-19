import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from slr_backend_only import main

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def root(request: Request, q: str = None):
    if q is None:
        return templates.TemplateResponse("index.html", {"request": request, "data": {"success": True, "ans": False}})
    productions = q.split("\n")
    productions = [p.replace('\r', '') for p in productions]
    try:
        ff, terminals, non_terminals, table = main(productions)
    except Exception:
        return templates.TemplateResponse("index.html", {"request": request, "data": {"success": False}})
    header = ["State"] + terminals + ["$"] + non_terminals
    _table = [header]
    _idx = {}
    for i, sym in enumerate(header):
        _idx[sym] = i

    sr, rr = {"is": False, "count": 0}, {"is": False, "count": 0}
    for state in table:
        temp = [""]*len(header)
        temp[0] = state
        for d in table[state].items():
            if type(d[1]) is not str:
                temp[_idx[d[0]]] = ", ".join(list(d[1]))
                con = "".join([ch for ch in temp[_idx[d[0]]] if ch in ['s', 'r']])
                if con == 'rr':
                    rr["is"] = True
                    rr["count"] += 1
                elif con == 'sr' or con == 'rs':
                    sr["is"] = True
                    sr["count"] += 1
            else:
                temp[_idx[d[0]]] = d[1]
        _table.append(temp)

    data = {
        "success": True,
        "ans": True,
        "terminals": terminals,
        "non-terminals": non_terminals,
        "ff": ff,
        "table": _table,
        "sr": sr,
        "rr": rr,
        "is_slr": not sr["is"] and not rr["is"],
        "productions": productions,
    }
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
