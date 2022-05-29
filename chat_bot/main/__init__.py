from flask import Flask
from flask import Blueprint
from . import house_welfare
from . import main_menu
from . import house_welfare_detail
from . import house_welfare_detail_1
from . import house_welfare_detail_2
from . import house_welfare_detail_3
from . import house_welfare_detail_4

application = Flask(__name__)

# ----- register -------------------------------------------------------------------------------
application.register_blueprint(house_welfare.blue_house_welfare)
application.register_blueprint(main_menu.blue_main_menu)
application.register_blueprint(house_welfare_detail.blue_house_welfare_detail)
application.register_blueprint(house_welfare_detail_1.blue_house_welfare_detail_1)
application.register_blueprint(house_welfare_detail_2.blue_house_welfare_detail_2)
application.register_blueprint(house_welfare_detail_3.blue_house_welfare_detail_3)
application.register_blueprint(house_welfare_detail_4.blue_house_welfare_detail_4)
# ----------------------------------------------------------------------------------------------