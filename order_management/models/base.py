from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""万一哪天需要扩展，就可以直接在这里扩展，使用了这个Base地方都会被更改"""