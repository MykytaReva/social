from .models import Profile, RelationShip


def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.avatar
        return {'picture': pic}
    else:
        return {}

def invitations_received_no(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = RelationShip.objects.invitation_received(profile_obj).count()
        return {'invites_num': qs_count}
    return {}