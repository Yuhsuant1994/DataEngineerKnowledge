# To start
`docker build -t api-app .`
`docker run -p 8000:80 api-app`
for auto reload
`docker run -p 8000:80 -v ./backend:/app api-app uvicorn app.main:app --reload --host 0.0.0.0 --port 80`