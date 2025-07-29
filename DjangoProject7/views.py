from django import http


def message(request):
    return http.HttpResponse("Hello, world. You're at the message.")
