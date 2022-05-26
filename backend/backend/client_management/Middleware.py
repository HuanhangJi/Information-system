# import re
# from django.shortcuts import *
#
#
# class ProMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         path = request.path
#         white_urls = []
#         if re.match(r'^', path) and path not in white_urls:
#             if 'producer' not in request.session:
#                 return redirect()
#
#         response = self.get_response(request)
#         return response
