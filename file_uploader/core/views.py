import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from core.models import File
from django.shortcuts import redirect
from django.utils import timezone
from core.forms import SearchForm
from core.parse import parse_pdf
from elasticsearch import Elasticsearch
import logging

logger = logging.getLogger("custom")

es = Elasticsearch([os.environ["ELASTICSEARCH_HOST"]])


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            files_from_content = []
            files_saved = list(
                File.objects.filter(name__icontains=form.cleaned_data["file_name"])
            )
            results = es.search(
                index="",
                body={
                    "query": {"query_string": {"query": form.cleaned_data["file_name"]}}
                },
            )
            if results["hits"]["total"]["value"] > 0:
                logger.info("find_documents")
                files_ids = []
                for result in results["hits"]["hits"]:
                    logger.info(result)
                    files_ids.append(result["_source"]["file_id"])

                files_from_content = list(File.objects.filter(id__in=files_ids))

            return render(
                request,
                "index.html",
                {"show_files": True, "files_saved": files_from_content + files_saved},
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
        parse_pdf(file.id, schedule=1)
        return redirect("/")
    return render(request, "index.html", {"upload_file": True})
