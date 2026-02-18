import unittest
import skills


class test_feature1(unittest.TestCase):
    def test_yes_returns_skills_gap(self):
        self.assertEqual(
            skills.user_a_path_for_testing(True),
            "skills_gap_to_dream_job"
        )

    def test_no_returns_exploration(self):
        self.assertEqual(
            skills.user_a_path_for_testing(False),
            "exploration_of_potential_dream_jobs"
        )

    def test_return_value_is_one_of_two_paths(self):
        self.assertIn(
            skills.user_a_path_for_testing(True),
            ("skills_gap_to_dream_job", "exploration_of_potential_dream_jobs")
        )


if __name__ == "__main__":
    unittest.main()
