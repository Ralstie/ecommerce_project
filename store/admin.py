from django.contrib import admin
from .models import (
    UserProfile,
    Store,
    Product,
    Order,
    OrderItem,
    Review
)


admin.site.register(UserProfile)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)


