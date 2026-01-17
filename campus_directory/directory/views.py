from django.shortcuts import render
from django.db.models import Q
from .models import Building, Room, Personnel, SearchLog

def home(request):
    buildings = Building.objects.prefetch_related(
        'floors__rooms__personnel'
    )
    return render(request, 'directory/home.html', {
        'buildings': buildings
    })

def search(request):
    query = request.GET.get('q', '').strip()
    building_id = request.GET.get('building')
    floor_number = request.GET.get('floor')
    room_type = request.GET.get('type')

    rooms = Room.objects.select_related(
        'floor__building'
    ).prefetch_related('personnel')

    # SEARCH ONLY ROOMS
    if query:
        rooms = rooms.filter(
            Q(room_number__icontains=query) |
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # FILTERS
    if building_id:
        rooms = rooms.filter(floor__building_id=building_id)

    if floor_number:
        rooms = rooms.filter(floor__floor_number=floor_number)

    if room_type:
        rooms = rooms.filter(type=room_type)

    # SAVE SEARCH LOG
    if query or building_id or floor_number or room_type:
        SearchLog.objects.create(
            entity_type="Search",
            entity_id=0
        )

    # If nothing searched, show nothing
    if not (query or building_id or floor_number or room_type):
        rooms = Room.objects.none()

    return render(request, 'directory/search.html', {
        'query': query,
        'rooms': rooms
    })


def search_logs(request):
    logs = SearchLog.objects.order_by('-search_time')[:200]
    return render(request, 'directory/search_logs.html', {
        'logs': logs
    })


def three_d(request):
    buildings = Building.objects.prefetch_related(
        'floors__rooms__personnel'
    )

    data = []
    for b in buildings:
        floors = []
        for f in b.floors.all():
            rooms = []
            for r in f.rooms.all():
                rooms.append({
                    "id": r.id,
                    "number": r.room_number,
                    "name": r.name,
                    "description": r.description,
                    "photo": r.photo.url if r.photo else "",
                    "personnel": [
                        {
                            "name": p.name,
                            "email": p.email,
                            "contact": p.contact_number,
                            "photo": p.photo.url if p.photo else ""
                        }
                        for p in r.personnel.all()
                    ]
                })
            floors.append({
                "number": f.floor_number,
                "rooms": rooms
            })

        data.append({
            "name": b.name,
            "floors": floors
        })

    return render(request, 'directory/three_d.html', {
        'buildings': data
    })
