from django.shortcuts import redirect


def redirect_to_content(request):
    return redirect('files_manager-files_list', permanent=True)
