from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic.base import TemplateResponseMixin

from ephios.event_management.models import Event
from ephios.extra.permissions import CustomPermissionRequiredMixin


class EventBulkDeleteView(CustomPermissionRequiredMixin, TemplateResponseMixin, View):
    permission_required = "event_management.delete_event"
    template_name = "event_management/event_bulk_delete.html"

    def post(self, request, *args, **kwargs):
        events = Event.objects.filter(pk__in=request.POST.getlist("bulk_action"))
        if not events:
            messages.info(request, _("No events were selected for deletion."))
            return redirect(reverse("event_management:event_list"))
        if request.POST.get("confirm"):
            events.delete()
            messages.info(request, _("The selected events have been deleted."))
            return redirect(reverse("event_management:event_list"))
        return self.render_to_response({"events": events})
