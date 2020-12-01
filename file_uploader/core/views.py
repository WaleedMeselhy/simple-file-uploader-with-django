from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
from core.models import File
from django.shortcuts import redirect
from core.forms import SearchForm


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            files_saved = list(File.objects.filter(name=form.cleaned_data["file_name"]))
            return render(
                request, "index.html", {"show_files": True, "files_saved": files_saved}
            )
    files_saved = list(File.objects.all())
    return render(
        request, "index.html", {"show_files": True, "files_saved": files_saved}
    )


def upload(request):
    if request.method == "POST" and request.FILES["myfile"]:
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        file = File(name=filename, file_path=uploaded_file_url)
        file.save()
        return redirect("/")
    return render(request, "index.html", {"upload_file": True})
