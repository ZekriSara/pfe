from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, 'Admin/home/page-404.html', status=404)