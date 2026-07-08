import unittest

from handlers.admin.panel import format_user_reference, normalize_user_identifier


class UserManageHelpersTests(unittest.TestCase):
    def test_normalize_user_identifier_strips_prefix_and_spaces(self) -> None:
        self.assertEqual(normalize_user_identifier(" @demo_user "), "demo_user")
        self.assertEqual(normalize_user_identifier(" 12345 "), "12345")

    def test_format_user_reference_contains_id_username_and_nickname(self) -> None:
        user = {"user_id": 42, "username": "demo", "full_name": "Demo User"}
        text = format_user_reference(user)
        self.assertIn("42", text)
        self.assertIn("demo", text)
        self.assertIn("Demo User", text)


if __name__ == "__main__":
    unittest.main()
