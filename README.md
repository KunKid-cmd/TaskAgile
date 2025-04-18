# TaskAgile

**TaskAgile** is a modern and responsive Todo List web app built with **
Django**, powered by **Neon PostgreSQL** and **Cloudinary** for media storage.

Users can:

- Sign up / log in securely
- Add, edit, and delete tasks
- Attach images to todos (stored on Cloudinary)
- Organize tasks by status: To Do, In Progress, Done
- Drag and drop tasks to change their status

---

## Tech Stack

- **Backend**: Django
- **Database**: PostgreSQL (hosted on Neon)
- **Media**: Cloudinary
- **Frontend**: Bootstrap 5
- **Storage & Config**: dotenv + widget-tweaks

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/KunKid-cmd/TaskAgile.git
cd taskagile
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. Set up ```.env```

5. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Run test**
   First Time

```bash
python manage.py test
```

After the First Run (reuse DB):

```bash
python manage.py test --keepdb
```

7. **Run the server**

```bash
python manage.py runserver
```