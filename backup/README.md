# Student Management System (Flask + Pytest + Jenkins + Docker)

## 📌 Features
- Add, view, fetch, and delete students
- REST API with Flask
- Tested with pytest
- Dockerized
- CI/CD ready with Jenkins

## 🚀 Run Locally
```bash
pip install -r requirements.txt
python app.py
```

## 🧪 Run Tests
```bash
pytest test_app.py
```

## 🐳 Docker
```bash
docker build -t student-api .
docker run -p 5000:5000 student-api
```

## 🛠️ Jenkins Pipeline
This project contains a `Jenkinsfile` to automate:
- Code clone
- Dependency install
- Test execution
- App deployment