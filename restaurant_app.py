from flask import Flask, render_template, request, url_for, abort, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sushi_model import Base_sushi, Sushi
from main_plate_model import Base_main_plate, Plate
from order_model import Base_order, Order


app = Flask(__name__)

engine_orders = create_engine("sqlite:///orders.db", echo=True)
engine_main_plates = create_engine("sqlite:///main_plates.db", echo=True)
engine_sushis = create_engine("sqlite:///sushis.db", echo=True)

Base_order.metadata.create_all(bind=engine_orders)
Base_main_plate.metadata.create_all(bind=engine_main_plates)
Base_sushi.metadata.create_all(bind=engine_sushis)

SessionOrders = sessionmaker(bind=engine_orders)
SessionMainPlates = sessionmaker(bind=engine_main_plates)
SessionSushis = sessionmaker(bind=engine_sushis)

session_orders = SessionOrders()
session_main_plates = SessionMainPlates()
session_sushis = SessionSushis()


@app.route("/")
def welcome_page():
    return render_template("welcome.html", main_menu_ref = url_for("main_menu_page"))



@app.route("/regenerate_database/")
def regenerate_database():

    sushi_items = [
        Sushi(type="Salmon", image="/static/images/sushis/sushi_01.png", price = 11.6),
        Sushi(type="Crab", image="/static/images/sushis/sushi_02.png", price = 10.5),
        Sushi(type="Tuna", image="/static/images/sushis/sushi_03.png", price = 12.9),
        Sushi(type="Seaweed", image="/static/images/sushis/sushi_04.png", price = 9.3),
        Sushi(type="California", image="/static/images/sushis/sushi_05.png", price = 12.6)
    ]

    session_sushis.add_all(sushi_items)
    session_sushis.commit()

    menu_items = [
        Plate(type="Fried Egg Plant", image="/static/images/main_menu/fried_egg_plant.png", url=url_for("sushi_page")),
        Plate(type="Meat with Rice", image="/static/images/main_menu/meat_with_rice.png", url=url_for("sushi_page")),
        Plate(type="Oyacondon", image="/static/images/main_menu/oyacondon.png", url=url_for("sushi_page")),
        Plate(type="Rice with Beef", image="/static/images/main_menu/rice_with_beef.png", url=url_for("sushi_page")),
        Plate(type="Sushi", image="/static/images/main_menu/sushis.png", url=url_for("sushi_page"))
    ]

    session_main_plates.add_all(menu_items)
    session_main_plates.commit()
    return 'Regenerating Database... Thanks for the amazing class Professor Paulo!'


@app.route("/main_menu_page/")
def main_menu_page():
    mainPlatesINJSONFormat = []
    main_plates = session_main_plates.query(Plate).all()
    for plate in main_plates:
        mainPlatesINJSONFormat.append(plate.toJSON())
    return render_template("main_menu.html", plates=mainPlatesINJSONFormat)



@app.route("/sushis/")
def sushi_page():
    sushisINJSONFormat = []
    sushis = session_sushis.query(Sushi).all()
    for sushi in sushis:
        sushisINJSONFormat.append(sushi.toJSON())
    return render_template("sushi_menu.html", sushis=sushisINJSONFormat, order_request_ref=url_for("order_request"))



@app.route("/order_request", methods=["POST"])
def order_request():

    orders = request.form["order_summary"]

    new_order = Order(customer_name=request.form["customer_name"], orders=orders[0:len(orders)-2])

    try:
        session_orders.add(new_order)
        session_orders.commit()

        items = orders[0:len(orders)-2].split("\r\n")

        return render_template("order_summary.html", order_summary=items, customer_name=request.form["customer_name"])
    except:
        return "There was an issue adding your order"
    



@app.route("/kitchen/")
def kitchen():
    ordersINJSONFormat = []
    orders = session_orders.query(Order).all()
    for order in orders:
        ordersINJSONFormat.append(order.toJSON())

    return render_template("kitchen.html", orders=ordersINJSONFormat)



@app.route('/delete/<id>')
def delete(id):
    order_to_delete = session_orders.query(Order).get(id)
    if order_to_delete is None:
        abort(404)
    try:
        session_orders.delete(order_to_delete)
        session_orders.commit()
        return redirect(url_for("kitchen"))
    except:
        return 'There was a problem deleting that task'


if __name__ == "__main__":
    app.run(debug=True)