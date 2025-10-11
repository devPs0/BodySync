# AI Gym Planner

A Flask-based web application that helps you create personalized workout plans using AI (Google Gemini API).

## Features

- **AI-powered workout plan generation** using Google Gemini
- **User authentication** with registration and login
- **Progress tracking** with workout streaks and fitness achievements
- **Interactive workout programs** with daily exercises and form tips
- **Fitness assessments** for various goals and fitness levels
- **Equipment-based customization** (basic, home gym, full gym)
- **Email notifications** for new user registration

## Quick Start

### 1. Install Dependencies

```bash
pip install Flask
```

Optional (for AI features):
```bash
pip install google-generativeai
```

### 2. Environment Setup (Optional)

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
GMAIL_SENDER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
FLASK_DEBUG=false
```

### 3. Run the Application

```bash
python app.py
```

The application will be available at: http://127.0.0.1:5000

## Usage

1. **Register** a new account or **login** with existing credentials
2. **Create workout plans** by specifying:
   - Fitness Goal (e.g., "Weight Loss", "Muscle Building", "Strength Training")
   - Fitness level (Beginner/Intermediate/Advanced)
   - Available equipment (Basic/Home Gym/Full Gym)
   - Number of days
   - Daily workout duration
3. **Track progress** by marking workout days as complete
4. **Generate fitness assessments** to evaluate your progress
5. **View detailed progress** and fitness achievement statistics

## File Structure

```
Gym Planner/
├── app.py                    # Main Flask application
├── gemini_handler.py         # AI workout plan generation
├── gemini_new_day.py         # Enhanced daily workout content
├── gemini_test_gen.py        # Fitness assessment generation
├── program_handler.py        # Workout data management
├── requirements.txt          # Python dependencies
├── templates/                # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── my_workouts.html
│   ├── progress_fitness.html
│   └── goals.html
├── static/                  # CSS and assets
│   └── styles.css
├── saved_workouts.json      # User workout programs
└── users.json              # User accounts
```

## API Endpoints

- `GET /` - Home page (create workout plans)
- `GET /login` - User login
- `GET /register` - User registration
- `GET /my_workouts` - View saved workout programs
- `GET /progress_fitness` - Progress tracking and fitness assessments
- `POST /generate` - Generate new workout plan
- `POST /generate_assessment` - Generate fitness assessment questions
- `POST /mark_complete` - Mark workout day as complete
- `POST /enhance_day` - Get enhanced workout details

## Configuration

### AI Features
- Set `GEMINI_API_KEY` environment variable to enable AI-powered features
- Without API key, the app will use fallback content

### Email Notifications
- Set `GMAIL_SENDER` and `GMAIL_APP_PASSWORD` for welcome emails
- Uses Gmail SMTP (requires app password, not regular password)

### Debug Mode
- Set `FLASK_DEBUG=true` to enable debug mode (not recommended for production)

## Troubleshooting

### Common Issues

1. **Import errors**: Install missing packages with `pip install package_name`
2. **Multiprocessing errors**: Disable debug mode by setting `FLASK_DEBUG=false`
3. **File not found**: Ensure you're running from the correct directory
4. **API errors**: Check your Gemini API key and internet connection

### Data Files

The app creates these JSON files automatically:
- `users.json` - Stores user accounts
- `saved_workouts.json` - Stores workout programs and progress

## Development

To contribute or modify:

1. Fork the repository
2. Make changes
3. Test locally with `python app.py`
4. Submit pull request

## License

This project is open source. Feel free to modify and distribute.