# TaskFlow

TaskFlow is a Django-based task management application.

## Prerequisites

- Python 3.12+
- Django (latest version)
- XAMPP (for local development)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/dmji006/taskflow.git
cd taskflow
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required dependencies:

```bash
pip install django
```

4. Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Development Server

To start the development server:

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Project Structure

```
taskflow/
├── manage.py
├── taskflow/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - [your-email@example.com](mailto:your-email@example.com)

Project Link: [https://github.com/yourusername/taskflow](https://github.com/yourusername/taskflow)
