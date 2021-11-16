import unittest
import requests

from admin import create_db

BASE_URL = 'http://localhost'


class TestRefactea(unittest.TestCase):

    def test_get_index_view(self):
        """
        お茶のリストがIndexに表示されているか
        :return:
        """
        resp = requests.get(BASE_URL + '/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('tea_0' in resp.text)
        self.assertTrue('tea_1' in resp.text)
        self.assertTrue('tea_2' in resp.text)

    def test_get_tea_search_view(self):
        """
        検索した際にそのお茶のみが出ているか
        :return:
        """
        resp = requests.get(BASE_URL + '/?q=tea_0')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('tea_0' in resp.text)
        self.assertTrue('tea_1' not in resp.text)

    def test_get_signup_view(self):
        """
        SignUp画面が表示されるか
        :return:
        """
        resp = requests.get(BASE_URL + '/signup')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.text)

    def test_get_login_view(self):
        """
        login画面が表示されるか
        :return:
        """
        resp = requests.get(BASE_URL + '/login')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('username' in resp.text)

    def test_get_tea_view(self):
        """
        お茶の詳細画面が正しく開けるか
        :return:
        """
        resp = requests.get(BASE_URL + '/tea/1')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('description of 0' in resp.text)

    def test_get_settle_view(self):
        """
        settleが正常なレスポンスを戻すか
        :return:
        """
        resp = requests.get(BASE_URL + '/settle')
        self.assertEqual(resp.status_code, 200)

    def test_signup_and_login_scenario(self):
        """
        SingUpからlogin/logoutまでできるか
        :return:
        """
        s = requests.Session()

        resp = s.post(BASE_URL + '/signup', data={'username': 'denzow', 'password': 'denzow_pass'})
        self.assertEqual(resp.status_code, 200)

        resp = s.get(BASE_URL + '/logout')
        self.assertEqual(resp.status_code, 200)

        resp = s.post(BASE_URL + '/login', data={'username': 'denzow', 'password': 'denzow_pass'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('tea_0' in resp.text)

        resp = s.get(BASE_URL + '/logout')
        self.assertEqual(resp.status_code, 200)

        # ログイン失敗
        resp = s.post(BASE_URL + '/login', data={'username': 'invalid', 'password': 'invalid'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Invalid username or password.' in resp.text)
        s.close()

    def test_buy_tea_scenario(self):
        """
        購入が正しくできるか
        :return:
        """
        s = requests.Session()

        resp = s.post(BASE_URL + '/signup', data={'username': 'denzow2', 'password': 'denzow_pass2'})
        self.assertEqual(resp.status_code, 200)

        resp = s.post(BASE_URL + '/cart', data={'teaId': '2', 'teaAmount': '200'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Sold' in resp.text)

        resp = s.get(BASE_URL + '/cart')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('tea_1' in resp.text)
        self.assertTrue('200' in resp.text)

        resp = s.get(BASE_URL + '/checkout')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('4380 yen' in resp.text)

        resp = s.post(BASE_URL + '/buy', data={'paymentType': 'poyjp', 'paymentInfo1': '123456789'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Teas.' in resp.text)
        s.close()


if __name__ == "__main__":
    create_db.init_db()
    unittest.main()
