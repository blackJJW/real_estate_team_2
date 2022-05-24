from flask import Flask
from flask import Blueprint
from . import house_welfare
from . import main_menu
from . import house_welfare_detail

application = Flask(__name__)

# ----- register -------------------------------------------------------------------------------
application.register_blueprint(house_welfare.blue_house_welfare)
application.register_blueprint(main_menu.blue_main_menu)
application.register_blueprint(house_welfare_detail.blue_house_welfare_detail)
# ----------------------------------------------------------------------------------------------