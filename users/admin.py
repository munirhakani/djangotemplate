from django.contrib import admin


from django.contrib.auth import get_user_model
User = get_user_model()
admin.site.unregister(User)


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as MyUser
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser', )
    class Meta:
        model = MyUser
admin.site.register(MyUser, MyUserAdmin)