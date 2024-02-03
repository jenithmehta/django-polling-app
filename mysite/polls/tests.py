from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from polls.models import Question
# Create your tests here.

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions
        whose pub_date is in future
        """
        future_time = timezone.now() + timedelta(seconds=1)
        future_question = Question(pub_date = future_time)
        self.assertIs(future_question.was_published_recently(),False)
        recent_time = timezone.now() - timedelta(hours=23,minutes=59,seconds=59)
        recent_question = Question(pub_date = recent_time)
        self.assertIs(recent_question.was_published_recently(),True)
        past_time = timezone.now() - timedelta(days=1,seconds=1)
        past_question = Question(pub_date = past_time)
        self.assertIs(past_question.was_published_recently(),False)

def create_question(question_text,days):
    question = Question.objects.create(
        pub_date = (timezone.now()
                    + timedelta(days = days)),
        question_text = question_text)
    return question

class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        """Test if no question is available"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"],[])
        self.assertContains(response,"No polls are available")

    def test_past_question(self):
        """ Question with past date are shown to user"""
        past_question = create_question("past_question",-3)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"],[past_question])
        
    def test_future_question(self):
        """No question should be visible when pub_data is in future"""
        create_question("future_question",+3)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"],[])
        self.assertContains(response,"No polls are available")
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)