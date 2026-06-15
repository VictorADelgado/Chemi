from chempy import balance_stoichiometry
from chempy.chemistry import Substance
from flask import Flask, render_template,request,session,redirect,url_for
def balance_equation(equation):
    reactants, products = equation.split('->')
    reactants = [r.strip() for r in reactants.split('+')]
    products = [p.strip() for p in products.split('+')]
    
    balanced_reactants, balanced_products = balance_stoichiometry(reactants, products)
    
    balanced_equation = ' + '.join(f"{coef} {comp}" for comp, coef in balanced_reactants.items())
    balanced_equation += ' -> '
    balanced_equation += ' + '.join(f"{coef} {comp}" for comp, coef in balanced_products.items())
    
    return balanced_equation
def calculate_molar_mass(formula):
    substance = Substance.from_formula(formula)
    return substance.mass

app = Flask(__name__)
app.secret_key = 'IDontGetDoubleSenseJokes'
@app.route('/')
def index():
    return render_template('index.html',title='Chemi')
@app.route('/about')
def about():
    return render_template('about.html', title='About')
@app.route('/calculate')
def calculate():
    return render_template('calculate.html', title='Calculate')
@app.route('/calculate/balance', methods=['GET', 'POST'])
def balance():
    if 'balance_history' not in session:
        session['balance_history'] = []
    balanced_equation = None
    equation = None
    if request.method == 'POST':
        equation = request.form.get('equation')
        if equation:
            balanced_equation = balance_equation(equation)
            current_history = session['balance_history']
            current_history.append({
                'input': equation,
                'output': balanced_equation
            })
            session['balance_history'] = current_history[-5:]
            session.modified = True
        else:
            return render_template('balance.html', title='Balance Equation', error='Please enter a chemical equation.')
        return render_template('balance.html', title='Balance Equation', balanced_equation=balanced_equation,balance_history=session['balance_history'])
    return render_template('balance.html', title='Balance Equation')
@app.route('/calculate/molar-mass', methods=['GET', 'POST'])
def molar_mass():
    if 'molar_mass_history' not in session:
        session['molar_mass_history'] = []
    formula = None
    molar_mass = None
    if request.method == 'POST':
        formula = request.form.get('formula')
        if formula:
            molar_mass = calculate_molar_mass(formula)
            current_history = session['molar_mass_history']
            current_history.append({
                'formula': formula,
                'molar_mass': molar_mass
            })
            session['molar_mass_history'] = current_history[-5:]
            session.modified = True
        else:
            return render_template('molar-mass.html', title='Calculate Molar Mass', error='Please enter a chemical formula.')
        return render_template('molar-mass.html', title='Calculate Molar Mass', molar_mass=molar_mass,formula=formula)
    return render_template('molar-mass.html', title='Calculate Molar Mass')

if __name__ == '__main__':
    app.run(debug=True)