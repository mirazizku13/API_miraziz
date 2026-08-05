from rest_framework.throttling import UserRateThrottle


class CarCreateThrottle(UserRateThrottle):
    scope = "post_create"