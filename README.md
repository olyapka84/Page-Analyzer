### Test status:
[![Actions Status](https://github.com/Olyapka84/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Olyapka84/python-project-83/actions)

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
# Install dependencies
uv pip install .
# Run locally
uv run flask --app page_analyzer run
