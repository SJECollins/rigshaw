from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import Review
from journey.models import Journey


class MyReviewList(generic.ListView):
    model = Review
    template_name = 'review/review_list.html'
    context_object_name = 'reviews'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviewee'] = User.objects.get(username=self.kwargs['reviewee'])
        return context
    

class MyCreatedReviewList(generic.ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviewer'] = User.objects.get(username=self.kwargs['reviewer'])
        return context


class CreateReview(LoginRequiredMixin, generic.CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'review/create_review.html'

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        reviewee = self.kwargs['reviewee']
        form.instance.reviewee = User.objects.get(username=reviewee)
        journey = self.kwargs['journey']
        form.instance.journey = Journey.objects.get(pk=journey)
        return super().form_valid(form)
    

class UpdateReview(LoginRequiredMixin, generic.UpdateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'review/update_review.html'


class DeleteReview(LoginRequiredMixin, generic.DeleteView):
    model = Review
    template_name = 'review/delete_review.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = Review.objects.get(pk=self.kwargs['pk'])
        return context