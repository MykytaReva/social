from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, RelationShip
from .forms import PrifileModelForm
from django.views import generic
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = PrifileModelForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form':form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)

@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = RelationShip.objects.invitation_received(profile)
    result = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(result) == 0:
        is_empty = True

    context = {
        'qs': result,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)

@login_required
def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(RelationShip, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
            return redirect('profiles:my-invites-view')
    return redirect('profiles:my-invites-view')

@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(RelationShip, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')

@login_required
def invite_profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'qs': qs,
    }

    return render(request, 'profiles/to_invite_list.html', context)


class ProfileListView(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'


    def post(self, request):
        if request.method == 'POST':
            return  render(request,'profiles/profile_list.html')
        return render(request,'profiles/profile_list.html')


    def get_context_data(self, *args, **kwargs):
        context: dict = super().get_context_data(*args, **kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = RelationShip.objects.filter(sender=profile)
        rel_s = RelationShip.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)

        for item in rel_s:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

@login_required
def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = RelationShip.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')

@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = RelationShip.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    # def get_object(self):
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = RelationShip.objects.filter(sender=profile)
        rel_s = RelationShip.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context["posts"] = self.get_object().get_all_authors_posts()
        context["len_posts"] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context
