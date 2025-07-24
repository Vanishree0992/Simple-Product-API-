from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
api = Api(app)

products = []
product_id_counter = 1

class ProductListResource(Resource):
    def get(self):
        return {'products': products}, 200

    def post(self):
        global product_id_counter
        data = request.get_json()

        if not data or 'name' not in data or 'price' not in data or 'in_stock' not in data:
            raise BadRequest("Fields 'name', 'price', and 'in_stock' are required.")

        try:
            price = float(data['price'])
            if price <= 0:
                raise ValueError
        except ValueError:
            raise BadRequest("Price must be a number greater than 0.")

        new_product = {
            'id': product_id_counter,
            'name': data['name'],
            'price': price,
            'in_stock': bool(data['in_stock'])
        }
        products.append(new_product)
        product_id_counter += 1
        return new_product, 201

class ProductResource(Resource):
    def get(self, id):
        product = next((p for p in products if p['id'] == id), None)
        if not product:
            raise NotFound("Product not found.")
        return product, 200

    def put(self, id):
        data = request.get_json()
        product = next((p for p in products if p['id'] == id), None)
        if not product:
            raise NotFound("Product not found.")

        if 'name' in data:
            product['name'] = data['name']
        if 'price' in data:
            try:
                price = float(data['price'])
                if price <= 0:
                    raise ValueError
                product['price'] = price
            except ValueError:
                raise BadRequest("Price must be a number greater than 0.")
        if 'in_stock' in data:
            product['in_stock'] = bool(data['in_stock'])

        return product, 200

    def delete(self, id):
        global products
        product = next((p for p in products if p['id'] == id), None)
        if not product:
            raise NotFound("Product not found.")
        products = [p for p in products if p['id'] != id]
        return {'message': f'Product with id {id} deleted.'}, 200

# Register routes
api.add_resource(ProductListResource, '/products')
api.add_resource(ProductResource, '/products/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
