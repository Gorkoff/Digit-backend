from datetime import datetime

from pydantic import BaseModel, validator


class Body(BaseModel):
    start_date: str
    end_date: str

    @validator('start_date', 'end_date')
    def validate_date(cls, v):
        try:
            # Попытка преобразовать строку в дату. Укажите желаемый формат даты.
            date = datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            # Вызов исключения, если формат не соответствует ожидаемому.
            raise ValueError('The date must be in the format YYYY-MM-DD')
        current_date = datetime.now()
        if date > current_date:
            raise ValueError('the date should not be in the future')
        return v

