from django import forms
from .models import Journey, Request, Meeting


class JourneyForm(forms.ModelForm):
    class Meta:
        model = Journey
        fields = ['title', 'date', 'time', 'start_location_long', 'start_location_lat', 'destination_long', 'destination_lat']
        labels = {
            'title': 'Title',
            'date': 'Date',
            'time': 'Time',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'start_location_long': forms.NumberInput(attrs={'class': 'form-control', 'type': 'hidden'}),
            'start_location_lat': forms.NumberInput(attrs={'class': 'form-control', 'type': 'hidden'}),
            'destination_long': forms.NumberInput(attrs={'class': 'form-control', 'type': 'hidden'}),
            'destination_lat': forms.NumberInput(attrs={'class': 'form-control', 'type': 'hidden'}),
        }
        

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request_message']
        labels = {
            'request_message': 'Message'
        }
        widgets = {
            'request_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
        

class MeetingForm(forms.ModelForm):
    
    class Meta:
        model = Meeting
        fields = ['description', 'meeting_time', 'meeting_location_long', 'meeting_location_lat']
        labels = {
            'description': 'Description',
            'meeting_time': 'Time',
        }
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'meeting_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'meeting_location_long': forms.NumberInput(attrs={'class': 'form-control', 'type': 'hidden'}),
            'meeting_location_lat': forms.NumberInput(attrs={'class': 'form-control', 'type': 'hidden'}),
        }

    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        self.fields['meeting_time'].required = False
        self.fields['meeting_location_lat'].required = False
        self.fields['meeting_location_long'].required = False