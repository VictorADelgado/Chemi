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
def calculate_stoichiometry(equation,given_substance,given_mol_number,target_substance):
    reactants, products = equation.split('->')
    reactants = [r.strip() for r in reactants.split('+')]
    products = [p.strip() for p in products.split('+')]
    balanced_reactants, balanced_products = balance_stoichiometry(reactants, products)
    sreactants = {comp: int(coef) for comp, coef in balanced_reactants.items()}
    sproducts = {comp: int(coef) for comp, coef in balanced_products.items()}
    balanced_compounds = {**sreactants, **sproducts}
    target_mol_number = None
    q = None
    if given_substance in balanced_compounds and target_substance in balanced_compounds:
        given_coefficient = balanced_compounds[given_substance]
        target_coefficient = balanced_compounds[target_substance]
        target_mol_number = (given_mol_number * target_coefficient) / given_coefficient
        return target_mol_number




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
        return render_template('molar-mass.html', title='Calculate Molar Mass', molar_mass=molar_mass,formula=formula,molar_mass_history=session['molar_mass_history'])
    return render_template('molar-mass.html', title='Calculate Molar Mass')
@app.route('/calculate/stoichiometry', methods=['GET', 'POST'])
def stoichiometry():
    if 'stoichiometry_history' not in session:
        session['stoichiometry_history'] = []
    equation = None
    given_substance = None
    given_mol_number = None
    target_substance = None
    target_mol_number = None
    if request.method == 'POST':
        equation = request.form.get('equation')
        given_substance = request.form.get('given_substance')
        given_mol_number = float(request.form.get('given_mol_number'))
        target_substance = request.form.get('target_substance')
        if equation and given_substance and given_mol_number and target_substance:
            target_mol_number = calculate_stoichiometry(equation, given_substance, given_mol_number, target_substance)
            current_history = session['stoichiometry_history']
            current_history.append({
                'equation': equation,
                'given_substance': given_substance,
                'given_mol_number': given_mol_number,
                'target_substance': target_substance,
                'target_mol_number': target_mol_number
            })
            session['stoichiometry_history'] = current_history[-5:]
            session.modified = True
        else:
            return render_template('stoichio.html', title='Calculate Stoichiometry', error='Please fill in all fields.')
        return render_template('stoichio.html', title='Calculate Stoichiometry', equation=equation,given_substance=given_substance,given_mol_number=given_mol_number,target_substance=target_substance,target_mol_number=target_mol_number,stoichiometry_history=session['stoichiometry_history'])
    return render_template('stoichio.html', title='Calculate Stoichiometry')
if __name__ == '__main__':
    app.run(debug=True)