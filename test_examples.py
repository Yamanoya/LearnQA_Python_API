class TestExample:
    def test_exam_ten_short_phrase(self):
        phrase = input()
        assert len(phrase) < 15
