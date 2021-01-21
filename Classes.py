from pydantic import BaseModel, Field


class ErrorBonch(BaseModel):
    description: str = Field('Бонч спит')


class ErrorServer(BaseModel):
    description: str = Field('Что-то сломалось на сервере апи')


class NotFound(BaseModel):
    description: str = Field('Такого расписания нет')



errorcodes = {
    523: {'model': ErrorBonch, 'description': 'Бонч спит'},
    500: {'model': ErrorServer, 'description': 'Ошибка в сервере апи'},
    200: {'description': 'Успешно отправлено'},
    404: {'description': "Такого расписания нет"}
}
