from fastapi import FastAPI
from app.routers import user, book
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()  # Создаем экземпляр приложения FastAPI

app.add_middleware(SessionMiddleware, secret_key='a3f5e4c3d6b89e8f3e6eebdbf65fa1234567890abcfdef1234a1b2c3d4e5f6g7')

app.include_router(user.router)  # подключаем дополнительные внешние роутеры
app.include_router(book.router)  # подключаем дополнительные внешние роутеры

templates = Jinja2Templates(directory='app/templates')  # указываме путь к templates

app.mount('/static', StaticFiles(directory='app/static'), name='static')


@app.get('/')
async def main(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})




# для запуска не из терминала, а напрямую
# if __name__ == "__main__":
#     uvicorn.run(app)
