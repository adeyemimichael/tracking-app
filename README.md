# 💰 Pocket Money Tracker - Web Version

A beautiful web interface for the Pocket Money Tracker Python application. This project keeps the original Python logic intact while providing a modern, user-friendly web interface.

## 📁 Project Structure

```
tracking-app/
├── tracking.py          # Original Python code (unchanged)
├── app.py              # Flask web application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # HTML interface
└── static/
    └── css/
        └── style.css  # Styling
```

## 🚀 How to Run

### Step 1: Install Flask
Open your terminal and run:
```bash
pip install flask
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Web App
```bash
python app.py
```

### Step 3: Open in Browser
Open your web browser and go to:
```
http://127.0.0.1:5000
```

## ✨ Features

- **💵 Balance Tracking** - Monitor your current balance in real-time
- **💸 Spend Money** - Record your spending with instant feedback
- **📊 Statistics** - View total amount spent
- **📜 Spending History** - See all your transactions
- **⚠️ Low Balance Warning** - Get alerts when balance is below ₦1000
- **🔄 Reset Function** - Start fresh anytime
- **📱 Responsive Design** - Works on all devices

## 🎨 Design Features

- Modern gradient background
- Smooth animations
- Card-based layout
- Color-coded alerts
- Mobile-friendly interface
- Hover effects and transitions

## 🔧 How It Works

The web app uses **Flask** to:
1. Keep the same logic from `tracking.py`
2. Store data in browser sessions
3. Display information in HTML
4. Style everything with CSS

**No changes were made to the original Python logic!** The same conditions, calculations, and features work exactly as before.

## 👨‍🏫 For Teachers

This is perfect for teaching students:
- How to convert console apps to web apps
- Flask basics and routing
- HTML forms and templates
- CSS styling and animations
- Session management

## 📝 Notes

- Data is stored in browser sessions (resets when browser closes)
- For permanent storage, you can add a database later
- The original `tracking.py` file remains unchanged and functional

## 🎓 Learning Outcomes

Students will learn:
- Web development basics
- Frontend-backend connection
- User interface design
- Form handling
- Session management

---

**Built with ❤️ for students learning web development**
