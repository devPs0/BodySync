from flask import Flask, render_template, request, redirect, jsonify, session
import os
import json
import secrets  # added for dynamic secret key
from datetime import datetime
from functools import wraps
from gemini_handler import generate_workout_plan
from gemini_new_day import generate_enhanced_workout_output
from gemini_test_gen import generate_fitness_assessment
from gemini_config import get_gemini_status, update_gemini_api_key
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import url_for


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # forces new session each run
app.config['SESSION_PERMANENT'] = False  # optional: avoids session persistence

# Resolve data files relative to this script directory to avoid CWD issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "saved_workouts.json")
USER_FILE = os.path.join(BASE_DIR, "users.json")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def load_saved_workouts():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_workouts(workouts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(workouts, f, indent=2, ensure_ascii=False)

def send_welcome_email(to_email, username):
    """Send a welcome email if sender and app password are available via env vars.

    Set GMAIL_SENDER and GMAIL_APP_PASSWORD in environment for this to work.
    If not set, the function will noop.
    """
    sender_email = os.getenv("GMAIL_SENDER")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        print("[info] Skipping welcome email (env GMAIL_SENDER/GMAIL_APP_PASSWORD not set)")
        return

    subject = "Welcome to AI Gym Planner"
    body = f"""
    Hi {username},

    Welcome to the AI-powered Gym Planner!
    We're thrilled to have you on board.

    Explore your personalized workout plans, track your fitness goals, and stay motivated on your fitness journey.

    - Team Fitness
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
            print("✅ Welcome email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)


@app.route('/')
@login_required
def home():
    workouts = load_saved_workouts()
    return render_template('index.html', workouts=workouts)

@app.route('/generate_workout', methods=['GET', 'POST'])
@login_required
def generate_workout():
    if request.method == 'GET':
        return redirect('/')
    
    try:
        goal = request.form.get('goal')
        experience = request.form.get('experience') 
        equipment = request.form.get('equipment')
        schedule = request.form.get('schedule')
        
        print(f"🔍 Received form data: goal={goal}, experience={experience}, equipment={equipment}, schedule={schedule}")
        
        if not goal or not experience or not equipment or not schedule:
            print("❌ Missing required fields")
            return render_template('index.html', error="Please fill in all required fields.")
        
        print("🤖 Calling Gemini to generate workout...")
        plan = generate_workout_plan(goal, experience, 7, 1, equipment)
        print(f"✅ Gemini returned: {type(plan)} with {len(plan) if isinstance(plan, list) else 'unknown'} items")
        
        # Format the plan nicely for display
        if isinstance(plan, list):
            formatted_plan = ""
            for day in plan:
                if isinstance(day, dict):
                    formatted_plan += f"<div class='workout-day bg-gray-50 p-4 mb-4 rounded-lg'>"
                    formatted_plan += f"<h3 class='text-lg font-bold text-gray-800 mb-2'>{day.get('workout', 'Workout Day')}</h3>"
                    exercises = day.get('exercises', '').replace('\n', '<br>')
                    formatted_plan += f"<div class='exercises text-gray-700'>{exercises}</div>"
                    formatted_plan += "</div>"
        else:
            formatted_plan = str(plan)
        
        workout = {
            'goal': goal,
            'description': f"{goal} workout plan for {experience} level with {equipment}",
            'plan': formatted_plan,
            'experience': experience,
            'equipment': equipment,
            'schedule': schedule,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"✅ Created workout object with plan length: {len(formatted_plan)} characters")
        print(f"✅ Rendering template with workout data...")
        
        return render_template('index.html', workout=workout)
        
    except Exception as e:
        print(f"Error generating workout: {e}")
        return render_template('index.html', error=f"Error generating workout: {str(e)}")

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    try:
        data = request.get_json()
        goal = data['goal']  # Changed from topic to goal
        level = data['level']
        days = int(data['days'])
        hours = int(data['hours'])
        equipment = data.get('equipment', 'basic')  # New field for equipment availability

        plan = generate_workout_plan(goal, level, days, hours, equipment)
        # Ensure each day object has a completed flag
        for day in plan:
            if 'completed' not in day:
                day['completed'] = False
        workouts = load_saved_workouts()
        workouts[goal] = {
            "goal": goal,
            "level": level,
            "days": days,
            "hours": hours,
            "equipment": equipment,
            "plan": plan,
            "completed_days": [],
            "last_completed_date": None,
            "streak_count": 0
        }
        save_workouts(workouts)
        return jsonify({"success": True, "workout": workouts[goal]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/my_workouts')
@login_required
def my_workouts():
    username = session.get('username')
    all_workouts = load_saved_workouts()
    user_workouts = all_workouts.get(username, [])
    return render_template('my_workouts.html', workouts=user_workouts)

@app.route('/complete_day', methods=['POST'])
@login_required
def complete_day():
    data = request.json
    goal = data['goal']  # Changed from topic to goal
    day_index = int(data['day'])

    workouts = load_saved_workouts()
    today = datetime.now().strftime("%Y-%m-%d")

    if goal in workouts and 0 <= day_index < len(workouts[goal]['plan']):
        workout = workouts[goal]
        completed_days = workout.get("completed_days", [])
        if day_index not in completed_days:
            completed_days.append(day_index)

        workout['plan'][day_index]['completed'] = True
        last_date = workout.get("last_completed_date")
        streak = workout.get("streak_count", 0)

        if last_date:
            last = datetime.strptime(last_date, "%Y-%m-%d")
            now = datetime.strptime(today, "%Y-%m-%d")
            if (now - last).days == 1:
                streak += 1
            elif (now - last).days > 1:
                streak = 1
        else:
            streak = 1

        workout["completed_days"] = completed_days
        workout["last_completed_date"] = today
        workout["streak_count"] = streak

        save_workouts(workouts)
        return jsonify({"success": True, "streak": streak, "completed_days": completed_days})
    return jsonify({"success": False, "error": "Invalid goal or day"})

@app.route('/regenerate', methods=['POST'])
@login_required
def regenerate():
    goal = request.form['goal']  # Changed from topic to goal
    workouts = load_saved_workouts()
    if goal in workouts:
        level = workouts[goal]['level']
        days = workouts[goal]['days']
        hours = workouts[goal]['hours']
        equipment = workouts[goal].get('equipment', 'basic')
        new_plan = generate_workout_plan(goal, level, days, hours, equipment)
        workouts[goal]['plan'] = new_plan
        save_workouts(workouts)
    return redirect('/my_workouts')

@app.route('/enhance_day', methods=['POST'])
@login_required
def enhance_day():
    try:
        data = request.json
        goal = data['goal']  # Changed from topic to goal
        level = data['level']
        days = data['days']
        hours = data['hours']
        day_workout = data['day_workout']  # Changed from day_task to day_workout
        output = generate_enhanced_workout_output(goal, day_workout, level, days, hours)
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/progress_fitness')
@login_required
def progress_fitness():
    return render_template('progress_fitness.html')

@app.route('/test_progress')
@login_required
def test_progress():
    return render_template('test_progress.html')

@app.route('/get_workouts')
@login_required
def get_workouts():
    all_workouts = load_saved_workouts()
    username = session.get('username')
    user_workouts = all_workouts.get(username, [])
    
    # Extract unique workout goals for the current user
    user_goals = []
    for workout in user_workouts:
        goal = workout.get('goal')
        if goal and goal not in user_goals:
            user_goals.append(goal)
    
    return jsonify({"success": True, "goals": user_goals, "topics": user_goals})

@app.route('/get_progress')
@login_required
def get_progress():
    print("🔍 GET_PROGRESS: Loading saved workouts...")
    all_workouts = load_saved_workouts()
    username = session.get('username')
    user_workouts = all_workouts.get(username, [])
    
    print(f"🔍 GET_PROGRESS: Username={username}, Found {len(user_workouts)} workouts")
    print(f"🔍 GET_PROGRESS: Workouts={[w.get('goal', 'No Goal') for w in user_workouts]}")
    
    total_workouts = len(user_workouts)
    total_completed = 0
    total_pending = 0
    max_streak = 0
    workout_data = {}

    for i, workout in enumerate(user_workouts):
        # Parse the plan to count days (count div elements with 'workout-day' class)
        plan_html = workout.get('plan', '')
        total_days = plan_html.count("class='workout-day")
        
        completed = len(workout.get('completed_days', []))
        pending = total_days - completed
        streak = workout.get('streak_count', 0)
        percent = int((completed / total_days) * 100) if total_days else 0

        total_completed += completed
        total_pending += pending
        max_streak = max(max_streak, streak)

        goal = workout.get('goal', f'Workout {i+1}')
        # Handle duplicate goals by adding index
        unique_key = goal
        counter = 1
        while unique_key in workout_data:
            unique_key = f"{goal} ({counter})"
            counter += 1
            
        workout_data[unique_key] = {
            "total_days": total_days,
            "completed": completed,
            "pending": pending,
            "streak": streak,
            "percent": percent
        }

    response_data = {
        "success": True,
        "total_workouts": total_workouts,
        "completed_days": total_completed,
        "pending_days": total_pending,
        "streak": max_streak,
        "workout_data": workout_data,
        "workouts": user_workouts  # Added the actual workouts array
    }
    
    print(f"🔍 GET_PROGRESS: Returning response with {len(user_workouts)} workouts")
    print(f"🔍 GET_PROGRESS: Response keys: {list(response_data.keys())}")
    
    return jsonify(response_data)

@app.route('/generate_assessment', methods=['POST'])
@login_required
def generate_assessment():
    try:
        data = request.json
        goal = data.get('goal')  # Changed from topic to goal
        level = data.get('level')
        # Frontend sends 'questions' key; fall back to 'num'
        num = int(data.get('questions', data.get('num', 5)))

        if not goal or not level:
            raise ValueError("Missing goal or level.")

        assessment = generate_fitness_assessment(goal, level, num)
        return jsonify({"success": True, "assessment": assessment})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/mark_complete', methods=['POST'])
@login_required
def mark_complete():
    data = request.json
    workout_index = int(data.get('workout_index', 0))
    day_index = int(data.get('day_index'))
    completed = data.get('completed', False)

    all_workouts = load_saved_workouts()
    username = session.get('username')
    user_workouts = all_workouts.get(username, [])

    if 0 <= workout_index < len(user_workouts):
        workout = user_workouts[workout_index]
        
        # Parse the plan to get the total number of days
        plan_html = workout.get('plan', '')
        total_days = plan_html.count("class='workout-day")
        
        if 0 <= day_index < total_days:
            # Ensure completed_days list exists
            workout.setdefault('completed_days', [])

            if completed:
                if day_index not in workout.get('completed_days', []):
                    workout['completed_days'].append(day_index)
            else:
                if day_index in workout.get('completed_days', []):
                    workout['completed_days'].remove(day_index)

            # Update the workouts data
            all_workouts[username] = user_workouts
            save_workouts(all_workouts)
            return jsonify({"success": True, "completed_days": workout['completed_days']})
    
    return jsonify({"success": False, "error": "Invalid request"})

@app.route('/save_workout', methods=['POST'])
@login_required
def save_workout():
    try:
        data = request.get_json()
        username = session.get('username')
        
        # Load existing workouts
        workouts = load_saved_workouts()
        if username not in workouts:
            workouts[username] = []
        
        # Add new workout
        workouts[username].append(data)
        save_workouts(workouts)
        
        return jsonify({"success": True, "message": "Workout saved successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/clear_workouts', methods=['POST'])
@login_required
def clear_workouts():
    try:
        username = session.get('username')
        workouts = load_saved_workouts()
        
        if username in workouts:
            workouts[username] = []
            save_workouts(workouts)
        
        return jsonify({"success": True, "message": "All workouts cleared!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/generate_test', methods=['POST'])
@login_required
def generate_test():
    try:
        data = request.get_json()
        topic = data.get('topic')
        level = data.get('level', 'intermediate')
        questions = int(data.get('questions', 5))
        
        # Generate fitness assessment questions using Gemini
        assessment_questions = generate_fitness_assessment(topic, level, questions)
        
        return jsonify({
            "success": True,
            "questions": assessment_questions
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/delete_workout", methods=["POST"])
@login_required
def delete_workout():
    try:
        print(f"🗑️ DELETE WORKOUT REQUEST RECEIVED")
        print(f"📋 Request content type: {request.content_type}")
        print(f"📋 Request data: {request.get_data()}")
        
        data = request.get_json()
        print(f"📋 Parsed JSON data: {data}")
        
        index = int(data.get('index'))
        username = session.get('username')
        print(f"👤 Username: {username}, Index to delete: {index}")
        
        all_workouts = load_saved_workouts()
        user_workouts = all_workouts.get(username, [])
        print(f"📊 User has {len(user_workouts)} workouts")
        
        if 0 <= index < len(user_workouts):
            deleted_workout = user_workouts[index]
            print(f"🎯 Deleting workout: {deleted_workout.get('goal', 'Unknown')} at index {index}")
            
            # Remove the workout at the specified index
            user_workouts.pop(index)
            all_workouts[username] = user_workouts
            save_workouts(all_workouts)
            
            print(f"✅ Workout deleted successfully! Remaining: {len(user_workouts)} workouts")
            return jsonify({"success": True, "message": "Workout deleted successfully!"})
        else:
            print(f"❌ Invalid index {index}, user has {len(user_workouts)} workouts")
            return jsonify({"success": False, "message": f"Invalid workout index {index}"})
            
    except Exception as e:
        print(f"❌ Exception in delete_workout: {str(e)}")
        return jsonify({"success": False, "message": str(e)})

@app.route('/goals')
@login_required
def goals_page():
    return render_template('goals.html')

@app.route('/api/streak_achievements')
@login_required
def get_streak_achievements():
    try:
        all_workouts = load_saved_workouts()
        username = session.get('username')
        user_workouts = all_workouts.get(username, [])

        total_workouts = len(user_workouts)
        total_completed = 0
        total_days = 0
        max_streak = 0

        for workout in user_workouts:
            # Parse HTML plan to count days
            plan_html = workout.get('plan', '')
            workout_days = plan_html.count("class='workout-day")
            total_days += workout_days
            
            completed_days = workout.get("completed_days", [])
            total_completed += len(completed_days)
            max_streak = max(max_streak, workout.get("streak_count", 0))

        badge = "-"
        if total_completed >= 30:
            badge = "🏆 Fitness Champion"
        elif total_completed >= 14:
            badge = "💪 Strength Builder"
        elif total_completed >= 7:
            badge = "🔥 Weekly Warrior"

        response = {
            "streak": max_streak if max_streak else total_completed,
            "badge": badge,
            "progress": f"{total_completed}/{total_days}",
            "quote": "Every workout counts! Stay strong and keep pushing forward!"
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_motivation_data', methods=['GET'])
@login_required
def get_motivation_data():
    # Keep this route consistent with /api/streak_achievements
    all_workouts = load_saved_workouts()
    username = session.get('username')
    user_workouts = all_workouts.get(username, [])

    total_completed = 0
    total_days = 0
    for workout in user_workouts:
        # Parse HTML plan to count days
        plan_html = workout.get('plan', '')
        workout_days = plan_html.count("class='workout-day")
        total_days += workout_days
        
        completed_days = workout.get("completed_days", [])
        total_completed += len(completed_days)

    badges = []
    if total_completed >= 30:
        badges.append('🏆 Fitness Champion')
    elif total_completed >= 14:
        badges.append('💪 Strength Builder')
    elif total_completed >= 7:
        badges.append('🔥 Weekly Warrior')

    streak = total_completed

    return jsonify({
        'streak': streak,
        'badge': ', '.join(badges) if badges else '-',
        'progress': f"{total_completed}/{total_days}"
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r', encoding="utf-8") as f:
                users = json.load(f)

            if username in users and users[username]['password'] == password:
                session['username'] = username
                return redirect('/')
            else:
                return render_template('login.html', error='Invalid credentials')

        return render_template('login.html', error='No users found. Please register first.')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users = {}
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r', encoding="utf-8") as f:
                try:
                    users = json.load(f)
                except Exception:
                    users = {}

        if username in users:
            return render_template('register.html', error='Username already exists')

        users[username] = {
            'password': password,
            'email': email
        }

        with open(USER_FILE, 'w', encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)

        send_welcome_email(email, username)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/api/gemini/status')
@login_required
def gemini_status():
    """Get current Gemini API status"""
    status = get_gemini_status()
    return jsonify(status)

@app.route('/api/gemini/update', methods=['POST'])
@login_required
def update_gemini_key():
    """Update Gemini API key"""
    try:
        data = request.get_json()
        new_key = data.get('api_key', '').strip()
        
        if not new_key:
            return jsonify({"success": False, "error": "API key is required"})
        
        update_gemini_api_key(new_key)
        status = get_gemini_status()
        
        return jsonify({
            "success": True, 
            "message": "API key updated successfully",
            "status": status
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    # Use debug=True to see detailed errors; disable reloader to avoid double-import issues
    app.run(debug=True, use_reloader=False, host='127.0.0.1', port=5000)
