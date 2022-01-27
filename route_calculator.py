import json
from collections import deque
from itertools import (
    permutations,
    tee,
)
from math import inf
from typing import (
    List,
    Tuple
)


class Route:
    def __init__(self):
        self.length = inf
        self.places = []

    @staticmethod
    def get_distance(place_pair: Tuple):
        distance = (
            ((place_pair[1].coords[0] - place_pair[0].coords[0]) ** 2 +
            (place_pair[1].coords[1] - place_pair[0].coords[1]) ** 2) ** 0.5
        )

        return distance


class Place:
    def __init__(self, address, coords: List, start_end_point_sign=False):
        self.address = address
        self.coords = coords
        self.start_end_point = start_end_point_sign

    def __str__(self):
        return f'Место: {self.address}, координаты: {self.coords}'


def get_places(filename='places.json',
               start_end_point_name='Почтовое отделение',
               places=None):

    '''Считывает входные данные для алгоритма.'''

    with open(filename, 'rt', encoding='utf-8') as file_with_points:
        points = json.load(file_with_points)

        places = places or []
        for address, point in points.items():
            if point['start_end_point_sign'] == start_end_point_name:
                place = Place(address, point['coords'], start_end_point_sign=True)
            else:
                place = Place(address, point['coords'])
            places.append(place)

    return places


def form_points_groups(places):

    '''Формирует две группы точек (мест)'''

    places_ = places[:]

    for idx, place in enumerate(places_):
        if place.start_end_point:
            break

    start_end_point = places_.pop(idx)

    return start_end_point, places_


def pairwise(iterable):

    '''Создаёт итератор последовательного попарного воспроизведения точек'''

    it_first, it_second = tee(iterable)
    next(it_second, None)

    return zip(it_first, it_second)


def search_shortest_route(places):
    start_end_point, others_points = form_points_groups(places)
    places_belonging_to_routes = permutations(others_points)

    shortest_route = Route()
    for places_belonging_to_route in places_belonging_to_routes:

        points = deque(places_belonging_to_route)
        points.appendleft(start_end_point)
        points.append(start_end_point)

        route_length = 0
        for points_pair in pairwise(points):
            distance = shortest_route.get_distance(points_pair)
            route_length += distance

        if route_length < shortest_route.length:
            shortest_route.length = route_length
            shortest_route.places = list(points)

    return shortest_route


def get_route_representation(route):

    representation = ''
    route_length = 0
    for first_point, second_point in pairwise(route.places):
        distance = route.get_distance([first_point, second_point])
        route_length += distance
        second_point_x = second_point.coords[0]
        second_point_y = second_point.coords[1]

        if first_point.start_end_point:
            template = '({}, {}) -> ({}, {})[{}] -> '
            representation += template.format(first_point.coords[0],
                                              first_point.coords[1],
                                              second_point_x,
                                              second_point_y,
                                              route_length)

        elif second_point.start_end_point:
            template = '({}, {})[{}] = {}'
            representation += template.format(second_point_x,
                                              second_point_y,
                                              route_length,
                                              route_length)

        else:
            template = '({}, {})[{}] -> '
            representation += template.format(second_point_x,
                                              second_point_y,
                                              route_length)

    return representation


def main():
    places = get_places()
    shortest_route = search_shortest_route(places)
    representation = get_route_representation(shortest_route)

    return representation


if __name__ == '__main__':
    print(main())
