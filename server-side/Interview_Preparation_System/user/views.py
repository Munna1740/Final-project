from django.shortcuts import render, redirect

from .models import UserResume
from .models import UserInfo
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


# Create your views here.

def profile(request):
    return render(request, 'home.html')


def upload_resume(request):
    if request.method == "POST":
        file = request.FILES['resume_upload']
        if not UserResume.objects.filter(user=request.user).exists():
            resume = UserResume(resume=file, user=request.user)
            resume.save()

            user = UserResume.objects.get(user=request.user)
            resume = user.resume.path
            pdfTotext = convert_pdf_to_string(resume)
            wordList = pdfTotext.split()
            # list of letters
            cvWords = set(wordList)
            filteredSkills = filter(filterWords, cvWords)

            print('The filtered skills are:')
            skillset = ""
            for skills in filteredSkills:
                skillset += skills + ", "
                print(skills)
            print(skillset)
            userinfo = UserInfo(user=request.user, key_skills=skillset)
            userinfo.save()
        else:
            resume = UserResume.objects.get(user=request.user)
            resume.resume = file
            resume.save()

            user = UserResume.objects.get(user=request.user)
            resume = user.resume.path
            pdfTotext = convert_pdf_to_string(resume)
            wordList = pdfTotext.split()
            # list of letters
            cvWords = set(wordList)
            filteredSkills = filter(filterWords, cvWords)

            print('The filtered skills are:')
            skillset = ""
            for skills in filteredSkills:
                skillset += skills + ", "
                print(skills)
            print(skillset)
            userinfo = UserInfo.objects.get(user=request.user)
            userinfo.key_skills = skillset
            userinfo.save()

    return render(request, 'home.html', {'skillset': skillset})


def convert_pdf_to_string(file_path):
    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    return (output_string.getvalue())


def convert_title_to_filename(title):
    filename = title.lower()
    filename = filename.replace(' ', '_')
    return filename


def split_to_title_and_pagenum(table_of_contents_entry):
    title_and_pagenum = table_of_contents_entry.strip()

    title = None
    pagenum = None

    if len(title_and_pagenum) > 0:
        if title_and_pagenum[-1].isdigit():
            i = -2
            while title_and_pagenum[i].isdigit():
                i -= 1

            title = title_and_pagenum[:i].strip()
            pagenum = int(title_and_pagenum[i:].strip())

    return title, pagenum


# function that filters vowels
def filterWords(word):
    skills = ['Python', 'Django', 'CSS', 'React', 'HTML']

    if (word in skills):
        return True
    else:
        return False
