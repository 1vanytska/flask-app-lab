from flask import Blueprint

order_bp = Blueprint("orders", 
                    __name__, 
                    url_prefix="/order",
                    template_folder="templates/orders",
                    static_folder="static",
                    static_url_path="/static_for_orders")

from . import views