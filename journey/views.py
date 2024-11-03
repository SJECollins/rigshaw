from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Journey, Request, Meeting
from .forms import JourneyForm, RequestForm, MeetingForm


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'journey/home.html')
    
    upcoming_journey = Journey.objects.filter(
        Q(creator=request.user, status=0) |
        Q(request__requester=request.user, request__status__in=[0, 1], status=0)
    ).first()
    journeys = []
    
    search = request.GET.get('search')
    if search:
        journeys = Journey.objects.filter(title__icontains=search)
        messages.info(request, f'Search results for "{search}"')
    else:
        journeys = Journey.objects.filter(status=0)
        
    context = {
        'upcoming_journey': upcoming_journey,
        'journeys': journeys
    }
    return render(request, 'journey/home.html', context)


@login_required
def my_journeys(request):
    journeys = Journey.objects.filter(creator=request.user)
    requests = Request.objects.filter(requester=request.user)
    context = {
        'journeys': journeys,
        'requests': requests
    }
    return render(request, 'journey/user_journeys.html', context)


@login_required
def create_journey(request):
    if request.method == 'POST':
        journey_form = JourneyForm(request.POST)
        meeting_form = MeetingForm(request.POST)

        if journey_form.is_valid():
            journey = journey_form.save(commit=False)
            journey.creator = request.user
            journey.save()

            if meeting_form.is_valid():
                if any(meeting_form.cleaned_data.values()):
                    meeting = meeting_form.save(commit=False)
                    meeting.journey = journey
                    meeting.user = request.user
                    meeting.save()
            else:
                messages.error(request, 'Error creating meeting, please try again')

            messages.success(request, 'Journey created')
            return redirect('home')
        else:
            location_errors = False
            for field, errors in journey_form.errors.items():
                if 'long' in field or 'lat' in field:
                    location_errors = True
                    continue
                for error in errors:
                    print(error)
                    messages.error(request, f"{field}: {error}")
            if location_errors:
                    messages.error(request, 'Please select a start location and destination from the map')
                    
    else:
        journey_form = JourneyForm()
        meeting_form = MeetingForm()

    return render(request, 'journey/create_journey.html', {
        'journey_form': journey_form,
        'meeting_form': meeting_form
    })


@login_required
def update_journey(request, pk):
    journey = Journey.objects.get(pk=pk)
    if request.method == 'POST':
        journey_form = JourneyForm(request.POST, instance=journey)

        if journey_form.is_valid():
            journey_form.save()

            messages.success(request, 'Journey updated')
            return redirect('home')
        else:
            messages.error(request, 'Journey update failed')
            for field, errors in journey_form.errors.items():
                print(field)
                for error in errors:
                    print(error)
    else:
        journey_form = JourneyForm(instance=journey)
    context = {
        'journey_form': journey_form,
        'journey': journey
    }
    return render(request, 'journey/update_journey.html', context)


@login_required
def cancel_journey(request, pk):
    journey = Journey.objects.get(pk=pk)
    journey.cancelled_time = datetime.now()
    journey.status = 3
    journey.save()
    messages.success(request, 'Journey cancelled')
    return redirect('home')


@login_required
def journey_detail(request, pk):
    journey = Journey.objects.get(pk=pk)
    requests = Request.objects.filter(journey=journey)
    meetings = Meeting.objects.filter(journey=journey)
    active_meetings = meetings.filter(status=1).first()
    can_join = True
    if request.user == journey.creator:
        can_join = False
    else:
        for req in requests:
            if req.requester == request.user:
                can_join = False
                break
    context = {
        'journey': journey,
        'requests': requests,
        'meetings': meetings,
        'active_meetings': active_meetings,
        'can_join': can_join
    }
    return render(request, 'journey/journey.html', context)


@login_required
def create_request(request, pk):
    journey = Journey.objects.get(pk=pk)
    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        meeting_form = MeetingForm(request.POST)
        if request_form.is_valid():
            req = request_form.save(commit=False)
            req.requester = request.user
            req.journey = journey
            req.save()
            if meeting_form.is_valid():
                if any(meeting_form.cleaned_data.values()):
                    meeting = meeting_form.save(commit=False)
                    meeting.journey = journey
                    meeting.request = req
                    meeting.user = request.user
                    meeting.save()
            else:
                messages.error(request, 'Error creating meeting, please try again')


            messages.success(request, 'Request created')
            return redirect('home')
        else:
            messages.error(request, 'Request creation failed')
            for field, errors in request_form.errors.items():
                print(field)
                for error in errors:
                    print(error)
    else:
        request_form = RequestForm()
        meeting_form = MeetingForm()
    context = {
        'request_form': request_form,
        'meeting_form': meeting_form,
        'journey': journey
    }
    return render(request, 'journey/create_request.html', context)


@login_required
def update_request(request, pk):
    request = Request.objects.get(pk=pk)
    if request.method == 'POST':
        request_form = RequestForm(request.POST, instance=request)

        if request_form.is_valid():
            request_form.save()

            messages.success(request, 'Request updated')
            return redirect('home')
        else:
            messages.error(request, 'Request update failed')
            for field, errors in request_form.errors.items():
                print(field)
                for error in errors:
                    print(error)
    else:
        request_form = RequestForm(instance=request)
    context = {
        'request_form': request_form,
        'request': request
    }
    return render(request, 'journey/update_request.html', context)


@login_required
def withdraw_request(request, pk):
    request = Request.objects.get(pk=pk)
    request.withdraw_message = request.POST.get('withdraw_message')
    request.status = 3
    request.save()
    messages.success(request, 'Request withdrawn')
    return redirect('home')


@login_required
def accept_request(request, pk):
    request = Request.objects.get(pk=pk)
    request.status = 2
    request.save()
    messages.success(request, 'Request accepted')
    return redirect('home')


@login_required
def reject_request(request, pk):
    request = Request.objects.get(pk=pk)
    request.status = 1
    request.save()
    messages.success(request, 'Request rejected')
    return redirect('home')


@login_required
def create_meeting(request, pk):
    journey = Journey.objects.get(pk=pk)

    if request.method == 'POST':
        meeting_form = MeetingForm(request.POST)

        if meeting_form.is_valid():
            meeting = meeting_form.save(commit=False)
            meeting.journey = journey
            meeting.user = request.user
            meeting.save()

            messages.success(request, 'Meeting created')
            return redirect('home')
        else:
            messages.error(request, 'Meeting creation failed')
            for field, errors in meeting_form.errors.items():
                print(field)
                for error in errors:
                    print(error)
    else:
        meeting_form = MeetingForm()
    context = {
        'meeting_form': meeting_form,
        'journey': journey
    }
    return render(request, 'journey/create_meeting.html', context)


@login_required
def update_meeting(request, pk):
    meeting = Meeting.objects.get(pk=pk)
    if request.method == 'POST':
        meeting_form = MeetingForm(request.POST, instance=meeting)

        if meeting_form.is_valid():
            meeting_form.save()

            messages.success(request, 'Meeting updated')
            return redirect('home')
        else:
            messages.error(request, 'Meeting update failed')
            for field, errors in meeting_form.errors.items():
                print(field)
                for error in errors:
                    print(error)
    else:
        meeting_form = MeetingForm(instance=meeting)
    context = {
        'meeting_form': meeting_form,
        'meeting': meeting
    }
    return render(request, 'journey/update_meeting.html', context)


@login_required
def accept_meeting(request, pk):
    meeting = Meeting.objects.get(pk=pk)
    meeting.status = 1
    meeting.save()
    messages.success(request, 'Meeting accepted')
    return redirect('home')


@login_required
def reject_meeting(request, pk):
    meeting = Meeting.objects.get(pk=pk)
    meeting.status = 2
    meeting.save()
    messages.success(request, 'Meeting rejected')
    return redirect('home')