from django.views.decorators.csrf import csrf_exempt
from reservation.models import Reservation
import json
from django.utils import timezone
from django.http import JsonResponse
from django.utils import timezone


@csrf_exempt
def enter_parking(request):
    request_body = request.body.decode('utf-8')
    data = json.loads(request_body)
    current_user = request.user
    # you cannot enter the parking slot if the slot isn't freed yet
    if Reservation.objects.filter(
        parking_slot_id=data.get('parking_slot_id'),
        enter_date__isnull=False,
        finish_date__gt=timezone.now()
        ).exists():
        return JsonResponse({"result": "This Parking is still occupied!"})
    reserved_parking = Reservation.objects.filter(
        user_id=current_user.id, parking_slot_id=data.get('parking_slot_id')
    )
    if reserved_parking:
        reserved_parking.update(enter_date=timezone.now(), exit_date=None)
        return JsonResponse({"result": "your enter has been recorded"})
    return JsonResponse({"result": "you don't have a reservation"})