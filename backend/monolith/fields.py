from django.db import models

from .crypto import blind_index, decrypt, encrypt, fernet


class EncryptedMixin:
    def db_type(self, connection):
        return "text"

    def get_db_prep_value(self, value, connection, prepared=False):
        value = self.get_prep_value(value)
        return None if value is None else encrypt(str(value))

    def from_db_value(self, value, expression, connection):
        return None if value is None else self.to_python(decrypt(value))


class EncryptedCharField(EncryptedMixin, models.CharField):
    pass


class EncryptedTextField(EncryptedMixin, models.TextField):
    pass


class EncryptedDateField(EncryptedMixin, models.DateField):
    pass


class EncryptedBinaryField(models.BinaryField):
    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        encrypted = fernet().encrypt(bytes(value))
        return super().get_db_prep_value(encrypted, connection, prepared)

    def from_db_value(self, value, expression, connection):
        return None if value is None else fernet().decrypt(bytes(value))


class HashField(models.CharField):
    def __init__(self, source, **kwargs):
        self.source = source
        kwargs.setdefault("max_length", 64)
        kwargs.setdefault("editable", False)
        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, {**kwargs, "source": self.source}

    def pre_save(self, model_instance, add):
        value = blind_index(getattr(model_instance, self.source))
        setattr(model_instance, self.attname, value)
        return value
