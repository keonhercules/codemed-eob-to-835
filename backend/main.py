from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from generator import generate_835
import datetime as dt, uuid, json

app = FastAPI()

class EOB(BaseModel):
    meta: dict
    payment: dict
    payer: dict
    payee: dict
    claims: list
    plb: list | None = None

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf","image/jpeg","image/png"]:
        raise HTTPException(400, "Unsupported file type")
    # TODO: push to GCS + Document AI; here we return a demo JSON (No-PHI)
    demo = {
      "meta":{"source_file":file.filename,"extraction_confidence":0.8,"payer_detected":"Demo","created_at":dt.datetime.utcnow().isoformat()+"Z"},
      "payment":{"amount":150.0,"date":str(dt.date.today()),"method":"CHK","handling":"I","trace_number":str(uuid.uuid4())[:12]},
      "payer":{"name":"Demo Payer","id_type":"2U","id":"99999"},
      "payee":{"name":"CODEMED CLINIC","npi":"1234567890","tax_id":"12-3456789","address":"100 Main St","city":"Dallas","state":"TX","zip":"75201"},
      "claims":[{"patient_control_number":"PCN1","payer_claim_control_number":"PCC1","claim_status_code":"1","filing_indicator_code":"12",
        "total_charge":200.0,"payment_amount":150.0,"patient_responsibility":50.0,"service_from":str(dt.date.today()),"service_to":str(dt.date.today()),
        "lines":[{"code":"99213","modifier":"25","charge":120.0,"allowed":90.0,"paid":90.0,"units":1,"service_date":str(dt.date.today()),
                  "adjustments":[{"group":"CO","reason_code":"45","amount":30.0}]},
                 {"code":"81002","charge":80.0,"allowed":60.0,"paid":60.0,"units":1,"service_date":str(dt.date.today()),
                  "adjustments":[{"group":"PR","reason_code":"1","amount":20.0}]}]}],
      "plb":[{"reason_qualifier":"WO","reference":"ADJ123","amount":-10.0,"fiscal_period":dt.date.today().strftime("%Y%m")}]
    }
    return EOB(**demo)

@app.post("/api/generate")
async def generate(eob:EOB):
    edi = generate_835(eob.model_dump())
    return {"edi": edi}
