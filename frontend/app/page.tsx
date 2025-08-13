"use client";
import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [json, setJson] = useState<any>(null);
  const [edi, setEdi] = useState<string>("");

  async function onDrop(f: File) {
    setFile(f);
    const fd = new FormData(); fd.append("file", f);
    const res = await fetch("/api/uploadProxy", { method: "POST", body: fd });
    const data = await res.json(); setJson(data);
  }

  async function onExport() {
    const res = await fetch("/api/generateProxy", {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify(json)
    });
    const data = await res.json(); setEdi(data.edi);
    const blob = new Blob([data.edi], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = "remit.835"; a.click();
  }

  return (
    <main style={{maxWidth:860,margin:"40px auto",fontFamily:"system-ui"}}>
      <h1>EOB → 835 (Demo, No-PHI)</h1>
      <div onDragOver={e=>e.preventDefault()}
           onDrop={e=>{e.preventDefault(); const f=e.dataTransfer.files?.[0]; if(f) onDrop(f);}}
           onClick={()=>document.getElementById("f")?.click()}
           style={{border:"2px dashed #999", padding:40, textAlign:"center", borderRadius:12, cursor:"pointer"}}>
        {file ? <>Selected: {file.name}</> : <>Drag & drop EOB or click to upload</>}
      </div>
      <input id="f" type="file" hidden accept=".pdf,.png,.jpg,.jpeg"
             onChange={e=>{const f=e.target.files?.[0]; if(f) onDrop(f);}} />
      {json && (<>
        <h3 style={{marginTop:24}}>Review (demo JSON)</h3>
        <pre style={{background:"#f7f7f7",padding:12,borderRadius:8, maxHeight:280, overflow:"auto"}}>
          {JSON.stringify(json, null, 2)}
        </pre>
        <button onClick={onExport} style={{padding:"10px 16px", borderRadius:8}}>Export 835</button>
      </>)}
      {edi && (<>
        <h3>Generated 835 (preview)</h3>
        <pre style={{whiteSpace:"pre-wrap",background:"#f7f7f7",padding:12,borderRadius:8}}>{edi}</pre>
      </>)}
    </main>
  );
}
