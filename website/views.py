from django.shortcuts import render
from website.models import Candidate
from .filters import RankingFilter
# Create your views here.



def index(request):
    return render(request, 'website/index.html')

def profile(request):
    return render(request, 'account/profile.html')

def contact(request):
    return render(request, 'website/contact.html')

def ranking(request):
    candidates = Candidate.objects.all()
    myFilter = RankingFilter(request.GET, queryset=candidates)
    candidates = myFilter.qs
    context = {
        'candidates':candidates,
        'myFilter':myFilter,
    }
    return render(request, 'website/ranking.html', context)