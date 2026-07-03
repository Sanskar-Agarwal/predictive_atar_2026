from django.http import JsonResponse


class CustomErrorException(Exception):
    def __init__(self, message="Custom error occurred", *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)

def handle_errors(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            #
            return view_func(request, *args, **kwargs)

        except CustomErrorException as e:
            #
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            #
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    return _wrapped_view
