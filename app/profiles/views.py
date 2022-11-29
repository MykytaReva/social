from django.shortcuts import render
from .models import Profile, RelationShip
from .forms import PrifileModelForm
from django.views import generic
from django.contrib.auth.models import User


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

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = RelationShip.objects.invitation_received(profile)

    context = {
        'qs': qs
    }

    return render(request, 'profiles/my_invites.html', context)


def invite_profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'qs': qs,
    }

    return render(request, 'profiles/to_invite_list.html', context)


class ProfileListView(generic.ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'


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
