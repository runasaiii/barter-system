from django.shortcuts import render, redirect, get_object_or_404
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return render(request, 'ads/ad_created.html', {'ad': ad})
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})

def ad_list(request):
    ads = Ad.objects.all().order_by('-created_at')

    query = request.GET.get('q', '')  
    category = request.GET.get('category', '')  
    condition = request.GET.get('condition', '')  

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if category:
        ads = ads.filter(category=category)

    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 10)
    page = request.GET.get('page')

    try:
        ads = paginator.page(page)
    except PageNotAnInteger:
        ads = paginator.page(1)
    except EmptyPage:
        ads = paginator.page(paginator.num_pages)

    context = {
        'ads': ads,
        'query': query,
        'category': category,
        'condition': condition,
    }
    return render(request, 'ads/ad_list.html', context)

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    is_author = request.user == ad.user if request.user.is_authenticated else False
    return render(request, 'ads/ad_detail.html', {'ad': ad, 'is_author': is_author})

@login_required
def create_proposal(request, ad_id):
    ad_receiver = get_object_or_404(Ad, id=ad_id)
    user_ads = Ad.objects.filter(user=request.user).exclude(id=ad_receiver.id)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_receiver = ad_receiver
            proposal.save()
            return redirect('ad_detail', pk=ad_id)
    else:
        form = ExchangeProposalForm()
        form.fields['ad_sender'].queryset = user_ads

    return render(request, 'ads/create_proposal.html', {'form': form, 'ad_receiver': ad_receiver})

@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать это объявление.")

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            ad = form.save()
            return redirect('ad_detail', pk=ad.id)
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/edit_ad.html', {'form': form, 'ad': ad})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if ad.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")

    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')

    return render(request, 'ads/confirm_delete.html', {'ad': ad})

@login_required
def proposals_for_user(request):
    proposals = ExchangeProposal.objects.filter(ad_receiver__user=request.user).order_by('-created_at')
    return render(request, 'ads/proposals_list.html', {'proposals': proposals})

@login_required
@require_POST
def handle_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, ad_receiver__user=request.user)

    action = request.POST.get('action')
    if action == 'accept':
        proposal.status = 'accepted'
    elif action == 'decline':
        proposal.status = 'declined'
    proposal.save()
    return redirect('proposals_for_user')
