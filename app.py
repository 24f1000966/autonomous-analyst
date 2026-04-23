import os
import json
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from database.database import db, User, AnalysisReport, Dataset
from flask_bcrypt import Bcrypt
import pandas as pd
from agents import NexusWorkflow
from agents.chat_agent import ChatAgent
import tempfile
from xhtml2pdf import pisa

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey_for_business_analyst'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/charts', exist_ok=True)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()
    
    # Auto-create Admin Superuser
    if not User.query.filter_by(email='admin@nexus.ai').first():
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(username='SuperAdmin', email='admin@nexus.ai', password=hashed_password, role='admin', tier='Enterprise', credits=9999, company_name='Nexus AI Core')
        db.session.add(admin_user)
        db.session.commit()

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Setup / Auth
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        company_name = request.form.get('company_name', 'Nexus AI')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password, role=role, credits=10, tier='Free', company_name=company_name)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! 10 free credits granted.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=request.form.get('remember'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# Role Based Query Helpers
def get_reports(user):
    if user.role == 'admin':
        return AnalysisReport.query.order_by(AnalysisReport.date_posted.desc()).all()
    elif user.role == 'manager':
        users = [u.id for u in User.query.filter_by(company_name=user.company_name).all()]
        return AnalysisReport.query.filter(AnalysisReport.user_id.in_(users)).order_by(AnalysisReport.date_posted.desc()).all()
    else:
        return AnalysisReport.query.filter_by(user_id=user.id).order_by(AnalysisReport.date_posted.desc()).all()

def get_datasets(user):
    if user.role == 'admin':
        return Dataset.query.order_by(Dataset.date_uploaded.desc()).all()
    elif user.role == 'manager':
        users = [u.id for u in User.query.filter_by(company_name=user.company_name).all()]
        return Dataset.query.filter(Dataset.user_id.in_(users)).order_by(Dataset.date_uploaded.desc()).all()
    else:
        return Dataset.query.filter_by(user_id=user.id).order_by(Dataset.date_uploaded.desc()).all()

# CORE NAVIGATION ROUTES
@app.route("/dashboard")
@login_required
def dashboard():
    reports = get_reports(current_user)[:5]
    datasets = get_datasets(current_user)
    rows_processed = sum(r.rows_processed for r in reports)
    insights_found = sum(r.insights_found for r in reports)
    
    return render_template('dashboard.html', 
                           reports=reports, 
                           total_reports=len(reports), 
                           rows_processed=rows_processed, 
                           insights_found=insights_found,
                           datasets=datasets)

@app.route("/datasets", methods=['GET', 'POST'])
@login_required
def datasets():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            ds = Dataset(filename=file.filename, filepath=filepath, user_id=current_user.id)
            db.session.add(ds)
            db.session.commit()
            flash('Dataset uploaded successfully!', 'success')
            return redirect(url_for('datasets'))
            
    datasets_list = get_datasets(current_user)
    return render_template('datasets.html', datasets=datasets_list)

@app.route("/dataset/delete/<int:dataset_id>", methods=['POST'])
@login_required
def delete_dataset(dataset_id):
    ds = db.session.get(Dataset, dataset_id)
    if ds and ds.user_id == current_user.id:
        db.session.delete(ds)
        db.session.commit()
        flash('Dataset deleted successfully.', 'info')
    return redirect(url_for('datasets'))


@app.route("/analysis", methods=['GET', 'POST'])
@login_required
def analysis():
    datasets = get_datasets(current_user)
    
    if request.method == 'POST':
        dataset_id = request.form.get('dataset_id')
        ds = db.session.get(Dataset, int(dataset_id))
        
        # Authorize: user can access this dataset
        if ds and ds in datasets:
            if current_user.credits <= 0:
                flash('Insufficient credits. Please upgrade your tier.', 'danger')
                return redirect(url_for('dashboard'))
                
            try:
                # Running the agentic workflow
                if ds.filename.endswith('.csv'):
                    df = pd.read_csv(ds.filepath)
                else:
                    df = pd.read_excel(ds.filepath)
                    
                workflow = NexusWorkflow()
                result = workflow.run_workflow(df)
                
                chart_path = result['charts'][0] if result['charts'] else None
                ai_insights = result['insights'].get('insights', [])
                recommendations_content = result.get('recommendations', '') # Not explicitly gathered if not saved, extending __init__.py required
                
                report_content = result['report_summary']
                
                # New Predictive Tracking
                forecast_data = json.dumps(result.get('forecasts', {}))
                alerts_data = json.dumps(result.get('alerts', []))
                
                report = AnalysisReport(
                    filename=ds.filename,
                    dataset_id=ds.id,
                    rows_processed=len(df),
                    insights_found=len(ai_insights),
                    report_content=report_content,
                    insights_content=json.dumps(ai_insights),
                    memory_context=report_content,
                    chart_path=chart_path,
                    user_id=current_user.id,
                    forecast_data=forecast_data,
                    alerts_data=alerts_data
                )
                
                current_user.credits -= 1
                db.session.add(report)
                db.session.commit()
                flash('File analyzed successfully! Agents have finished processing. Cost: 1 Credit.', 'success')
                return redirect(url_for('reports'))
            except Exception as e:
                flash(f'Error processing dataset: {str(e)}', 'danger')
                return redirect(request.url)
        else:
            flash('Invalid dataset selected.', 'danger')
            return redirect(request.url)
            
    return render_template('analysis.html', datasets=datasets)

# Analytics Subroutes
@app.route("/visualizations")
@login_required
def visualizations():
    reports = get_reports(current_user)
    return render_template('visualizations.html', reports=reports)
    
@app.route("/insights")
@login_required
def insights():
    reports = get_reports(current_user)
    # Unpack JSON insights for the view
    processed_reports = []
    for r in reports:
        insights_list = json.loads(r.insights_content) if r.insights_content else []
        processed_reports.append({"id": r.id, "filename": r.filename, "date_posted": r.date_posted, "insights": insights_list})
    return render_template('insights.html', reports=processed_reports)
    
@app.route("/recommendations")
@login_required
def recommendations():
    reports = get_reports(current_user)
    return render_template('recommendations.html', reports=reports)


@app.route("/reports")
@login_required
def reports():
    reports_list = get_reports(current_user)
    return render_template('reports_list.html', reports=reports_list)

@app.route("/report/<int:report_id>")
@login_required
def report_view(report_id):
    report = db.session.get(AnalysisReport, report_id)
    if not report:
        flash('Report not found', 'danger')
        return redirect(url_for('reports'))
        
    if current_user.role == 'manager':
        users = [u.id for u in User.query.filter_by(company_name=current_user.company_name).all()]
        if report.user_id not in users:
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('reports'))
    elif current_user.role == 'user':
        if report.user_id != current_user.id:
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('reports'))
            
    alerts_list = json.loads(report.alerts_data) if report.alerts_data else []
    forecast_dict = json.loads(report.forecast_data) if report.forecast_data else {}
            
    return render_template('report.html', report=report, alerts=alerts_list, forecasts=forecast_dict)

@app.route("/report/<int:report_id>/download")
@login_required
def download_report(report_id):
    report = db.session.get(AnalysisReport, report_id)
    if not report:
        flash('Report not found', 'danger')
        return redirect(url_for('reports'))
        
    if current_user.role == 'manager':
        users = [u.id for u in User.query.filter_by(company_name=current_user.company_name).all()]
        if report.user_id not in users:
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('reports'))
    elif current_user.role == 'user':
        if report.user_id != current_user.id:
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('reports'))

    insights_list = json.loads(report.insights_content) if report.insights_content else []
    
    chart_absolute = ""
    if report.chart_path:
        path = os.path.abspath(os.path.join(app.root_path, 'static', 'charts', report.chart_path))
        chart_absolute = "file:///" + path.replace('\\', '/')

    html_string = render_template('pdf_report.html', report=report, insights=insights_list, chart_absolute_path=chart_absolute)
    
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    with open(temp_pdf.name, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(html_string, dest=result_file)
        
    if pisa_status.err:
        flash('Error generating PDF.', 'danger')
        return redirect(url_for('report_view', report_id=report.id))
        
    return send_file(temp_pdf.name, as_attachment=True, download_name=f"Nexus_Report_{report.filename}.pdf", mimetype='application/pdf')


@app.route("/ask-ai", methods=['GET'])
@login_required
def ask_ai():
    reports = get_reports(current_user)
    return render_template('ask_ai.html', reports=reports)

@app.route("/api/chat", methods=['POST'])
@login_required
def api_chat():
    data = request.json
    question = data.get('question', '')
    report_id = data.get('report_id')
    
    report = db.session.get(AnalysisReport, report_id)
    if not report:
        return jsonify({"error": "Report not found"}), 404
        
    if current_user.role == 'manager':
        users = [u.id for u in User.query.filter_by(company_name=current_user.company_name).all()]
        if report.user_id not in users:
            return jsonify({"error": "Unauthorized"}), 403
    elif current_user.role == 'user':
        if report.user_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403
            
    agent = ChatAgent()
    answer = agent.execute(question, report.memory_context)
    
    return jsonify({"answer": answer})


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.company_name = request.form.get('company_name', 'Nexus AI')
        current_user.theme_color = request.form.get('theme_color', '#2f81f7')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route("/admin")
@login_required
def admin():
    if current_user.role != 'admin':
        flash('Access Denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    reports = AnalysisReport.query.all()
    return render_template('admin.html', users=users, total_reports=len(reports))

@app.route("/admin/add_credits/<int:user_id>", methods=['POST'])
@login_required
def admin_add_credits(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    amount = int(request.form.get('amount', 50))
    user = db.session.get(User, user_id)
    if user:
        user.credits += amount
        db.session.commit()
        flash(f'Successfully added {amount} credits to {user.username}.', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
