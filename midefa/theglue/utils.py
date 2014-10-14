# -*- coding: UTF-8 -*-
# utils.py
#
# Copyright (C) 2014 HES-SO//HEG Arc
#
# Author(s): Cédric Gaspoz <cedric.gaspoz@he-arc.ch>
#
# This file is part of Midefa.
#
# Midefa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Midefa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Midefa. If not, see <http://www.gnu.org/licenses/>.

# Stdlib imports

# Core Django imports

# Third-party app imports
from trolly.client import Client
from trolly.organisation import Organisation
from trolly.board import Board
from trolly.list import List
from trolly.card import Card
from trolly.checklist import Checklist
from trolly.member import Member
from trolly import ResourceUnavailable

# Midefa imports
from .models import TrelloBoard, TrelloList, TrelloCard


def create_client_token(project):
    return Client(project.trello_api_key, project.trello_token)


def get_boards(project):
    client = create_client_token(project)
    member = Member(client, project.trello_user)
    boards = Member.get_boards(member)
    return boards


def get_board(project):
    client = create_client_token(project)
    board = Board(client, project.board.board_id)
    return board


def get_lists(project):
    board = get_board(project)
    lists = board.get_lists()
    return lists


def get_cards(project, list_):
    client = create_client_token(project)
    trello_list = List(client, list_.list_id)
    cards = trello_list.get_cards()
    return cards


def fetch_boards(project):
    boards = get_boards(project)
    boards_list = []
    for board in boards:
        obj, created = TrelloBoard.objects.update_or_create(board_id=board.id, project_origin=project, defaults={'name': board.name})
        board_information = board.get_board_information()
        obj.short_url = board_information['shortUrl']
        obj.closed = board_information['closed']
        obj.save()
        boards_list.append({'board': obj, 'created': created})
    return boards_list


def fetch_lists(project):
    lists = get_lists(project)
    for list_ in lists:
        obj, created = TrelloList.objects.update_or_create(list_id=list_.id, defaults={'name': list_.name, 'trello_board': project.board})
        list_information = list_.get_list_information()
        obj.closed = list_information['closed']
        obj.pos = list_information['pos']
        obj.save()
    return True


def fetch_all_cards(project):
    for list_ in project.board.lists.all():
        if list_.watch:
            cards = get_cards(project, list_)
            for card in cards:
                obj, created = TrelloCard.objects.update_or_create(card_id=card.id, defaults={'name': card.name, 'trello_list': list_})
                card_information = card.get_card_information()
                obj.description = card_information['desc']
                obj.id_short = card_information['idShort']
                obj.short_url = card_information['shortUrl']
                obj.last_activity = card_information['dateLastActivity']
                labels = []
                for label in card_information['labels']:
                    labels.append(label['color'])
                if 'green' in labels:
                    obj.label_green = True
                else:
                    obj.label_green = False
                if 'yellow' in labels:
                    obj.label_yellow = True
                else:
                    obj.label_yellow = False
                if 'orange' in labels:
                    obj.label_orange = True
                else:
                    obj.label_orange = False
                if 'red' in labels:
                    obj.label_red = True
                else:
                    obj.label_red = False
                if 'purple' in labels:
                    obj.label_purple = True
                else:
                    obj.label_purple = False
                if 'blue' in labels:
                    obj.label_blue = True
                else:
                    obj.label_blue = False
                obj.save()
    return True


def fetch_labels(project):
    board = get_board(project)
    labels = board.get_board_information()['labelNames']
    project.label_blue = labels['blue']
    project.label_green = labels['green']
    project.label_orange = labels['orange']
    project.label_purple = labels['purple']
    project.label_red = labels['red']
    project.label_yellow = labels['yellow']
    project.save()
    return True