from rest_framework.routers import DefaultRouter


class NoPutRouter(DefaultRouter):
    """
    Router class that disables the PUT method.
    """
    def get_method_map(self, viewset, method_map):

        bound_methods = super().get_method_map(viewset, method_map)

        if 'put' in bound_methods.keys():
            bound_methods.pop('put', None)
        return bound_methods
