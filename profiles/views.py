from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserProfile
from journey.models import Journey
from .forms import UserProfileUpdateForm


class UpdateProfile(LoginRequiredMixin, generic.UpdateView):
    model = UserProfile
    form = UserProfileUpdateForm
    fields = ['name', 'phone', 'picture']
    template_name = 'profiles/update_profile.html'
    
    def get_object(self):
        return self.request.user.userprofile
    
    
def profile(request, pk):
    profile = UserProfile.objects.get(pk=pk)
    total_journeys = Journey.objects.filter(creator=request.user).count()
    # Get the last journey they created or the last they took part in?
    last_journey = Journey.objects.filter(creator=request.user, status=2).first()
    context = {
        'profile': profile,
        'total_journeys': total_journeys,
        'last_journey': last_journey,
    }
    return render(request, 'profiles/profile.html', context)
