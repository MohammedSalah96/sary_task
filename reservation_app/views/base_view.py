from rest_framework.views import APIView


class BaseView(APIView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        