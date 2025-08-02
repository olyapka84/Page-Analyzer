### Hexlet tests and linter status:
[![Actions Status](https://github.com/Olyapka84/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Olyapka84/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=olyapka84_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=olyapka84_python-project-83)

# Page Analyzer

[Live Demo on Render](https://python-project-83-olyapka.onrender.com/)

## 📌 About the Project

**Page Analyzer** is a web application built with Flask that allows users to analyze web pages for basic SEO suitability — similar to Google's PageSpeed Insights.

This project is part of a backend development curriculum and demonstrates:

- The basics of **MVC architecture**
- Handling **HTTP requests**, **routing**, and using a **template engine (Jinja2)**
- Interacting with a **PostgreSQL database** using **psycopg**
- Styling the frontend with **Bootstrap**
- Understanding **HTTP protocol** and **client-server architecture**
- Deployment using **Render.com** as a **PaaS (Platform as a Service)**

---

## Technologies Used

- Python 3.10+
- Flask
- Gunicorn
- psycopg
- Bootstrap 5
- uv (Python package manager)
- Render.com (deployment)

---

## 🛠 Local Setup

```bash
# Clone the repository
git clone https://github.com/your-username/python-project-83.git
cd python-project-83

# Install dependencies
uv pip install .

# Run locally
uv run flask --app page_analyzer run
