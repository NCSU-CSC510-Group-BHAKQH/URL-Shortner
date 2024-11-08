from unittest import TestCase
from shortner.models import Link
import uuid


class TestModel(TestCase):

    def test_create_new_entry_1(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.ncsu.edu",
            special_code=unique_special_code,
            stub="aaaaaaaaaa",
        )

        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_2(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.google.com",
            special_code=unique_special_code,
            stub="bbbbbbbbbb",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_3(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.github.com",
            special_code=unique_special_code,
            stub="cccccccccc",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_4(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.stackoverflow.com",
            special_code=unique_special_code,
            stub="dddddddddd",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_5(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.microsoft.com",
            special_code=unique_special_code,
            stub="eeeeeeeeee",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_6(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.apple.com",
            special_code=unique_special_code,
            stub="ffffffffff",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_7(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.amazon.com",
            special_code=unique_special_code,
            stub="gggggggggg",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_8(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.reddit.com",
            special_code=unique_special_code,
            stub="hhhhhhhhhh",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_9(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.wikipedia.org",
            special_code=unique_special_code,
            stub="iiiiiiiiii",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_10(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.linkedin.com",
            special_code=unique_special_code,
            stub="jjjjjjjjjj",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_11(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.twitter.com",
            special_code=unique_special_code,
            stub="kkkkkkkkkk",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_12(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.facebook.com",
            special_code=unique_special_code,
            stub="llllllllll",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_13(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.instagram.com",
            special_code=unique_special_code,
            stub="mmmmmmmmmm",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_14(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.tiktok.com",
            special_code=unique_special_code,
            stub="nnnnnnnnnn",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_15(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.netflix.com",
            special_code=unique_special_code,
            stub="oooooooooo",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_16(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.spotify.com",
            special_code=unique_special_code,
            stub="pppppppppp",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_17(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.pinterest.com",
            special_code=unique_special_code,
            stub="qqqqqqqqqq",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_18(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.quora.com",
            special_code=unique_special_code,
            stub="rrrrrrrrrr",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_19(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.tumblr.com",
            special_code=unique_special_code,
            stub="ssssssssss",
        )
        self.assertIsInstance(link.to_json(), str)

    def test_create_new_entry_20(self):
        unique_special_code = str(uuid.uuid4())
        link = Link.objects.create(
            long_url="www.flickr.com",
            special_code=unique_special_code,
            stub="tttttttttt",
        )
        self.assertIsInstance(link.to_json(), str)

    def setUp(self):
        self.unique_special_code = str(uuid.uuid4())
        self.link = Link.objects.create(
            long_url="https://www.example.com",
            special_code=self.unique_special_code,
            stub="abcd1234ef",
            username="test_user",
        )

    def test_create_new_entry(self):
        self.assertIsInstance(self.link, Link)

    def test_to_json_returns_string(self):
        self.assertIsInstance(self.link.to_json(), str)

    def test_long_url_max_length(self):
        max_length_url = "https://" + "a" * (2083 - 8)
        link = Link.objects.create(
            long_url=max_length_url, special_code=str(uuid.uuid4()), stub="abcd1234ef"
        )
        self.assertEqual(link.long_url, max_length_url)

    def test_stub_unique(self):
        another_link = Link.objects.create(
            long_url="https://www.different.com",
            special_code=str(uuid.uuid4()),
            stub="unique_stub",
        )
        self.assertNotEqual(self.link.stub, another_link.stub)

    def test_username_default_value(self):
        link_without_username = Link.objects.create(
            long_url="https://www.another.com",
            special_code=str(uuid.uuid4()),
            stub="stub1234",
        )
        self.assertEqual(link_without_username.username, "xxx")

    def test_ctr_initial_value(self):
        self.assertEqual(self.link.ctr, 0)

    def test_save_assigns_stub(self):
        link_with_generated_stub = Link(long_url="https://example.com")
        link_with_generated_stub.save()
        self.assertIsInstance(link_with_generated_stub.stub, str)

    def test_save_custom_stub(self):
        custom_stub = "customstub"
        self.link.save_custom(custom_stub)
        self.assertEqual(self.link.stub, custom_stub)

    def test_to_json_contains_long_url(self):
        json_data = self.link.to_json()
        self.assertIn("long_url", json_data)

    def test_to_json_contains_special_code(self):
        json_data = self.link.to_json()
        self.assertIn("special_code", json_data)

    def test_to_json_contains_stub(self):
        json_data = self.link.to_json()
        self.assertIn("stub", json_data)
