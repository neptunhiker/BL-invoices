# Module that holds the class of training participants

class Human(object):

    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name
        self._full_name = f"{first_name} {last_name}"

    @property
    def full_name(self):
        return self._full_name

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value
        self._full_name = f"{self._first_name} {self._last_name}"

    @last_name.setter
    def last_name(self, value):
        self._last_name = value
        self._full_name = f"{self._first_name} {self._last_name}"

    @full_name.setter
    def full_name(self, value):
        raise AttributeError

    def __str__(self):
        return f"{self._full_name}"


class Participant(Human):

    def __init__(self, first_name, last_name):
        super().__init__(first_name=first_name, last_name=last_name)
        self.avgs_coupons = {}

    def assign_avgs(self, avgs):
        """
        Assign an avgs coupon to a participant
        """
        if avgs.nr in self.avgs_coupons:
            return
        else:
            self.avgs_coupons[avgs.nr] = avgs

def main():
    human = Human(first_name="Joe", last_name="Doe")
    print(human)
    print(human.first_name)
    human.last_name ="Richardson"
    print(human)

    ahmed = Participant(first_name="Ahmed", last_name="Muhadi")
    print(ahmed)

    ahmed.full_name = "Peter Bauer"
    print(ahmed.full_name)

if __name__ == '__main__':
    main()
