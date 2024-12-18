from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from ..models import Zajęcia, Sala, Samochód, Użytkownik, KursanciNaZajęciach


@login_required
@require_POST
def transakcja(request, zajęcia_id, kursant_id):
    try:
        # Pobranie zajęć, sali, samochodu i użytkownika
        zajęcia = Zajęcia.objects.get(id=zajęcia_id)
        kursant = Użytkownik.objects.get(id=kursant_id)

        sala = zajęcia.sala
        samochód = zajęcia.samochód

    except (Zajęcia.DoesNotExist, Użytkownik.DoesNotExist, Sala.DoesNotExist, Samochód.DoesNotExist) as e:
        return JsonResponse({"error": f"Nie znaleziono wymaganych danych: {str(e)}"}, status=404)

    # Rozpoczęcie transakcji
    try:
        with transaction.atomic():
            # 1. Sprawdzenie dostępności miejsc w sali
            if sala.remaining_seats > 0:
                sala.remaining_seats -= 1  # Decrement remaining seats
                sala.save()
            else:
                raise Exception("Brak dostępnych miejsc w sali.")

            # 2. Sprawdzenie dostępności samochodu
            if samochód.availability:
                samochód.availability = False  # Mark the car as unavailable
                samochód.save()
            else:
                raise Exception("Samochód jest już niedostępny.")

            # 3. Zaktualizowanie godzin lekcji kursanta
            kursant.godziny_lekcji_praktycznych += 1  # Przykładowo, dodajemy 1 godzinę lekcji praktycznych
            kursant.save()

            return JsonResponse({"message": "Transakcja zakończona sukcesem!"}, status=201)

    except Exception as e:
        # Jeśli jakikolwiek błąd wystąpi, cała transakcja zostanie wycofana
        return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=400)

@login_required
@require_POST
def zakoncz_zajecia(request, zajęcia_id, kursant_id):
    try:
        # Pobranie zajęć i użytkownika
        zajęcia = Zajęcia.objects.get(id=zajęcia_id)
        kursant = Użytkownik.objects.get(id=kursant_id)

        # Sprawdzenie, czy kursant jest zapisany na te zajęcia
        if not KursanciNaZajęciach.objects.filter(użytkownik=kursant, zajęcia=zajęcia).exists():
            return JsonResponse({"error": "Kursant nie jest zapisany na te zajęcia."}, status=400)

    except (Zajęcia.DoesNotExist, Użytkownik.DoesNotExist) as e:
        return JsonResponse({"error": f"Nie znaleziono wymaganych danych: {str(e)}"}, status=404)

    try:
        # Rozpoczęcie transakcji
        with transaction.atomic():
            if zajęcia.sala:  # Zajęcia teoretyczne
                if kursant.posiadane_lekcje_teoretyczne <= 0:
                    return JsonResponse({"error": "Brak dostępnych godzin teoretycznych."}, status=400)

                # Aktualizacja godzin teoretycznych
                kursant.godziny_lekcje_teoretyczne += 1
                kursant.posiadane_lekcje_teoretyczne -= 1

            elif zajęcia.samochód:  # Zajęcia praktyczne
                if kursant.posiadane_lekcje_praktyczne <= 0:
                    return JsonResponse({"error": "Brak dostępnych godzin praktycznych."}, status=400)

                # Aktualizacja godzin praktycznych
                kursant.godziny_lekcji_praktycznych += 1
                kursant.posiadane_lekcje_praktyczne -= 1

            # 2. Usunięcie zajęć
            zajęcia.delete()

            return JsonResponse({"message": "Transakcja zakończona sukcesem!"}, status=201)

    except Exception as e:
        # Jeśli wystąpi jakikolwiek błąd, cała transakcja zostanie wycofana
        return JsonResponse({"error": f"Wystąpił błąd: {str(e)}"}, status=400)

