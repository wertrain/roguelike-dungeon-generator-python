# -*- coding: utf-8 -*-

import linkedlist
import random

class Rect:

    def __init__(self):
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

class Section:

    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.rect = None
        self.split_vertical = False;
        self.split_horizontal = False;

    def set_rect(self, left, top, right, bottom):
        self.rect = Rect(left, top, right, bottom)

class SectionList(linkedlist.LinkedList):

    def __init__(self):
        linkedlist.LinkedList.__init__(self)

    def to_map(self, map):
        p = self.root
        while p is not None:
            rect = p.data.rect
            for i in range(rect.top, rect.bottom):
                for j in range(rect.left, rect.right):
                    map[i][j] = 1
            p = p.next
        return map

class SectionAndPassage:

    PASS_VERTICAL = 0;
    PASS_HORIZONTAL = 1;

    def __init__(self, vf, sec0, sec1):
        self.v_or_f = vf
        self.section_0 = sec0
        self.section_1 = sec1

class SectionAndPassageList(linkedlist.LinkedList):

    def __init__(self):
        linkedlist.LinkedList.__init__(self)

    def __line(self, map, x0, y0, x1, y1):
        min_x = min(x0, x1)
        max_x = max(x0, x1)
        min_y = min(y0, y1)
        max_y = max(y0, y1)
        
        if (x0 <= x1) and (y0 >= y1):
            for i in range(min_x, max_x):
                map[max_y][i] = 1;
            for j in range(min_y, max_y):
                map[j][max_x] = 1;
            return

        if (x0 > x1) and (y0 > y1):
            for i in range(min_x, max_x):
                map[min_y][i] = 1;
            for j in range(min_y, max_y):
                map[j][max_x] = 1;
            return

        if (x0 > x1) and (y0 <= y1):
            for i in range(min_x, max_x):
                map[min_y][i] = 1;
            for j in range(min_y, max_y):
                map[j][min_x] = 1;
            return

        if (x0 <= x1) and (y0 < y1):
            for i in range(min_x, max_x):
                map[max_y][i] = 1;
            for j in range(min_y, max_y):
                map[j][min_x] = 1;
            return

    def to_map(self, map):
        p = self.root
        while p is not None:
            sp = p.data
            if sp.v_or_f == SectionAndPassage.PASS_VERTICAL:
                x0 = random.randrange(sp.section_0.rect.left + 1, sp.section_0.rect.right)
                y0 = sp.section_0.bottom
                x1 = random.randrange(sp.section_1.rect.left + 1, sp.section_1.rect.right)
                y1 = sp.section_1.top
                self.__line(map, x0, y0, x1, y1)
                self.__line(map, x0, sp.section_0.rect.bottom, x0, y0)
                self.__line(map, x1, sp.section_1.rect.top, x1, y1)
            elif sp.v_or_f == SectionAndPassage.PASS_HORIZONTAL:
                x0 = sp.section_0.right
                y0 = random.randrange(sp.section_0.rect.top + 1, sp.section_0.rect.bottom)
                x1 = sp.section_1.left
                y1 = random.randrange(sp.section_1.rect.top + 1, sp.section_1.rect.bottom)
                self.__line(map, x0, y0, x1, y1)
                self.__line(map, sp.section_0.rect.right, y0, x0, y0)
                self.__line(map, sp.section_1.rect.left, y1, x1, y1)
            p = p.next

class Generator:

    DEFAULT_MIN_ROOM_SIZE = 4
    DEFAULT_MARGIN_BETWEEN_ROOM = 2
    DEFAULT_ONE_ROOM_PROBABILITY = 5
    DEFAULT_PLURAL_PASSAGES_PROBABILITY = 0

    def __init__(self, width, height, 
                  min_room_size=DEFAULT_MIN_ROOM_SIZE, margin_between_room=DEFAULT_MARGIN_BETWEEN_ROOM, 
                  one_room_probability=DEFAULT_ONE_ROOM_PROBABILITY, plural_passages_probability=DEFAULT_PLURAL_PASSAGES_PROBABILITY):
        self.min_room_size = min_room_size
        self.margin_between_room = margin_between_room
        self.min_rect_size = self.min_room_size + (self.margin_between_room * 2)
        
        self.dungeon_width = width
        self.dungeon_height = height
        self.section_list = SectionList()
        self.section_and_passage_list = SectionAndPassageList()
        
        self.map = [[0 for i in range(self.dungeon_width)] for j in range(self.dungeon_height)]
        
        self.one_room_probability = one_room_probability
        self.plural_passages_probability = plural_passages_probability

    def __make_divided_rect(self, section):
        if random.randrange(100) < self.one_room_probability:
            section.split_vertical = section.split_horizontal = True
        
        # check min size
        if section.bottom - section.top <= self.min_rect_size * 2:
            section.split_vertical = True
        if section.right - section.left <= self.min_rect_size * 2:
            section.split_horizontal = True

        # OK?
        if section.split_vertical and section.split_horizontal:
            return
        
        # Rectangle created after the division
        new_section = Section(section.left, section.top, section.right, section.bottom)
        self.section_list.append(new_section)
        
        if not section.split_vertical:
            coord_y = random.randrange(section.top + self.min_rect_size, section.bottom - self.min_rect_size)
            section.bottom = coord_y
            new_section.top = coord_y
            section.split_vertical = True
            new_section.split_vertical = True
            self.section_and_passage_list.append(SectionAndPassage(SectionAndPassage.PASS_VERTICAL, section, new_section))
            self.__make_divided_rect(section)
            self.__make_divided_rect(new_section)
            return
        
        if not section.split_horizontal:
            coord_x = random.randrange(section.left + self.min_rect_size, section.right - self.min_rect_size)
            section.right = coord_x
            new_section.left = coord_x
            section.split_horizontal = True
            new_section.split_horizontal = True
            self.section_and_passage_list.append(SectionAndPassage(SectionAndPassage.PASS_HORIZONTAL, section, new_section))
            self.__make_divided_rect(section)
            self.__make_divided_rect(new_section)
            return

    def __make_rect_in_section(self):
        p = self.section_list.root
        while p is not None:
            section = p.data
            w = random.randrange(self.min_room_size, section.right - section.left - (self.margin_between_room * 2) + 1)
            h = random.randrange(self.min_room_size, section.bottom - section.top - (self.margin_between_room * 2) + 1)
            x = random.randrange(section.left + self.margin_between_room, section.right - self.margin_between_room - w + 1)
            y = random.randrange(section.top + self.margin_between_room, section.bottom - self.margin_between_room - h + 1)
            section.set_rect(x, y, x + w, y + h)
            p = p.next

    def __make_more_passages(self):
        if self.plural_passages_probability == 0:
            return
        section_map = [[0 for i in range(self.dungeon_width)] for j in range(self.dungeon_height)]

        p = self.section_list.root
        while p is not None:
            section = p.data
            for i in range(section.top, section.bottom):
                for j in range(section.left, section.right):
                    section_map[i][j] = section
            p = p.next

        for i in range(0, self.dungeon_height - 2):
            for j in range(0, self.dungeon_width - 2):
                if section_map[i][j] != section_map[i][j + 1]:
                    if random.randrange(100) < self.plural_passages_probability:
                        self.section_and_passage_list.append(
                            SectionAndPassage(SectionAndPassage.PASS_HORIZONTAL, section_map[i][j], section_map[i][j + 1])
                        )
                if section_map[i][j] != section_map[i + 1][j]:
                    if random.randrange(100) < self.plural_passages_probability:
                        self.section_and_passage_list.append(
                            SectionAndPassage(SectionAndPassage.PASS_VERTICAL, section_map[i][j], section_map[i + 1][j])
                        )

    def __clear(self):
        for i in range(0, self.dungeon_height):
            for j in range(0, self.dungeon_width):
                self.map[i][j] = 0

    def generate(self):
        self.__clear()
        
        section = Section(0, 0, self.dungeon_width - 1, self.dungeon_height - 1)
        self.section_list.append(section)
        
        self.__make_divided_rect(section)
        self.__make_rect_in_section()
        self.__make_more_passages()
        
        self.section_list.to_map(self.map)
        self.section_and_passage_list.to_map(self.map)