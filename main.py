from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
from pathlib import Path
import json
import uuid
import os

app = FastAPI()

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Инициализация шаблонов
templates = Jinja2Templates(directory="templates")

# Модели Pydantic
class Employee(BaseModel):
    name: str
    department: str
    total_days: int

class Vacation(BaseModel):
    start: date
    end: date
    employee_id: str
    status: str = "pending"
    submitted_at: str = datetime.now().isoformat()
    manager_comment: Optional[str] = None
    processed_at: Optional[str] = None

class Department(BaseModel):
    manager: str
    max_concurrent: int

# Файлы для хранения данных
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

EMPLOYEES_FILE = DATA_DIR / "employees.json"
VACATIONS_FILE = DATA_DIR / "vacations.json"
DEPARTMENTS_FILE = DATA_DIR / "departments.json"

# Загрузка и сохранение данных
def load_data(filename: Path) -> Dict:
    if filename.exists():
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_data(data: Dict, filename: Path):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Инициализация тестовых данных
def init_test_data():
    if not EMPLOYEES_FILE.exists():
        employees = {
            "1": {"name": "Иванов Иван", "department": "IT", "total_days": 28},
            "2": {"name": "Петров Петр", "department": "IT", "total_days": 28},
            "3": {"name": "Сидорова Анна", "department": "HR", "total_days": 28}
        }
        save_data(employees, EMPLOYEES_FILE)
    
    if not DEPARTMENTS_FILE.exists():
        departments = {
            "IT": {"manager": "manager1", "max_concurrent": 1},
            "HR": {"manager": "manager2", "max_concurrent": 1}
        }
        save_data(departments, DEPARTMENTS_FILE)
    
    if not VACATIONS_FILE.exists():
        save_data({}, VACATIONS_FILE)

init_test_data()

# Вспомогательные функции
def date_range(start: date, end: date) -> List[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]

def check_vacation_overlap(new_vacation: Vacation, existing_vacations: List[Vacation]) -> bool:
    for vac in existing_vacations:
        if not (new_vacation.end < vac.start or new_vacation.start > vac.end):
            return True
    return False

def check_14_days_rule(vacation_periods: List[Vacation]) -> bool:
    return any((vac.end - vac.start).days + 1 >= 14 for vac in vacation_periods)

def get_remaining_days(employee_id: str, vacations: Dict[str, Vacation]) -> int:
    employee = load_data(EMPLOYEES_FILE).get(employee_id)
    if not employee:
        return 0
    
    used_days = 0
    for vac in vacations.values():
        if vac["employee_id"] == employee_id:
            start = datetime.strptime(vac["start"], "%Y-%m-%d").date()
            end = datetime.strptime(vac["end"], "%Y-%m-%d").date()
            used_days += (end - start).days + 1
    
    return employee["total_days"] - used_days

# Роуты FastAPI
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    employee_id = form_data.get("employee_id")
    
    employees = load_data(EMPLOYEES_FILE)
    if employee_id in employees:
        return RedirectResponse(f"/employee/{employee_id}", status_code=status.HTTP_303_SEE_OTHER)
    
    raise HTTPException(status_code=400, detail="Сотрудник не найден")

@app.get("/employee/{employee_id}", response_class=HTMLResponse)
async def employee_dashboard(request: Request, employee_id: str):
    employees = load_data(EMPLOYEES_FILE)
    vacations = load_data(VACATIONS_FILE)
    departments = load_data(DEPARTMENTS_FILE)
    
    employee = employees.get(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    
    department = employee["department"]
    dept_vacations = [
        Vacation(**v) for v in vacations.values() 
        if (v["employee_id"] == employee_id or 
            (employees[v["employee_id"]]["department"] == department and v["status"] == "approved"))
    ]
    
    employee_vacations = [Vacation(**v) for v in vacations.values() if v["employee_id"] == employee_id]
    remaining_days = get_remaining_days(employee_id, vacations)
    
    return templates.TemplateResponse(
        "employee_dashboard.html",
        {
            "request": request,
            "employee": employee,
            "vacations": employee_vacations,
            "dept_vacations": [v for v in dept_vacations if v.status == "approved"],
            "remaining_days": remaining_days,
            "departments": departments,
            "now": datetime.now().date()
        }
    )

@app.post("/employee/{employee_id}/request_vacation")
async def request_vacation(request: Request, employee_id: str):
    form_data = await request.form()
    start_date = form_data.get("start_date")
    end_date = form_data.get("end_date")
    
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный формат даты. Используйте ГГГГ-ММ-ДД")
    
    if end < start:
        raise HTTPException(status_code=400, detail="Дата окончания должна быть после даты начала")
    
    employees = load_data(EMPLOYEES_FILE)
    vacations = load_data(VACATIONS_FILE)
    
    employee = employees.get(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    
    remaining_days = get_remaining_days(employee_id, vacations)
    duration = (end - start).days + 1
    
    if duration > remaining_days:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточно дней отпуска. Осталось: {remaining_days}"
        )
    
    new_vacation = Vacation(
        start=start,
        end=end,
        employee_id=employee_id
    )
    
    # Проверка на 14 дней (если это единственный период)
    employee_vacations = [Vacation(**v) for v in vacations.values() if v["employee_id"] == employee_id]
    if not employee_vacations and duration < 14:
        raise HTTPException(
            status_code=400,
            detail="Хотя бы одна часть отпуска должна быть 14 дней или более"
        )
    
    # Проверка пересечений с другими утвержденными отпусками в отделе
    approved_vacations = [
        Vacation(**v) for v in vacations.values() 
        if employees[v["employee_id"]]["department"] == employee["department"] and v["status"] == "approved"
    ]
    
    if check_vacation_overlap(new_vacation, approved_vacations):
        new_vacation.status = "conflict"
    
    # Сохраняем новый отпуск
    vacation_id = str(uuid.uuid4())
    vacations[vacation_id] = new_vacation.dict()
    save_data(vacations, VACATIONS_FILE)
    
    return RedirectResponse(f"/employee/{employee_id}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/manager/{manager_id}", response_class=HTMLResponse)
async def manager_dashboard(request: Request, manager_id: str):
    departments = load_data(DEPARTMENTS_FILE)
    employees = load_data(EMPLOYEES_FILE)
    vacations = load_data(VACATIONS_FILE)
    
    # Находим отделы, которыми управляет этот менеджер
    managed_depts = [dept for dept, info in departments.items() if info["manager"] == manager_id]
    
    if not managed_depts:
        raise HTTPException(
            status_code=403,
            detail="Вы не являетесь руководителем какого-либо отдела"
        )
    
    # Собираем все отпуска в этих отделах
    dept_vacations = []
    for vac_id, vac in vacations.items():
        emp = employees.get(vac["employee_id"])
        if emp and emp["department"] in managed_depts:
            dept_vacations.append({
                "id": vac_id,
                **vac,
                "employee_name": emp["name"],
                "department": emp["department"]
            })
    
    # Группируем по статусам
    pending_vacations = [v for v in dept_vacations if v["status"] == "pending"]
    conflict_vacations = [v for v in dept_vacations if v["status"] == "conflict"]
    approved_vacations = [v for v in dept_vacations if v["status"] == "approved"]
    
    return templates.TemplateResponse(
        "manager_dashboard.html",
        {
            "request": request,
            "pending_vacations": pending_vacations,
            "conflict_vacations": conflict_vacations,
            "approved_vacations": approved_vacations,
            "departments": managed_depts,
            "manager_id": manager_id
        }
    )

@app.post("/manager/action/{vacation_id}")
async def manager_action(vacation_id: str, request: Request):
    form_data = await request.form()
    action = form_data.get("action")
    comment = form_data.get("comment", "")
    manager_id = form_data.get("manager_id")
    
    vacations = load_data(VACATIONS_FILE)
    vacation = vacations.get(vacation_id)
    
    if not vacation:
        raise HTTPException(status_code=404, detail="Запрос на отпуск не найден")
    
    if action == "approve":
        vacation["status"] = "approved"
    elif action == "reject":
        vacation["status"] = "rejected"
    else:
        raise HTTPException(status_code=400, detail="Некорректное действие")
    
    vacation["manager_comment"] = comment
    vacation["processed_at"] = datetime.now().isoformat()
    
    save_data(vacations, VACATIONS_FILE)
    
    return RedirectResponse(f"/manager/{manager_id}", status_code=status.HTTP_303_SEE_OTHER)