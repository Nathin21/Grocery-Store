from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GS.db'
app.config['SECRET_KEY'] = '1234'
db = SQLAlchemy(app)

# Database models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)  # This is the available stock for the product
    unit = db.Column(db.String(10), nullable=False)  # Unit: 'each' or 'kg'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    products = db.Column(db.Text, nullable=False)  # Stores product details in JSON format

# Routes
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)



@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        unit = request.form['unit']

        new_product = Product(name=name, price=price, quantity=0, unit=unit)  # Set quantity to 0, as it's managed separately
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!')
        return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        
        # Get form data, without 'quantity'
        
        name = request.form.get('name')
        price = request.form.get('price')
        unit = request.form.get('unit')

        # Update product data (without quantity)
        
        product.name = name
        product.price = price
        product.unit = unit

        try:
            db.session.commit()
            flash("Product updated successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "danger")

    return render_template('update_product.html', product=product)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('index'))

@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        # Get customer name
        customer_name = request.form.get('customer_name')
        
        # Validate customer name
        
        if not customer_name.strip():
            flash('Customer name is required!', 'danger')
            return redirect(url_for('place_order'))
        
        # Get selected product IDs and their quantities
        
        selected_products = []
        total_price = 0

        for product in Product.query.all():
            quantity = request.form.get(f'quantity_{product.id}')
            if quantity and int(quantity) > 0:
                quantity = int(quantity)
                total_price += product.price * quantity
                selected_products.append(f"{product.name} ({quantity}{product.unit})")
        
        if selected_products:
            # Save the order to the database
            new_order = Order(
                customer_name=customer_name,
                total_price=total_price,
                products=', '.join(selected_products)
            )
            db.session.add(new_order)
            db.session.commit()
            flash('Order placed successfully!', 'success')
        else:
            flash('Please select at least one product to place the order.', 'danger')

        return redirect(url_for('index'))

    # For GET requests, fetch all products
    products = Product.query.all()
    return render_template('place_order.html', products=products)




@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
