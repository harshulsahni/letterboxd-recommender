from src.utils import one_of_list_starts_with


class TestOneOfListStartsWith:
    @staticmethod
    def test_list_does_not_start_with_any():
        elements = ["hello", "my", "name", "is", "bob"]
        assert not one_of_list_starts_with(elements, "bye", "your", "age")

    @staticmethod
    def test_list_does_not_start_with_some():
        elements = ["hello", "my", "name", "is", "bob"]
        assert one_of_list_starts_with(elements, "bo")

    @staticmethod
    def test_empty_list():
        elements = []
        assert not one_of_list_starts_with(elements, "one", "heehehe")

    @staticmethod
    def test_all_elements_in_list():
        elements = ["one", "only", "onyx"]
        assert one_of_list_starts_with(elements, "on")

    @staticmethod
    def test_with_no_args():
        elements = ["one", "two"]
        assert not one_of_list_starts_with(elements)
