from chempy import balance_stoichiometry
from chempy.chemistry import Substance
from flask import Flask, render_template,request
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
@app.route('/')
def index():
    return render_template('index.html',title='Chemi')
@app.route('/about')
def about():
    return render_template('about.html', title='About')
@app.route('/calculate')
def calculate():
    return render_template('calculate.html', title='Calculate')
@app.route('/balance', methods=['POST'])
def balance():
    equation = request.form['equation']
    balanced_equation = balance_equation(equation)
    return render_template('balance.html', title='Balance Equation', balanced_equation=balanced_equation)
@app.route('/calculate-molar-mass', methods=['POST'])
def calculate_molar_mass_route():
    formula = request.form['formula']
    molar_mass = calculate_molar_mass(formula)
    return render_template('molar_mass.html', title='Calculate Molar Mass', molar_mass=molar_mass)

if __name__ == '__main__':
    app.run(debug=True)