import random

from Event import Event

class Sorter:

    def __init__(self, list_to_sort):
        self.list = list_to_sort

    # SORTING FUNCTIONS
    def bubble_sort(self, to_sort = None):
        to_sort = to_sort or self.copy()

        sorted_index = len(to_sort)
        while True:
            changed = False
            for curr_index, curr_item in enumerate(to_sort):
                if curr_index >= sorted_index - 1:
                    break

                next_item = to_sort[(next_index := curr_index + 1)]

                event = Event(curr_index, next_index, "comparison")
                yield event

                if curr_item > next_item:
                    to_sort = self.swap(to_sort, curr_index, next_index)
                    changed = True
                    event = Event(curr_index, next_index, "swap")
                    yield event

            if not changed:
                break

            sorted_index -= 1

        event_list = self.confirm_sort(to_sort, False)[1]
        for event in event_list:
            yield event

        yield to_sort

    def insertion_sort(self, to_sort = None):
        to_sort = to_sort or self.copy()

        for curr_index in range(1, len(to_sort)):

            curr_item = to_sort[curr_index]

            prev_index = curr_index - 1
            event = Event(curr_index, prev_index, 'comparison')
            yield event
            while curr_item < to_sort[prev_index] and prev_index >= 0:

                to_sort = self.swap(to_sort, prev_index + 1, prev_index)
                event = Event(prev_index + 1, prev_index, 'swap')
                yield event

                prev_index -= 1

        event_list = self.confirm_sort(to_sort, False)[1]
        for event in event_list:
            yield event

        yield to_sort

    def selection_sort(self, to_sort = None):
        to_sort = to_sort or self.copy()

        event_list = []
        for curr_index in range(len(to_sort)):
            min_index = curr_index
            for next_index in range(curr_index + 1, len(to_sort)):
                event = Event(min_index, next_index, "comparison")
                yield event
                if to_sort[next_index] < to_sort[min_index]:
                    min_index = next_index

            to_sort = self.swap(to_sort, min_index, curr_index)
            event = Event(min_index, curr_index, "swap")
            yield event

        event_list = self.confirm_sort(to_sort, False)[1]
        for event in event_list:
            yield event

        yield to_sort

    def quick_sort(self, to_sort = None):
        to_sort = to_sort or self.copy()
        for i in self.quick_sort_helper(to_sort, 0, len(to_sort) - 1):
            yield i


    def quick_sort_helper(self, to_sort, start, end):

        if start < end:

            to_sort, p_index, event_list = self.quick_sort_partition(to_sort, start, end)
            for event in event_list:
                yield event

            gen = self.quick_sort_helper(to_sort, start, p_index - 1)
            for event in gen:
                if isinstance(event, Event):
                    yield event

            gen = self.quick_sort_helper(to_sort, p_index + 1, end)
            for event in gen:
                if isinstance(event, Event):
                    yield event

        event_list = self.confirm_sort(to_sort, False)[1]
        for event in event_list:
            if start == 0 and end == len(to_sort) - 1:
                yield event

        yield to_sort

    def quick_sort_partition(self, to_sort, start, end):
        event_list = []
        pivot = to_sort[end]
        p_index = start

        for i in range(start, end):
            event_list.append(Event(i, end, "comparison"))
            if to_sort[i] <= pivot:
                to_sort = self.swap(to_sort, p_index, i)
                event_list.append(Event(i, p_index, "swap"))
                p_index += 1

        to_sort = self.swap(to_sort, p_index, end)
        event_list.append(Event(p_index, end, "swap"))

        return to_sort, p_index, event_list

    def bogo_sort(self, to_sort = None):
        to_sort = to_sort or self.copy()

        sorted, event_list = self.confirm_sort(to_sort)
        for event in event_list:
            if not sorted:
                event.set_state(type = "comparison", keep = False)
            yield event

        while not sorted:
            shuffle_gen = self.shuffle_list(to_sort)
            for event in shuffle_gen:
                if isinstance(event, Event):
                    yield event
                if isinstance(event, list):
                    to_sort = event

            sorted, event_list = self.confirm_sort(to_sort)
            for event in event_list:
                if not sorted:
                    event.set_state(type = "comparison", keep = False)
                yield event

        yield to_sort

    def bozo_sort(self, to_sort = None):
        to_sort = to_sort or self.copy()

        sorted, event_list = self.confirm_sort(to_sort)
        for event in event_list:
            if not sorted:
                event.set_state(type = "comparison", keep = False)
            yield event

        while not sorted:
            shuffle_gen = self.shuffle_list(to_sort)
            for event in shuffle_gen:
                if isinstance(event, Event):
                    yield event
                if isinstance(event, list):
                    to_sort = event

            sorted, event_list = self.confirm_sort(to_sort)
            for event in event_list:
                if not sorted:
                    event.set_state(type = "comparison", keep = False)
                yield event

        yield to_sort

    # HELPER FUNCTIONS
    def shuffle_list(self, to_shuffle = None, whole_list = True):
        to_shuffle = to_shuffle or self.copy()

        event_list = []

        if whole_list:
            for n in range(len(to_shuffle)):
                random_index = random.randint(n, len(to_shuffle) - 1)
                to_shuffle = self.swap(to_shuffle, n, random_index)
                event_list.append(Event(n, random_index, "swap"))
        else:
            random_index_one = random.randint(0, len(to_shuffle) - 1)
            random_index_two = random.randint(0, len(to_shuffle) - 1)
            to_shuffle = self.swap(to_shuffle, random_index_one, random_index_two)
            event_list.append(Event(random_index_one, random_index_two, "swap"))

        for event in event_list:
            yield event

        yield to_shuffle

    def copy(self, to_copy: list = None):
        """
        Returns a copy of the class' list or the passed list

        :param list to_copy: An optional parameter for a user-sent list
        :return: The copy of the list
        """
        to_copy = to_copy or self.list
        return [i for i in to_copy]

    def confirm_sort(self, to_check: list = None, check: bool = True):
        """
        Returns an event list of checking if the list is sorted, as well as a bool of wether it's sorted or not
        If we are sure the list is sorted and just want the event list, `check` would be false
        """
        event_list = []
        for n in range(len(to_check) - 1):
            event_list.append(Event(n, n + 1))
            if not check:
                continue
            if to_check[n] <= to_check[n + 1]:
                continue
            else:
                return False, event_list

        return True, event_list

    @staticmethod
    def swap(list: list, first_index: int , second_index: int) -> list:
        """
        Swaps the items at first_index and second_index for list `list`

        :param list list: The list to swap the items of
        :param int first_index: The index of the first item to swap
        :param int second_index: The index of the second item to swap
        :return: The list with the swapped values
        """
        temp = list[first_index]
        list[first_index] = list[second_index]
        list[second_index] = temp

        return list

    @staticmethod
    def generate_random_list(size: int = 10, min_item: int = -10, max_item: int = 10):
        """
        Returns a randomly generated list of size `size` with with minimum and maximum constrains on the values

        :param int min_item: An optional param for the minimum amount a value in the list can be
        :param int max_item: An optional param for the maxmimum amount a value in the list can be
        :return: The randomly generated list
        """
        return [random.randint(min_item, max_item) for _ in range(size)]

    def get_list(self):
        return self.list