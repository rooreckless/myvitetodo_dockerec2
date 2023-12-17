#app.py
#config切り替えにはconfig.pyのconfig辞書が使えればいい。
# from apps.config import config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# #SQLAlchemyをインスタンス化
db=SQLAlchemy()
#ブループリントback_appのviews.pyをインポート
from apps.back_app import views


def create_app(config_key):
  app=Flask(__name__)
  app.register_blueprint(views.back_app,url_prefix="/back_app")
  
  print("create_app----config_key=",config_key)
  if config_key == "local":
    app.debug = True  # デバッグモードを有効にする
  elif config_key == "product":
    app.debug = False  # デバッグモードを無効にする
  else:
    app.debug = False  # デバッグモードを無効にする
  #環境変数を読み込む(docker-composeのenv-fileを使っていることを前提)
  app.config["TESTING"] = os.getenv("TESTING")
  app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
  app.config["SQLALCHEMY_DATABASE_URI"] = 'mariadb+pymysql://'+os.getenv('MYSQL_USER')+':'+os.getenv('MYSQL_PASSWORD')+'@'+os.getenv('MYSQL_ENDPOINT')+'/'+os.getenv('MYSQL_DATABASE')
  app.config["WTF_CSRF_SECRET_KEY"] = os.getenv("WTF_CSRF_SECRET_KEY")  
  
  #SQLAlchemyとアプリを連携する初期化
  db.init_app(app)
  # #Migrateインスタンス作成 appとdbを入れて連携させる
  Migrate(app,db)
  #CORSも連携します
  # CORS(app, resources={"/back_app/*":{"origins":"http://tmp/gunicorn_flask.sock"}})
  # CORS(app, resources={"/back_app/*":{"origins":"http://vue:5173"}})
  CORS(app)
  return app
if __name__=="__main__":
    app=create_app()