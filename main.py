from fastapi import FastAPI, status, Form
from fastapi.responses import JSONResponse
from typing import List
from typing import Optional
import json

from Classes import *
from timetable.main import timetable as tt

app = FastAPI(title="Bonch Open TimeTable", version="0.8.0", description="Это апи для <a href='http://cabinet.sut.ru/raspisanie_all_new.php' target=_blank>источника</a>. если его снесут то это апи бесмысленно.")


@app.post("/tt/all", tags=["Полное расписание"], summary="Получение полного расписания", responses=errorcodes)
async def getall(year: str = Form(..., description="семестр"),
              type_z: int = Form(..., description="тип расписания"),
              facultetid: int = Form(..., description="id факультета"),
              kurs: int = Form(..., description=""),
              groupid: int = Form(..., description="")):
    """
     Получение всего расписания. Работает медленно потому-что бонч. <a href="http://cabinet.sut.ru/raspisanie_all_new.php" target=_blank>источник</a>.
    """
    t = tt()
    try:

        res = t.getTimeTable(year, type_z=str(type_z), facultetid=str(facultetid), kurs=str(kurs), groupid=str(groupid))
        try:
            if res["error"] == 404:
                return JSONResponse(status_code=res["error"], content=res)
        except TypeError:
            pass
        return JSONResponse(status_code=200, content=res)
    except:
        return JSONResponse(status_code=500)


@app.get("/tt/all", tags=["Полное расписание"], summary="Получение полного расписания", responses=errorcodes)
async def getallget(year: str = "205.2021/2",
                 type_z: int = "1",
                 facultetid: int = "50554",
                 kurs: int = "3",
                 groupid: int = "53954"):
    """
     Получение всего расписания чисто для 590
    """
    t = tt()
    try:
        res = t.getTimeTable(year=year, type_z=str(type_z), facultetid=str(facultetid), kurs=str(kurs), groupid=str(groupid))
        try:
            if res["error"] == 404:
                return JSONResponse(status_code=res["error"], content=res)
        except TypeError:
            pass
        return JSONResponse(status_code=200, content=res)
    except:
        return JSONResponse(status_code=500)


@app.get("/facultet", tags=["Факультеты"], summary="Получение списка факультетов", responses=errorcodes)
async def getfacult(year: str = "205.2021/2", type_z: int = 1):
    """
    получение списка факультетов

    """
    t = tt()
    try:
        res = t.getFacultet(type_z=int(type_z), schet=str(year))
        try:
            if res["error"] == 404:
                return JSONResponse(status_code=res["error"], content=res)
        except:
            pass
        return JSONResponse(status_code=200, content=res['facultet'])
    except:
        return JSONResponse(status_code=500)


@app.get("/course", tags=["Номер курса"], summary="Получение номеров курсов", responses=errorcodes)
async def getcourse(facultetId: int):
    """
    Получение номеров куосов. хз как должно быть но сделал как на сайте.

    """
    t = tt()
    try:
        res = t.getCourse(facultetId)
        try:
            if res["error"] == 404:
                return JSONResponse(status_code=res["error"], content=res)
        except:
            pass
        return JSONResponse(status_code=200, content=res)
    except:
        return JSONResponse(status_code=500)


@app.get("/groups", tags=["Группы"], summary="Получение номеров и наименование групп", responses=errorcodes)
async def getgroups(facultetId: int, kurs: int, type_z: int = 1, year: str = "205.2021/2"):
    """
    Получение номеров и наименование групп
    """
    t = tt()
    try:
        res = t.getGroups(facultetId, type_z, year, kurs)
        try:
            if res["error"] == 404:
                return JSONResponse(status_code=res["error"], content=res)
        except:
            pass
        return JSONResponse(status_code=200, content=res["groups"])
    except:
        return JSONResponse(status_code=500)


@app.get("/years", tags=["Семестры"], summary="Получение списка семестров", responses=errorcodes)
async def getyears():
    """
    Получение списка семестров
    """
    t = tt()
    try:
        res = t.getYears()
        try:
            if res["error"] == 404:
                return JSONResponse(status_code=res["error"], content=res)
        except:
            pass
        return JSONResponse(status_code=200, content=res["years"])
    except:
        return JSONResponse(status_code=500)


@app.get("/week/education", tags=["Неделя"], summary="Получение номера учебной недели", responses=errorcodes)
async def getweekeducation():
    """
    Получение номера учебной недели
    """
    t = tt()
    try:
        return JSONResponse(status_code=200, content={"weekEducation": t.getEdWeek()})
    except:
        return JSONResponse(status_code=500)

@app.get("/curse/today", tags=["Расписание"], summary="Получение расписания на сегодня", responses=errorcodes)
async def getCurseToday(facultetId: int, kurs: int, groupid: int, type_z: int = 1, year: str = "205.2021/2"):
    """
    Получение расписания на сегодня
    """
    t = tt()

    try:
        res = t.getToDayTimeTable(facultetid=facultetId, kurs=kurs, type_z=type_z, year=year, groupid=groupid)
        try:
            if res["error"] == 404:
                return JSONResponse(status_code=res["error"], content=res)
        except:
            pass
        return JSONResponse(status_code=200, content=res)
    except:
        return JSONResponse(status_code=500)

@app.get("/curse/forday", tags=["Расписание"], summary="Получение расписания на день недели", responses=errorcodes)
async def getCurseForday(facultetId: int, kurs: int, groupid: int, type_z: int = 1, year: str = "205.2021/2", weekDay: int = 0):
    """
    Получение расписания на определенный день недели. Понедельник - 1 ... Воскресенье - 7. 0 - на сегодня
    """
    t = tt()
    try:
        res = t.getToDayTimeTable(facultetid=facultetId, kurs=kurs, type_z=type_z, year=year, weekDay=weekDay, groupid=groupid)
        try:
            if res["error"] == 404:
                return JSONResponse(status_code=res["error"], content=res)
        except:
            pass
        return JSONResponse(status_code=200, content=res)
    except:
        return JSONResponse(status_code=500)


