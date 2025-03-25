import pytest

import app.bin2text as btt


class Test_depth_validation:
    """Тест ожидаемых исключений depth_validation"""

    error_msg = "Error: Depth must be a multiple of 8!"

    @pytest.mark.parametrize("depth", ["-1", "0", "1", "abc"])
    def test_depth_validation_raises(self, depth):
        with pytest.raises(ValueError) as excinfo:
            btt.depth_validation(depth)
        assert str(excinfo.value) == self.error_msg

    def test_depth_validation_negative(self):
        print("Отрицательные")
        with pytest.raises(ValueError) as excinfo:
            btt.depth_validation("-1")  # Отрицательные
        assert str(excinfo.value) == self.error_msg

    def test_depth_validation_zero(self):
        print("Ноль")
        with pytest.raises(ValueError) as excinfo:
            btt.depth_validation("0")  # Ноль
        assert str(excinfo.value) == self.error_msg

    def test_depth_validation_positive(self):
        print("Положительные")
        with pytest.raises(ValueError) as excinfo:
            btt.depth_validation("1")  # Положительные
        assert str(excinfo.value) == self.error_msg

    def test_depth_validation_text(self):
        print("Текст")
        with pytest.raises(ValueError) as excinfo:
            btt.depth_validation("abc")  # Текст
        assert str(excinfo.value) == self.error_msg

    def test_depth_validation_correct(self):
        print("Корректные")
        assert btt.depth_validation("8") == 8  # Корректные
        assert btt.depth_validation("16") == 16
        assert btt.depth_validation("32") == 32
        assert btt.depth_validation("64") == 64
