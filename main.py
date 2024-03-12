import uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

app = FastAPI()
# ایجاد جدول در دیتابیس (فقط برای اولین اجرا)
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()


class MySchoolClasses(BaseModel):
    name: str = Field(min_lengh=1)
    school_name: str = Field(min_lengh=1, max_length=100)
    teacher_name: str = Field(min_lengh=1, max_length=100)
    student_count: int = Field(gt=1, lt=100)


@app.get("/")
def read_school_class(db: Session = Depends(get_db)):
    return db.query(models.MySchoolClasses).all()


@app.post("/")
def create_school_class(my_school_class: MySchoolClasses, db: Session = Depends(get_db)):
    school_class = models.MySchoolClasses()
    school_class.name = my_school_class.name
    school_class.school_name = my_school_class.school_name
    school_class.teacher_name = my_school_class.teacher_name
    school_class.student_count = my_school_class.student_count
    db.add(school_class)
    db.commit()
    db.refresh(school_class)


@app.put("/{schoolclass_id}")
def school_class_update(my_school_class_id: int, my_school_class: MySchoolClasses, db: Session = Depends(get_db)):
    school_class = db.query(models.MySchoolClasses).filter(models.MySchoolClasses.id == my_school_class_id).first()
    if school_class is None:
        print("The school class is not exist!")
    school_class.name = my_school_class.name
    school_class.school_name = my_school_class.school_name
    school_class.teacher_name = my_school_class.teacher_name
    school_class.student_count = my_school_class.student_count
    db.add(school_class)
    db.commit()
    db.refresh(school_class)
    return my_school_class


@app.delete("/{school_class_id}")
def delete_school_class(my_school_class_id: int, db: Session = Depends(get_db)):
    school_class = db.query(models.MySchoolClasses).filter(models.MySchoolClasses.id == my_school_class_id).first()
    if school_class is not None:
        db.query(models.MySchoolClasses).filter(models.MySchoolClasses.id == my_school_class_id).delete()
        db.commit()


@app.get("/about/{name}")
def about_faradars(name: str):
    return {"data": name}


my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@app.get("/my_list/")
def get_list():
    return {"list": my_list}


@app.post("/add/{number:int}")
def add_to_list(number: int):
    my_list.append(number)
    return my_list


@app.put("/update_list/{index:int}")
def update_list(index: int, new_number):
    my_list[index] = new_number
    return {"updated_list": my_list}


@app.delete("/delete/{number:int}")
def delete_from_list(number: int):
    my_list.remove(number)
    return my_list


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
# uvicorn main:app --reload
