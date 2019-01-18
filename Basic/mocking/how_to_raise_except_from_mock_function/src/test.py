from unittest import main, TestCase
from unittest.mock import patch, Mock

from code import perform
# import code

class TestMock(TestCase):
    # @patch('code._perform')
    # def test_perform(self, mock_perform):
    @patch('code._perform', Mock(side_effect=Exception('This is side_effect test.')))
    def test_perform(self):
        # mock_perform.side_effect = Exception('This is side_effect test.')
        with self.assertRaises(Exception) as ex:
            perform()

if __name__ == '__main__':
    main()