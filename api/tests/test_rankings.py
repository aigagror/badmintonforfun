from .custom_test_case import *

class RankingTest(CustomTestCase):

    def _assert_fields(self, topPlayer):
        # self.assertTrue('member_info' in topPlayer)
        # member_info = topPlayer['member_info']
        self.assertTrue('first_name' in topPlayer)

        self.assertTrue('total_games' in topPlayer)
        self.assertTrue('wins' in topPlayer)
        self.assertTrue('level' in topPlayer)

    @run(path_name='get_rankings_by_level', email=MEMBER, method=GET, args={})
    def test_get_rankings_by_level(self):
        response = self.response
        self.assertGoodResponse(response)

        json = response.json()

        self.assertTrue('rankings' in json)

        rankings = json['rankings']

        self.assertTrue(isinstance(rankings, (list, )))

        topPlayer = rankings[0]

        self._assert_fields(topPlayer)

        # Joshua should be the top player, since only he has a level greater than 0 (10).
        self.assertEqual(topPlayer['first_name'], 'Joshua')




    @run(path_name='get_rankings_by_win_ratio', email=MEMBER, method=GET, args={})
    def test_get_rankings_by_win_ratio(self):
        response = self.response
        self.assertGoodResponse(response)

        json = response.json()

        self.assertTrue('rankings' in json)

        rankings = json['rankings']

        self.assertTrue(isinstance(rankings, (list,)))

        topPlayer = rankings[0]

        self._assert_fields(topPlayer)

        # Eddie should be the top player, since only he has a win ratio of 1
        self.assertEqual(topPlayer['first_name'], 'Eddie')

