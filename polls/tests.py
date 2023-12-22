import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

""" 
Assert list:
    assertIs: check the return value of a function against a value
    assertEqual: check both values if they are equal
    assertQuerySetEqual: check a queryset against a list of values
    assertContains: check if an object contains some parameter value
"""


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the given number of days offset to now (negative for questions published in the past, positive for questions that have yet to be published)
    """

    # make the offset
    time = timezone.now() + datetime.timedelta(days=days)

    # create question with previous parameters
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future
        """

        time = timezone.now() + datetime.timedelta(days=30)
        # create a Question object using only the pub_date field
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() return False for questions whose pub_date is older than 1 day
        """
        # just on second before of the previous day
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_questions(self):
        """
        was_published_recently() returns True for question whose pub_date is within the last day
        """
        # just the last time during the day
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

# it assumes an mepty database
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        if no questions exist, and appropiate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index_page
        """
        question = create_question(question_text="Past_question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_future_questions(self):
        """
        Questions with a pub_date in the future aren't displayed on the index page
        """

        create_question(question_text="Future_question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exists, only past question are displayed
        """
        question = create_question(question_text="Past_question", days=-30)
        create_question(question_text="Future_question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_two_past_questions(self):
        """
        the questions index page may displayed multiple question in the past
        """
        question1 = create_question(question_text="Past_question 1", days=-30)
        question2 = create_question(question_text="Past_question 2", days=-10)
        response = self.client.get(reverse("polls:index"))
        # remember is ordered by pub_date question2 has less offset days
        self.assertQuerySetEqual(response.context["latest_question_list"], [question2, question1])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        the detail view of a question with a pub_date in the future returns a 404 not found
        """
        future_question = create_question(question_text="Future_question", days=5)
        # give the quesiton id on args to detail view
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        the detail view of a question with a pub_date in the past displays the question's text in the form
        """
        past_question = create_question(question_text="Past_question", days=-5)
        # give the quesiton id on args to detail view
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


