from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import VIN
from .schemas import VINSearchRequest, VINSearchResponse, VINAddRequest, VINSchema

Session = sessionmaker()
db_uri = f'sqlite:///{settings.DATABASES["default"]["NAME"]}'


@csrf_exempt
def add_vin(request):
    if request.method == 'POST':
        try:
            request_data = VINAddRequest(**json.loads(request.body))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': f'Invalid data: {e}'}, status=400)

        engine = create_engine(db_uri)
        Session.configure(bind=engine)
        session = Session()
        try:
            vin = VIN(
                version=request_data.version,
                equipment_code=request_data.equipment_code,
                year_of_issue=request_data.year_of_issue,
                serial_number=request_data.serial_number,
                place_of_production=request_data.place_of_production
            )
            session.add(vin)
            session.commit()
            return JsonResponse({'success': 'VIN entry added successfully'}, status=200)
        except Exception as e:
            session.rollback()
            return JsonResponse({'error': f'Failed to add VIN entry: {str(e)}'}, status=500)
        finally:
            session.close()
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def search_vin(request):
    if request.method == 'POST':
        engine = create_engine(db_uri)
        Session.configure(bind=engine)
        session = Session()
        try:
            request_data = VINSearchRequest(**json.loads(request.body))

            filtered_vins = session.query(VIN).filter(
                VIN.version == request_data.version,
                VIN.equipment_code == request_data.equipment_code,
                VIN.year_of_issue == request_data.year_of_issue,
                VIN.place_of_production == request_data.place_of_production
            ).order_by(VIN.serial_number).all()

            if filtered_vins:
                next_serial_number = filtered_vins[-1].serial_number + 1
            else:
                next_serial_number = 1000000

            response_data = VINSearchResponse(next_serial_number=next_serial_number)

            return JsonResponse(response_data.dict())
        except ValidationError as e:
            return JsonResponse({'error': f'Validation error: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def list_all_vins(request):
    per_page = 6
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1
        engine = create_engine(db_uri)
        Session.configure(bind=engine)
        session = Session()
        try:
            vins_query = session.query(VIN)
            vins = vins_query.offset((page - 1) * per_page).limit(per_page).all()
            total = vins_query.count()
            serialized_vins = [VINSchema.from_orm(vin).dict() for vin in vins]
            return JsonResponse({'vins': serialized_vins, 'total': total, 'page': page, 'perPage': per_page}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_total_pages(request):
    if request.method == 'GET':
        engine = create_engine(db_uri)
        Session.configure(bind=engine)
        session = Session()
        try:
            vins_query = session.query(VIN)
            total = vins_query.count()
            total_pages = int(total/6) + 1
            print(total_pages)
            return JsonResponse({'total_pages': total_pages})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

