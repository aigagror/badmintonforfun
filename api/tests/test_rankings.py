from .custom_test_case import *

class RankingTest(CustomTestCase):

    @run(path_name='ranking', email=MEMBER, method=GET, args={})
    def test_get_ranking(self):
        response = self.response
        self.assertGoodResponse(response)

        json = response.json()

        self.assertTrue('rankings' in json)

        rankings = json['rankings']

        self.assertTrue(isinstance(rankings, (list, )))

        topPlayer = rankings[0]

        self.assertTrue('member' in topPlayer)

        self.assertTrue('number_of_total_games' in topPlayer)

        self.assertTrue('number_of_won_games' in topPlayer)