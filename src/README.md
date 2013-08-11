
rhino website
=====

初始化工程

    1. pip install -r requirements.txt
    2. 在rhino下新建一个local_settings.py, 和settings.py同级
    3. 在local_settings.py里配置自己的设置，如：
        ```
          DATABASES = {
            'default':  {
                  'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                  'NAME': 'rhino.db',                      # Or path to database file if using sqlite3.
                  # The following settings are not used with sqlite3:
                  'USER': 'root',
                  'PASSWORD': '',
                  'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                  'PORT': '',                      # Set to empty string for default.
            }
          }
        ```
        注意：local_settings.py里的设置会覆盖settings.py，默认git会ignore这个文件，请不要提交这个文件
    4. python manage.py syncdb, 是否建立管理员用户随便你

本地运行

    1. python manage.py runserver
    2. 建议用Chrome，打开Chrome的开发工具，在设置中选择：开发工具下不使用缓存
    3. 如果使用其他浏览器，在更新JS文件以后请积极清理缓存
    3. 访问http://127.0.0.1:8000

注意事项

    1. 增加的js记得加入index.html


