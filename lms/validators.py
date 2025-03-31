import re
from rest_framework.serializers import ValidationError


class VideoUrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r'^(https?:\/\/)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]*$')
        tmp_val = dict(value).get(self.field)
        if not bool(reg.match(tmp_val)) or not value or value is None:
            raise ValidationError('Url неверный')
        elif 'youtube.com' not in tmp_val:
            raise ValidationError('Ссылка на видео только с youtube.com')
