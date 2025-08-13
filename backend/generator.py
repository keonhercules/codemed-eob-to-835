import datetime as dt


def _isa(num:int)->str:
    return f"ISA*00*          *00*          *ZZ*PAYERID       *ZZ*123456789      *{dt.date.today():%y%m%d}*{dt.datetime.utcnow():%H%M}*^*00501*{num:09d}*1*T*:~"


def generate_835(eob:dict, control:int=905)->str:
    segs=[_isa(control),
          f"GS*HP*PAYERID*123456789*{dt.date.today():%Y%m%d}*{dt.datetime.utcnow():%H%M}*1*X*005010X221A1~",
          "ST*835*0001~",
          f"BPR*{eob['payment'].get('handling','I')}*{eob['payment']['amount']:.2f}*C*{eob['payment']['method']}*P*NON~",
          f"TRN*1*{eob['payment']['trace_number']}~",
          f"DTM*405*{eob['payment']['date'].replace('-','')}~",
          f"N1*PR*{eob['payer']['name']}~"]
    if eob['payer'].get('id'):
        segs.append(f"REF*{eob['payer'].get('id_type','2U')}*{eob['payer']['id']}~")
    segs += [
        f"N1*PE*{eob['payee']['name']}~",
        f"N3*{eob['payee'].get('address','')}~",
        f"N4*{eob['payee'].get('city','')}*{eob['payee'].get('state','')}*{eob['payee'].get('zip','')}~"
    ]
    if eob['payee'].get('tax_id'):
        segs.append(f"REF*TJ*{eob['payee']['tax_id'].replace('-','')}~")
    if eob['payee'].get('npi'):
        segs.append(f"REF*XX*{eob['payee']['npi']}~")
    lx=1
    for c in eob.get('claims',[]):
        segs += [f"LX*{lx}~"]
        lx+=1
        segs += [
            f"CLP*{c['patient_control_number']}*{c.get('claim_status_code','1')}*{c['total_charge']:.2f}*{c['payment_amount']:.2f}*{c['patient_responsibility']:.2f}*{c.get('payer_claim_control_number','')}*{c.get('filing_indicator_code','12')}*11*1~",
            f"REF*6R*{c['patient_control_number']}~"
        ]
        if c.get('service_from'):
            segs.append(f"DTM*232*{c['service_from'].replace('-','')}~")
        if c.get('service_to'):
            segs.append(f"DTM*233*{c['service_to'].replace('-','')}~")
        for ln in c.get('lines',[]):
            comp=f"HC:{ln['code']}" + (f":{ln['modifier']}" if ln.get('modifier') else "")
            segs += [
                f"SVC*{comp}*{ln['charge']:.2f}*{ln['paid']:.2f}**{int(ln['units'])}~",
                f"DTM*472*{ln['service_date'].replace('-','')}~"
            ]
            for adj in ln.get('adjustments',[]):
                segs.append(f"CAS*{adj['group']}*{adj['reason_code']}*{adj['amount']:.2f}~")
            if ln.get('allowed') is not None:
                segs.append(f"AMT*B6*{ln['allowed']:.2f}~")
    for p in eob.get('plb', []):
        segs.append(f"PLB*{eob['payee'].get('tax_id','')}*{p['fiscal_period']}*{p['reason_qualifier']}:{p['reference']}*{p['amount']:.2f}~")
    body=segs[2:]
    segs += [
        f"SE*{len(body)}*0001~",
        "GE*1*1~",
        f"IEA*1*{control:09d}~"
    ]
    return "\n".join(segs)
