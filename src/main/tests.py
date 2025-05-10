from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tournament, basketballTeam, TeamFightBasketball

User = get_user_model()

class TournamentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tournament = Tournament.objects.create(
            name="Чемпионат Москвы",
            description="Ежегодный турнир",
            address="ул. Спортивная, 15",
            type="Профессиональный"
        )

    def test_name_max_length(self):
        self.assertEqual(self.tournament._meta.get_field('name').max_length, 100)

    def test_object_creation(self):
        self.assertEqual(self.tournament.name, "Чемпионат Москвы")
        self.assertEqual(self.tournament.description, "Ежегодный турнир")
        self.assertEqual(self.tournament.address, "ул. Спортивная, 15")
        self.assertEqual(self.tournament.type, "Профессиональный")

    def test_verbose_names(self):
        self.assertEqual(Tournament._meta.verbose_name, "Турнир")
        self.assertEqual(Tournament._meta.verbose_name_plural, "Турниры")

    def test_string_representation(self):
        self.assertEqual(
            str(self.tournament), 
            "Турнир Чемпионат Москвы по адресу ул. Спортивная, 15"
        )

class BasketballTeamModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="team_coach",
            password="coachpass123"
        )
        cls.tournament = Tournament.objects.create(name="Тестовый турнир")
        cls.team = basketballTeam.objects.create(
            name="Динамо",
            coach=cls.user,
            num_players=7,
            category="Любительская",
            tournament=cls.tournament
        )

    def test_field_properties(self):
        self.assertEqual(self.team._meta.get_field('name').max_length, 50)
        self.assertEqual(self.team._meta.get_field('num_players').validators[0].limit_value, 1)

    def test_default_values(self):
        new_team = basketballTeam.objects.create(
            coach=self.user,
            tournament=self.tournament
        )
        self.assertEqual(new_team.points, 0)
        self.assertEqual(new_team.is_playing_now, False)

    def test_foreign_key_relations(self):
        self.assertEqual(self.team.coach.username, "team_coach")
        self.assertEqual(self.team.tournament.name, "Тестовый турнир")

    def test_ordering(self):
        basketballTeam.objects.create(
            name="ЦСКА",
            coach=self.user,
            points=15,
            tournament=self.tournament
        )
        teams = basketballTeam.objects.all()
        self.assertEqual(teams[0].points, 0)
        self.assertEqual(teams[1].points, 15)

    def test_string_representation(self):
        self.assertEqual(
            str(self.team),
            "Баскетбольная команда Динамо на турнир Тестовый турнир"
        )

class TeamFightBasketballModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="referee", password="refpass123")
        cls.tournament = Tournament.objects.create(name="Финал сезона")
        
        cls.team1 = basketballTeam.objects.create(
            name="Локомотив",
            coach=cls.user,
            tournament=cls.tournament
        )
        
        cls.team2 = basketballTeam.objects.create(
            name="Спартак",
            coach=cls.user,
            tournament=cls.tournament
        )
        
        cls.match = TeamFightBasketball.objects.create(
            team_one=cls.team1,
            team_two=cls.team2,
            team1_points=89,
            team2_points=91,
            time=48
        )

    def test_match_relationships(self):
        self.assertEqual(self.match.team_one.name, "Локомотив")
        self.assertEqual(self.match.team_two.name, "Спартак")

    def test_score_logic(self):
        self.assertEqual(self.match.team1_points, 89)
        self.assertEqual(self.match.team2_points, 91)
        self.assertLess(self.match.team1_points, self.match.team2_points)

    def test_default_time(self):
        new_match = TeamFightBasketball.objects.create(
            team_one=self.team1,
            team_two=self.team2
        )
        self.assertEqual(new_match.time, 40)

    def test_related_queries(self):
        matches_as_team1 = self.team1.jewel_item_code.all()
        matches_as_team2 = self.team2.jewel_item_name.all()
        
        self.assertEqual(matches_as_team1.count(), 1)
        self.assertEqual(matches_as_team2.count(), 1)
        self.assertEqual(matches_as_team1[0].team1_points, 89)
        self.assertEqual(matches_as_team2[0].team2_points, 91)

    def test_string_representation(self):
        expected_str = (
            "Баскетбольный матч между "
            "Баскетбольная команда Локомотив на турнир Финал сезона и "
            "Баскетбольная команда Спартак на турнир Финал сезона"
        )
        self.assertEqual(str(self.match), expected_str)
