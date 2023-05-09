from .models import ExtraInfo
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class ExtraInfoForm(ModelForm):
    """
    The fields on this form are derived from the ExtraInfo model in models.py.
    """
    def __init__(self, *args, **kwargs):
        super(ExtraInfoForm, self).__init__(*args, **kwargs)
        self.fields['mobile'].error_messages = {
            "required": u"Please provide your mobile number.",
            "invalid": u"The mobile number you have entered is invalid.",
        }

    class Meta(object):
        model = ExtraInfo
        fields = ('mobile',)

    def check_mobile(self, mobile):
        if mobile.isnumeric():
            check_list = [6, 7, 8, 9]
            if int(str(mobile)[0]) in check_list:
                return mobile
            else:
                raise ValidationError("Mobile number should start with 6 or 7 or 8 or 9")
        else:
            raise ValidationError("No special character allowed in mobile number")

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', False)
        if not mobile.isalpha():
            if len(str(mobile)) == 10 or len(str(mobile)) == 13:
                if len(str(mobile)) == 13 and str(mobile).startswith("+91"):
                    self.check_mobile(str(mobile)[-10])
                else:
                    if len(str(mobile)) == 10:
                        self.check_mobile(mobile)
                    else:
                        raise ValidationError("Mobile number length should be 10 digit or should starts with +91")
            else:
                raise ValidationError("Mobile number length should be 10 digit or 13 digits")
        else:
            raise ValidationError("Mobile number should not be text")
        return mobile