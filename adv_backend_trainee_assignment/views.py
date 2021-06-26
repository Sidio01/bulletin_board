import datetime
import json

from django.core.exceptions import FieldError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import URLValidator
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from jsonschema import validate
from jsonschema.exceptions import ValidationError as JsonschemaValidationError

from .models import Ad
from .schemas import AD_SCHEMA


class GetAdListView(View):
    """View для получения списка объявлений."""
    
    def get(self, request):
        try:
            page = int(request.GET.get('page'))
            sort_by = request.GET.get('sorted')
            order = request.GET.get('order')

            if not sort_by:
                sort_by = 'price'
            if not order:
                order = 'asc'

            assert order in ('asc', 'desc')

            start = 10 * (page - 1)
            end = page * 10

            sorting_order = sort_by if order == 'asc' else '-' + sort_by

            ads = Ad.objects.all().order_by(sorting_order)[start:end]
            ads_dict = {}

            for ad in ads:
                ads_dict[ad.id] = model_to_dict(ad, fields=['id', 'title', 'urls_list', 'price'])
                ads_dict[ad.id]['urls_list'] = ads_dict[ad.id]['urls_list'].split(',')[0]
        except AssertionError:
            return JsonResponse({'error': 'Order must be \'asc\' or \'desc\''}, status=400)
        except FieldError:
            return JsonResponse({'error': 'Sorted must be \'price\' or \'date\''}, status=400)
        except TypeError:
            return JsonResponse({'error': 'Enter page'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Page must be integer'}, status=400)

        return JsonResponse(ads_dict, status=200)


class GetAdView(View):
    """View для получения одного объявления."""
    
    def get(self, request, ad_id):
        try:
            flag = request.GET.get('fields')
            ad = Ad.objects.get(id=ad_id)
        except Ad.DoesNotExist:
            return JsonResponse({'error': 'Ad doesn\'t exist'}, status=404)
        if flag == 'true':
            ad_dict = model_to_dict(ad, fields=['id', 'title', 'description', 'price', 'urls_list'])
        else:
            ad_dict = model_to_dict(ad, fields=['id', 'title', 'price', 'urls_list'])
            ad_dict['urls_list'] = ad_dict['urls_list'].split(',')[0]
        return JsonResponse(ad_dict, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AddAdView(View):
    """View для создания объявления."""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            validate(data, AD_SCHEMA)

            url_validator = URLValidator()
            pre_urls_list = data['urls_list'].split(',')
            if len(pre_urls_list) > 3:
                return JsonResponse({'error': 'Enter 3 or less URL'}, status=400)
            for url in pre_urls_list:
                url_validator(url)

            ad = Ad(title=data['title'],
                    description=data['description'],
                    urls_list=data['urls_list'],
                    price=data['price'],
                    date=datetime.datetime.now())
            ad.save()
            return JsonResponse({'id': ad.id}, status=201)
        except DjangoValidationError as exc:
            return JsonResponse({'error': exc.message}, status=400)
        except JsonschemaValidationError as exc:
            return JsonResponse({'error': exc.message}, status=400)
