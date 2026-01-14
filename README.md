# 💀 LayOff Market

> *"Where careers come to die"* - A satirical betting platform

A dark-humor web application where users can place bets on which employees might be laid off. This is **purely satirical** and meant for entertainment purposes only.

## ⚠️ Disclaimer

This application is **satire**. It should not be used to actually bet on people's employment status. It's a commentary on corporate layoff culture and should be treated as dark humor among colleagues.

## 🎰 Features

### User Features
- Register and receive 1000 starting coins
- Browse departments and positions marked for cuts
- View candidates with their betting odds
- Place bets on who might be laid off
- Track betting history and winnings
- Compete on the leaderboard

### Admin Backoffice
- Add/manage departments (e.g., CAESARS SLOTS, CENTRAL SLOTS)
- Add/manage positions with COR codes and number of cuts
- Add candidates with photos, bios, and betting odds
- Set and adjust "cotele" (odds) for each candidate
- Mark candidates as laid off (resolves bets)
- View betting statistics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone/navigate to the project**
   ```bash
   cd layoffs_market
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   - User interface: http://localhost:5000
   - Admin panel: http://localhost:5000/admin

### Default Admin Credentials
- **Username:** `admin`
- **Password:** `layoffs2024`

## 📁 Project Structure

```
layoffs_market/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   ├── css/
│   │   ├── style.css     # User interface styles
│   │   └── admin.css     # Admin panel styles
│   ├── js/
│   │   └── app.js        # Frontend JavaScript
│   ├── img/              # Static images
│   └── uploads/          # Candidate photos
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Homepage
    ├── department.html   # Department view
    ├── leaderboard.html  # Leaderboard
    ├── profile.html      # User profile
    └── admin/
        ├── base.html         # Admin base template
        ├── login.html        # Admin login
        ├── dashboard.html    # Admin dashboard
        ├── departments.html  # Manage departments
        ├── positions.html    # Manage positions
        ├── candidates.html   # Manage candidates
        └── edit_candidate.html
```

## 🎮 How to Use

### As Admin:
1. Login at `/admin/login`
2. Add departments (e.g., "CAESARS SLOTS (CC)", "CENTRAL SLOTS")
3. Add positions with number of cuts (e.g., "C# Developer - 10 positions to cut")
4. Add candidates (employees) with photos and set their odds
5. When layoffs occur, mark candidates as "laid off" to resolve bets

### As User:
1. Register on the homepage
2. Browse departments to see positions at risk
3. View candidates and their odds
4. Place bets using your coins
5. If your prediction comes true, win coins based on the odds!

## 🎯 Understanding Odds (Cotele)

- **Low odds (1.5x - 2.0x):** High probability of being laid off
- **Medium odds (2.0x - 4.0x):** Medium probability
- **High odds (4.0x+):** Low probability (bigger payout if correct!)

Example: Bet 100 coins on someone with 3.5x odds. If they get laid off, you win 350 coins!

## 🛠️ Customization

### Change Admin Password
Edit `app.py` and modify the `init_db()` function, or update directly in SQLite.

### Add Default Avatar
Replace `static/img/default-avatar.png` with your preferred default image.

### Styling
Modify CSS variables in `static/css/style.css` and `static/css/admin.css` to change the color scheme.

## 🔧 Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login
- **Database:** SQLite
- **Frontend:** HTML5, CSS3 (custom), Vanilla JavaScript
- **Fonts:** Creepster (display), Rubik (body)

## 🐛 Known Issues

- No real-time updates (page refresh needed to see bet changes)
- No password recovery for users (by design - it's just for fun)
- Images must be manually replaced if default avatar is needed

## 📜 License

MIT License - Use at your own risk and humor.

---

*Remember: This is satire. Be kind to your colleagues, even if you bet against them. 💀*

