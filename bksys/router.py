class DBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'bksys':
            return 'rooms'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'bksys':
            return 'rooms'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'bksys' or obj2._meta.app_label == 'bksys':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'rooms':
            return model._meta.app_label == 'bksys'
        elif model._meta.app_label == 'bksys':
            return False
        return None