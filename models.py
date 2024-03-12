from sqlalchemy import Column, Integer, String
from database import Base


# تعریف مدل (کلاس) جدول دیتابیس
class MySchoolClasses(Base):
    __tablename__ = 'my_school_classes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    school_name = Column(String)
    teacher_name = Column(String)
    student_count = Column(Integer)
