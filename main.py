from chempy import balance_stoichiometry
from chempy.chemistry import Substance
from flask import Flask, render_template
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
    return render_template('index.html',title='Clemistry Suite')
if __name__ == '__main__':
    app.run(debug=True)
@app.route('/about')
def about():
    return render_template('index.html', title='About')