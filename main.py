from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

plans = {
    "减脂": {
        "plan": "有氧+全身循环训练，每周4-5次，每次40分钟",
        "tips": "饮食上控制热量缺口，配合HIIT效果更好"
    },
    "增肌": {
        "plan": "分化训练（推/拉/腿），每周4次，每次60分钟，渐进超负荷",
        "tips": "保证蛋白质摄入，每公斤体重1.6-2g左右"
    },
    "塑形": {
        "plan": "力量训练+轻量有氧结合，每周3-4次",
        "tips": "注重动作质量，控制好节奏，不用追求大重量"
    }
}

@app.get("/")
def home():
    return {
        "app": "FitFlow",
        "message": "FitFlow is running!"
    }

@app.get("/plan")
def get_plan(goal: str = "减脂"):
    if goal in plans:
        data = plans[goal]
    else:
        data = {"error": f"暂不支持目标'{goal}'，可选：减脂、增肌、塑形"}

    if "error" not in data:
        supabase.table("workouts").insert({
            "goal": goal,
            "plan": data["plan"],
            "tips": data["tips"]
        }).execute()

    content = json.dumps(data, ensure_ascii=False)
    return JSONResponse(content=json.loads(content), media_type="application/json; charset=utf-8")

@app.get("/history")
def get_history():
    result = supabase.table("workouts").select("*").order("created_at", desc=True).execute()
    content = json.dumps(result.data, ensure_ascii=False)
    return JSONResponse(content=json.loads(content), media_type="application/json; charset=utf-8")


