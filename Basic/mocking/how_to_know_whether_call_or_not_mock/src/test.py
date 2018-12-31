from unittest import main, TestCase
from unittest.mock import patch

from code import perform


class TestMock(TestCase):
    @patch('code.get_value')
    def test_perform(self, mock_get_value):
        mock_get_value.return_value = 1
        self.assertEqual(perform(), 10)
        # mock_get_value.assert_called_with()
        mock_get_value.assert_called()
        

if __name__ == '__main__':
    main()