# Phishing Quiz

Interactive quiz application to test and educate users about identifying phishing attempts versus legitimate messages across email, SMS, and WhatsApp.

## Features

- 18 randomized quiz questions (9 phishing + 9 legitimate examples)
- Real-world examples of phishing emails, SMS, and WhatsApp messages
- Detailed explanations for each answer
- Flag rewards for correct answers
- Responsive design with Bootstrap
- Backend data shuffling for each session

## Project Structure

```
phising-quiz/
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── id/                     # Indonesian version
│   ├── index.html
│   └── quiz.html
├── en/                     # English version
│   ├── index.html
│   └── quiz.html
├── scripts/
│   ├── script-id.js        # Indonesian quiz logic
│   └── script-en.js        # English quiz logic
├── iframe-soal-id/         # Quiz example iframes (Indonesian)
├── assets/                 # Images and logos
├── bootstrap-5/            # Bootstrap CSS/JS
└── css/                    # Custom styles
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone or Download the Project

```bash
cd "phising-quiz"
```

### 2. Create Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
```

**Windows (Command Prompt):**

```cmd
python -m venv .venv
```

**Linux/Mac:**

```bash
python3 -m venv .venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (Command Prompt):**

```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install Flask manually:

```bash
pip install flask
```

### 5. Run the Application

```bash
python app.py
```

The application will start on:

- **Local:** http://localhost:5000
- **Network:** http://0.0.0.0:5000

### 6. Access the Quiz

Open your browser and navigate to:

- **Indonesian version:** http://localhost:5000/id/quiz
- **English version:** http://localhost:5000/en/quiz
- **Home (redirects to Indonesian):** http://localhost:5000/

## API Endpoints

- `GET /api/quiz-data` - Returns shuffled quiz questions
- `GET /api/flag-data` - Returns flag rewards

## Development

### Deactivate Virtual Environment

When you're done working:

```bash
deactivate
```

### Update Dependencies

To update dependencies after making changes:

```bash
pip freeze > requirements.txt
```

## Quiz Content

The quiz includes:

**Phishing Examples:**

- Email phishing (document review, fake security alerts, Dropbox/Google spoofs)
- SMS phishing (Netflix, prize scams)
- WhatsApp phishing (.apk malware, government subsidy scams)

**Legitimate Examples:**

- Security notifications (LinkedIn, X/Twitter, Goodreads)
- Newsletters (Letterboxd)
- Sponsored ads (Android Developers)
- SMS promotions (myIM3, McDonald's)
- WhatsApp Business verified accounts (Tokopedia, Gojek)

## Configuration

### Secret Key

For production, set the `SECRET_KEY` environment variable:

**Windows (PowerShell):**

```powershell
$env:SECRET_KEY="your-secure-random-key-here"
```

**Linux/Mac:**

```bash
export SECRET_KEY="your-secure-random-key-here"
```

### Production Deployment

1. Set `debug=False` in `app.py`
2. Use a production WSGI server (gunicorn, waitress)
3. Set environment variables for secrets
4. Use HTTPS
5. Configure proper firewall rules

## Troubleshooting

### Virtual Environment Not Activating

- Ensure Python is in your PATH
- Check execution policy on Windows
- Use absolute path to activation script

### Port Already in Use

Change the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Not Found

Ensure virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

## License

Educational project for ITS NABU - Phishing awareness training.

## Contributors

- Mikhael Abie

## Support

For issues or questions, contact the development team.
