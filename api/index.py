from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Create Flask app
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'the-layoffs-are-coming-winter-is-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'


# ============== MODELS ==============

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50))
    positions = db.relationship('Position', backref='department', lazy=True, cascade='all, delete-orphan')


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    cor_code = db.Column(db.String(100))
    total_employees = db.Column(db.Integer, default=0)
    positions_to_cut = db.Column(db.Integer, default=0)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    candidates = db.relationship('Candidate', backref='position', lazy=True, cascade='all, delete-orphan')


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(500), default='default.png')
    odds = db.Column(db.Float, default=2.0)
    bio = db.Column(db.Text)
    is_laid_off = db.Column(db.Boolean, default=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    bets = db.relationship('Bet', backref='candidate', lazy=True, cascade='all, delete-orphan')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    coins = db.Column(db.Integer, default=1000)
    bets = db.relationship('Bet', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    odds_at_bet = db.Column(db.Float, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False)
    won = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


# ============== COMPLETE SEED DATA (262 employees, 63 to cut) ==============
SEED_DATA = {
    "Boost": [
        {"title": "Machine Learning Engineer", "cor_code": "251204", "total": 1, "cut": 0},
    ],
    "CC (Caesars Slots)": [
        {"title": "2D Animator", "cor_code": "251101", "total": 1, "cut": 0},
        {"title": "2D Artist", "cor_code": "251101, 251201", "total": 7, "cut": 1},
        {"title": "Animator", "cor_code": "251101", "total": 3, "cut": 1},
        {"title": "Art Group Manager", "cor_code": "122314", "total": 1, "cut": 0},
        {"title": "Art Team Leader", "cor_code": "122314, 251206", "total": 2, "cut": 0},
        {"title": "C# Developer", "cor_code": "251202, 251204, 351201", "total": 17, "cut": 10},
        {"title": "C# Technical Lead", "cor_code": "251202, 251204", "total": 5, "cut": 0},
        {"title": "Copywriter", "cor_code": "351202", "total": 1, "cut": 0},
        {"title": "Flash Integrator", "cor_code": "251101, 351202", "total": 7, "cut": 3},
        {"title": "Java Developer", "cor_code": "251202, 251204", "total": 11, "cut": 0},
        {"title": "Java Technical Lead", "cor_code": "121904, 251202, 251204", "total": 5, "cut": 0},
        {"title": "JavaScript Developer", "cor_code": "251202, 251204", "total": 2, "cut": 0},
        {"title": "JavaScript Technical Lead", "cor_code": "251202", "total": 1, "cut": 0},
        {"title": "Lead Animator", "cor_code": "251201", "total": 1, "cut": 0},
        {"title": "Manual QA Engineer", "cor_code": "251201, 351202", "total": 17, "cut": 6},
        {"title": "Monetization Operations Specialist", "cor_code": "251201", "total": 2, "cut": 0},
        {"title": "Product Owner (Tech)", "cor_code": "121904", "total": 1, "cut": 1},
        {"title": "Product Senior Expert", "cor_code": "121904", "total": 1, "cut": 0},
        {"title": "Program Lead", "cor_code": "251206", "total": 1, "cut": 0},
        {"title": "QA Automation Engineer", "cor_code": "251201, 251202, 351202", "total": 4, "cut": 1},
        {"title": "QA Automation Team Leader", "cor_code": "251206", "total": 1, "cut": 1},
        {"title": "QA Technical Lead", "cor_code": "251201, 351202", "total": 2, "cut": 0},
        {"title": "R&D Group Manager", "cor_code": "251206", "total": 3, "cut": 0},
        {"title": "R&D Team Leader", "cor_code": "122314, 251206", "total": 9, "cut": 2},
        {"title": "Senior Director of Research & Development", "cor_code": "251206", "total": 1, "cut": 0},
        {"title": "Technical Product Owner", "cor_code": "122314, 251206", "total": 2, "cut": 0},
    ],
    "Cross Communication": [
        {"title": "Communication and Brand Manager", "cor_code": "243104", "total": 1, "cut": 1},
    ],
    "Cross Finance": [
        {"title": "Bookkeeper", "cor_code": "263102", "total": 1, "cut": 0},
    ],
    "Cross HR": [
        {"title": "HR Director", "cor_code": "121207", "total": 1, "cut": 0},
        {"title": "HR Operations Specialist", "cor_code": "242314", "total": 2, "cut": 0},
        {"title": "Talent Acquisition Specialist", "cor_code": "242309", "total": 2, "cut": 1},
        {"title": "Talent Acquisition Team Lead", "cor_code": "121207", "total": 1, "cut": 0},
    ],
    "Cross Legal & Finance": [
        {"title": "Chief Accountant", "cor_code": "112020", "total": 1, "cut": 0},
        {"title": "Expert Corporate Counsel", "cor_code": "261103", "total": 1, "cut": 0},
    ],
    "Cross Operations": [
        {"title": "HSE Responsible", "cor_code": "242304", "total": 1, "cut": 1},
    ],
    "Cross Slots Central": [
        {"title": "2D Animator", "cor_code": "251101", "total": 2, "cut": 2},
        {"title": "2D Artist", "cor_code": "251101, 251201, 351202", "total": 5, "cut": 4},
        {"title": "Animator", "cor_code": "251101, 251201", "total": 3, "cut": 3},
        {"title": "Art Director", "cor_code": "251206", "total": 1, "cut": 0},
        {"title": "Art Team Leader", "cor_code": "251206", "total": 2, "cut": 2},
        {"title": "Expert Animator", "cor_code": "351202", "total": 1, "cut": 1},
        {"title": "Expert Artist", "cor_code": "251101, 351202", "total": 2, "cut": 1},
        {"title": "Lead Animator", "cor_code": "251101", "total": 1, "cut": 0},
        {"title": "Product Owner", "cor_code": "251206", "total": 2, "cut": 1},
        {"title": "Product Team Leader", "cor_code": "251206", "total": 1, "cut": 0},
        {"title": "Technical Art Lead", "cor_code": "121904, 251101", "total": 2, "cut": 2},
        {"title": "Technical Artist", "cor_code": "251101", "total": 1, "cut": 1},
    ],
    "Cross Technologies": [
        {"title": "Incident Engineer", "cor_code": "251201, 351202", "total": 2, "cut": 1},
        {"title": "Incident Engineer Expert", "cor_code": "351202", "total": 1, "cut": 1},
        {"title": "IT Service Specialist", "cor_code": "251101, 251203", "total": 2, "cut": 1},
        {"title": "IT System Engineer", "cor_code": "251101", "total": 1, "cut": 0},
        {"title": "Service Operations Analyst", "cor_code": "351202", "total": 1, "cut": 1},
        {"title": "Site Reliability Engineer", "cor_code": "251204", "total": 1, "cut": 0},
        {"title": "SRE Expert", "cor_code": "251204", "total": 1, "cut": 0},
        {"title": "SVP Technologies Program", "cor_code": "251206", "total": 1, "cut": 0},
        {"title": "System Operations Engineer", "cor_code": "351202", "total": 1, "cut": 0},
        {"title": "Tech Project Management Expert", "cor_code": "121904", "total": 1, "cut": 0},
        {"title": "Technical Account Manager", "cor_code": "351202", "total": 1, "cut": 0},
        {"title": "MIS Group Manager", "cor_code": "251206", "total": 1, "cut": 0},
    ],
    "HOF (House of Fun)": [
        {"title": "Manual QA Engineer", "cor_code": "251201", "total": 2, "cut": 0},
        {"title": "Monetization Operation Team Leader", "cor_code": "251206", "total": 1, "cut": 0},
        {"title": "Monetization Operations Lead", "cor_code": "351202", "total": 1, "cut": 0},
        {"title": "Monetization Operations Specialist", "cor_code": "251201", "total": 1, "cut": 0},
        {"title": "QA Technical Lead", "cor_code": "351202", "total": 1, "cut": 0},
        {"title": "Technical Art Lead", "cor_code": "351202", "total": 1, "cut": 0},
        {"title": "Technical Artist", "cor_code": "251101", "total": 1, "cut": 1},
    ],
    "SHARED TECH": [
        {"title": "Director of Architecture", "cor_code": "251101", "total": 1, "cut": 1},
    ],
    "WSOP": [
        {"title": "C# Developer", "cor_code": "251202", "total": 1, "cut": 0},
        {"title": "Full Stack Developer", "cor_code": "251202", "total": 1, "cut": 0},
        {"title": "Java Developer", "cor_code": "251202", "total": 14, "cut": 0},
        {"title": "Java Technical Lead", "cor_code": "251202", "total": 3, "cut": 0},
        {"title": "JavaScript Developer", "cor_code": "251202, 251204", "total": 3, "cut": 0},
        {"title": "JavaScript Technical Lead", "cor_code": "251202", "total": 2, "cut": 0},
        {"title": "Manual QA Engineer", "cor_code": "251201, 351202", "total": 16, "cut": 3},
        {"title": "Monetization Operation Team Leader", "cor_code": "251206", "total": 1, "cut": 0},
        {"title": "QA Automation Engineer", "cor_code": "251202, 351202", "total": 5, "cut": 2},
        {"title": "QA Automation Team Leader", "cor_code": "251206", "total": 1, "cut": 0},
        {"title": "QA Manager", "cor_code": "251206", "total": 1, "cut": 1},
        {"title": "QA Technical Lead", "cor_code": "251201, 351202", "total": 3, "cut": 0},
        {"title": "R&D Director", "cor_code": "251206", "total": 1, "cut": 0},
        {"title": "R&D Group Manager", "cor_code": "251206", "total": 3, "cut": 0},
        {"title": "R&D Team Leader", "cor_code": "251206", "total": 8, "cut": 0},
        {"title": "Release Engineer", "cor_code": "251206", "total": 1, "cut": 0},
        {"title": "Software Architect", "cor_code": "251101", "total": 2, "cut": 0},
        {"title": "Technical Artist", "cor_code": "251101, 351202", "total": 5, "cut": 2},
        {"title": "Technical Product Owner", "cor_code": "251202", "total": 1, "cut": 0},
        {"title": "Unity Developer", "cor_code": "251202, 251204, 351201, 351202", "total": 18, "cut": 3},
        {"title": "Unity Technical Lead", "cor_code": "251202, 251204", "total": 4, "cut": 0},
        {"title": "VP of Research & Development", "cor_code": "112019", "total": 1, "cut": 0},
    ],
    "Youda": [
        {"title": "Product Manager", "cor_code": "251206", "total": 1, "cut": 0},
    ],
}


def init_db():
    """Initialize database with seed data"""
    db.create_all()
    
    if not Admin.query.first():
        admin = Admin(username='admin')
        admin.set_password(os.environ.get('ADMIN_PASSWORD', 'layoffs2024'))
        db.session.add(admin)
    
    if not Department.query.first():
        for dept_name, positions in SEED_DATA.items():
            dept = Department(name=dept_name, code=dept_name[:3].upper())
            db.session.add(dept)
            db.session.flush()
            
            for pos_data in positions:
                position = Position(
                    title=pos_data["title"],
                    cor_code=pos_data["cor_code"],
                    total_employees=pos_data["total"],
                    positions_to_cut=pos_data["cut"],
                    department_id=dept.id
                )
                db.session.add(position)
    
    db.session.commit()


# ============== ROUTES ==============

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin_dashboard():
    departments = Department.query.all()
    total_employees = sum(p.total_employees for d in departments for p in d.positions)
    total_to_cut = sum(p.positions_to_cut for d in departments for p in d.positions)
    total_candidates = Candidate.query.count()
    total_bets = Bet.query.count()
    return render_template('admin/dashboard.html', 
                         departments=departments,
                         total_employees=total_employees,
                         total_to_cut=total_to_cut,
                         total_candidates=total_candidates,
                         total_bets=total_bets)


@app.route('/admin/departments', methods=['GET', 'POST'])
@login_required
def admin_departments():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        dept = Department(name=name, code=code)
        db.session.add(dept)
        db.session.commit()
        flash('Department added!', 'success')
        return redirect(url_for('admin_departments'))
    departments = Department.query.all()
    return render_template('admin/departments.html', departments=departments)


@app.route('/admin/departments/<int:id>/delete', methods=['POST'])
@login_required
def delete_department(id):
    dept = Department.query.get_or_404(id)
    db.session.delete(dept)
    db.session.commit()
    flash('Department deleted!', 'success')
    return redirect(url_for('admin_departments'))


@app.route('/admin/positions', methods=['GET', 'POST'])
@login_required
def admin_positions():
    if request.method == 'POST':
        title = request.form.get('title')
        cor_code = request.form.get('cor_code')
        total_employees = int(request.form.get('total_employees', 0))
        positions_to_cut = int(request.form.get('positions_to_cut', 0))
        department_id = int(request.form.get('department_id'))
        pos = Position(title=title, cor_code=cor_code, 
                      total_employees=total_employees,
                      positions_to_cut=positions_to_cut, department_id=department_id)
        db.session.add(pos)
        db.session.commit()
        flash('Position added!', 'success')
        return redirect(url_for('admin_positions'))
    positions = Position.query.all()
    departments = Department.query.all()
    return render_template('admin/positions.html', positions=positions, departments=departments)


@app.route('/admin/positions/<int:id>/update-cuts', methods=['POST'])
@login_required
def update_position_cuts(id):
    pos = Position.query.get_or_404(id)
    pos.positions_to_cut = int(request.form.get('positions_to_cut', 0))
    db.session.commit()
    flash(f'Updated: {pos.title}', 'success')
    return redirect(url_for('admin_positions'))


@app.route('/admin/positions/<int:id>/delete', methods=['POST'])
@login_required
def delete_position(id):
    pos = Position.query.get_or_404(id)
    db.session.delete(pos)
    db.session.commit()
    flash('Position deleted!', 'success')
    return redirect(url_for('admin_positions'))


@app.route('/admin/candidates', methods=['GET', 'POST'])
@login_required
def admin_candidates():
    if request.method == 'POST':
        name = request.form.get('name')
        bio = request.form.get('bio')
        odds = float(request.form.get('odds', 2.0))
        position_id = int(request.form.get('position_id'))
        
        candidate = Candidate(name=name, bio=bio, odds=odds, 
                            position_id=position_id, photo='default.png')
        db.session.add(candidate)
        db.session.commit()
        flash('Candidate added! 💀', 'success')
        return redirect(url_for('admin_candidates'))
    
    candidates = Candidate.query.all()
    positions = Position.query.all()
    return render_template('admin/candidates.html', candidates=candidates, positions=positions)


@app.route('/admin/candidates/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_candidate(id):
    candidate = Candidate.query.get_or_404(id)
    if request.method == 'POST':
        candidate.name = request.form.get('name')
        candidate.bio = request.form.get('bio')
        candidate.odds = float(request.form.get('odds', 2.0))
        candidate.position_id = int(request.form.get('position_id'))
        db.session.commit()
        flash('Candidate updated!', 'success')
        return redirect(url_for('admin_candidates'))
    
    positions = Position.query.all()
    return render_template('admin/edit_candidate.html', candidate=candidate, positions=positions)


@app.route('/admin/candidates/<int:id>/delete', methods=['POST'])
@login_required
def delete_candidate(id):
    candidate = Candidate.query.get_or_404(id)
    db.session.delete(candidate)
    db.session.commit()
    flash('Candidate removed!', 'success')
    return redirect(url_for('admin_candidates'))


@app.route('/admin/candidates/<int:id>/layoff', methods=['POST'])
@login_required
def mark_laid_off(id):
    candidate = Candidate.query.get_or_404(id)
    candidate.is_laid_off = not candidate.is_laid_off
    
    if candidate.is_laid_off:
        for bet in candidate.bets:
            if not bet.is_resolved:
                bet.is_resolved = True
                bet.won = True
                winnings = int(bet.amount * bet.odds_at_bet)
                bet.user.coins += winnings
        flash(f'💀 {candidate.name} LAID OFF!', 'danger')
    else:
        flash(f'{candidate.name} status reset.', 'info')
    
    db.session.commit()
    return redirect(url_for('admin_candidates'))


@app.route('/')
def index():
    departments = Department.query.all()
    total_employees = sum(p.total_employees for d in departments for p in d.positions)
    total_to_cut = sum(p.positions_to_cut for d in departments for p in d.positions)
    return render_template('index.html', departments=departments, 
                          total_employees=total_employees, total_to_cut=total_to_cut)


@app.route('/department/<int:id>')
def department_view(id):
    department = Department.query.get_or_404(id)
    return render_template('department.html', department=department)


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': 'Username taken!'})
    
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'user_id': user.id, 'coins': user.coins})


@app.route('/user/<int:id>')
def user_profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)


@app.route('/bet', methods=['POST'])
def place_bet():
    data = request.json
    user_id = data.get('user_id')
    candidate_id = data.get('candidate_id')
    amount = int(data.get('amount', 0))
    
    user = User.query.get(user_id)
    candidate = Candidate.query.get(candidate_id)
    
    if not user or not candidate:
        return jsonify({'success': False, 'message': 'Invalid user or candidate'})
    
    if candidate.is_laid_off:
        return jsonify({'success': False, 'message': 'Too late! 💀'})
    
    if amount <= 0 or user.coins < amount:
        return jsonify({'success': False, 'message': 'Not enough coins! 💸'})
    
    user.coins -= amount
    bet = Bet(user_id=user_id, candidate_id=candidate_id, 
              amount=amount, odds_at_bet=candidate.odds)
    db.session.add(bet)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'Bet placed! 🎰',
        'remaining_coins': user.coins,
        'potential_win': int(amount * candidate.odds)
    })


@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.coins.desc()).limit(50).all()
    return render_template('leaderboard.html', users=users)


@app.route('/api/user/<int:id>')
def api_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'username': user.username, 'coins': user.coins})


# Initialize on startup
with app.app_context():
    init_db()

application = app
