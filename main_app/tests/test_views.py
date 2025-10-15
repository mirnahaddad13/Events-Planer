from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from django.utils import timezone

from main_app.models import Event
from main_app.views import _is_privileged

#our urls
URL_EVENT_CREATE = "event-create"
URL_EVENT_DETAILS = "event-details"
URL_EVENT_UPDATE = "event-update"
URL_EVENT_DELETE = "event-delete"

User = get_user_model()

# we have to add this to match the datetime-local widgets: 'YYYY-MM-DDTHH:MM'
DATETIME_FMT = "%Y-%m-%dT%H:%M"

#the required fields for creating events
REQUIRED_DEFAULTS = {
    "description": "Test description",
    "location": "Test Hall A",
    "attendees_count": 25,
    "theme_colors": "gold,white",
}


class EventViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.regular = User.objects.create_user(
            username="user", password="pass", is_staff=False, is_superuser=False
        )
        cls.staff = User.objects.create_user(
            username="staff", password="pass", is_staff=True, is_superuser=False
        )
        cls.admin = User.objects.create_superuser(username="admin", password="pass")

    def make_event(self, owner, start_delta_hours=30, end_delta_hours=32, **extra):
        """
        Create an Event instance with all required fields present.
        """
        now = timezone.now()
        payload = {
            "user": owner,
            "title": extra.pop("title", "Test Event"),
            "start_date": now + timedelta(hours=start_delta_hours),
            "end_date": now + timedelta(hours=end_delta_hours),
            **REQUIRED_DEFAULTS,
            **extra,
        }
        return Event.objects.create(**payload)

    def form_payload(self, start_dt, end_dt, **extra):
        """
        Build a POST payload that matches the EventForm (including required fields),
        and using datetime-local formatting.
        """
        base = {
            "title": extra.pop("title", "Test Event"),
            "start_date": start_dt.strftime(DATETIME_FMT),
            "end_date": end_dt.strftime(DATETIME_FMT),
            **REQUIRED_DEFAULTS,
        }
        base.update(extra)
        return base

    def test_is_privileged(self):
        self.assertFalse(_is_privileged(self.regular))
        self.assertTrue(_is_privileged(self.staff))
        self.assertTrue(_is_privileged(self.admin))

    # testing creat event
    def test_create_happy_path_sets_owner_and_redirects(self):
        try:
            url = reverse(URL_EVENT_CREATE)
        except NoReverseMatch:
            self.skipTest(f"URL name '{URL_EVENT_CREATE}' not found. Adjust constants at top.")
            return

        self.client.login(username="user", password="pass")
        now = timezone.now()
        start = now + timedelta(hours=6)   
        end = start + timedelta(hours=2)

        resp = self.client.post(url, self.form_payload(start, end), follow=False)
        self.assertIn(resp.status_code, (302, 303))

        ev = Event.objects.latest("id")
        self.assertEqual(ev.user, self.regular)
        self.assertEqual(ev.title, "Test Event")

    def test_create_rejects_less_than_5_hours(self):
        try:
            url = reverse(URL_EVENT_CREATE)
        except NoReverseMatch:
            self.skipTest(f"URL name '{URL_EVENT_CREATE}' not found.")
            return

        self.client.login(username="user", password="pass")
        now = timezone.now()
        start = now + timedelta(hours=4, minutes=30) 
        end = start + timedelta(hours=2)

        resp = self.client.post(url, self.form_payload(start, end))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("You must reserve at least 5 hours in advance.", resp.content.decode())

    def test_create_rejects_past_and_end_not_after_start(self):
        try:
            url = reverse(URL_EVENT_CREATE)
        except NoReverseMatch:
            self.skipTest(f"URL name '{URL_EVENT_CREATE}' not found.")
            return

        self.client.login(username="user", password="pass")
        now = timezone.now()

        #past start
        resp1 = self.client.post(url, self.form_payload(now - timedelta(hours=1), now + timedelta(hours=1)))
        self.assertEqual(resp1.status_code, 200)
        self.assertIn("Start date/time cannot be in the past.", resp1.content.decode())

        #past end
        resp2 = self.client.post(url, self.form_payload(now + timedelta(hours=6), now - timedelta(hours=1)))
        self.assertEqual(resp2.status_code, 200)
        self.assertIn("End date/time cannot be in the past.", resp2.content.decode())

        #end <= start
        same = now + timedelta(hours=6)
        resp3 = self.client.post(url, self.form_payload(same, same))
        self.assertEqual(resp3.status_code, 200)
        self.assertIn("End date/time must be after the start date/time.", resp3.content.decode())

    #testing update event
    def test_update_dispatch_blocks_non_privileged_within_one_day(self):
        try:
            reverse(URL_EVENT_UPDATE, kwargs={"pk": 1})
        except NoReverseMatch:
            self.skipTest(f"URL name '{URL_EVENT_UPDATE}' not found.")
            return

        ev = self.make_event(self.regular, start_delta_hours=12, end_delta_hours=14)
        self.client.login(username="user", password="pass")
        resp = self.client.get(reverse(URL_EVENT_UPDATE, kwargs={"pk": ev.pk}))
        self.assertIn(resp.status_code, (301, 302))
        self.assertIn(reverse(URL_EVENT_DETAILS, kwargs={"pk": ev.pk}), resp["Location"])

    def test_update_dispatch_allows_staff_even_within_one_day(self):
        try:
            reverse(URL_EVENT_UPDATE, kwargs={"pk": 1})
        except NoReverseMatch:
            self.skipTest(f"URL name '{URL_EVENT_UPDATE}' not found.")
            return

        ev = self.make_event(self.staff, start_delta_hours=6, end_delta_hours=8)
        self.client.login(username="staff", password="pass")
        resp = self.client.get(reverse(URL_EVENT_UPDATE, kwargs={"pk": ev.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_update_validations_and_success(self):
        try:
            reverse(URL_EVENT_UPDATE, kwargs={"pk": 1})
        except NoReverseMatch:
            self.skipTest(f"URL name '{URL_EVENT_UPDATE}' not found.")
            return

        ev = self.make_event(self.regular, start_delta_hours=48, end_delta_hours=50)
        self.client.login(username="user", password="pass")
        url = reverse(URL_EVENT_UPDATE, kwargs={"pk": ev.pk})
        now = timezone.now()

        #end <= start
        resp1 = self.client.post(url, self.form_payload(now + timedelta(days=2), now + timedelta(days=2)))
        self.assertEqual(resp1.status_code, 200)
        self.assertIn("End date/time must be after the start date/time.", resp1.content.decode())

        #past start
        resp2 = self.client.post(url, self.form_payload(now - timedelta(hours=1), now + timedelta(hours=1)))
        self.assertEqual(resp2.status_code, 200)
        self.assertIn("Start date/time cannot be in the past.", resp2.content.decode())

        #past end
        resp3 = self.client.post(url, self.form_payload(now + timedelta(hours=6), now - timedelta(hours=1)))
        self.assertEqual(resp3.status_code, 200)
        self.assertIn("End date/time cannot be in the past.", resp3.content.decode())

        #non-privileged: start < now+1day
        resp4 = self.client.post(url, self.form_payload(now + timedelta(hours=12), now + timedelta(hours=18)))
        self.assertEqual(resp4.status_code, 200)
        self.assertIn("You cannot set the start time to less than 1 day from now.", resp4.content.decode())

        #happy path
        ok = self.client.post(url, self.form_payload(now + timedelta(days=2), now + timedelta(days=2, hours=2)))
        self.assertIn(ok.status_code, (302, 303))

    #testing delete event
    def test_delete_blocks_non_privileged_within_one_day(self):
        try:
            reverse(URL_EVENT_DELETE, kwargs={"pk": 1})
        except NoReverseMatch:
            self.skipTest(f"URL name '{URL_EVENT_DELETE}' not found.")
            return

        ev = self.make_event(self.regular, start_delta_hours=8, end_delta_hours=10)
        self.client.login(username="user", password="pass")
        resp = self.client.post(reverse(URL_EVENT_DELETE, kwargs={"pk": ev.pk}))
        self.assertIn(resp.status_code, (301, 302))
        self.assertIn(reverse(URL_EVENT_DETAILS, kwargs={"pk": ev.pk}), resp["Location"])
        self.assertTrue(Event.objects.filter(pk=ev.pk).exists(), "Event should NOT be deleted")

    def test_delete_allows_staff_even_within_one_day(self):
        try:
            reverse(URL_EVENT_DELETE, kwargs={"pk": 1})
        except NoReverseMatch:
            self.skipTest(f"URL name '{URL_EVENT_DELETE}' not found.")
            return

        ev = self.make_event(self.staff, start_delta_hours=6, end_delta_hours=7)
        self.client.login(username="staff", password="pass")
        resp = self.client.post(reverse(URL_EVENT_DELETE, kwargs={"pk": ev.pk}))
        self.assertIn(resp.status_code, (301, 302))
        self.assertFalse(Event.objects.filter(pk=ev.pk).exists(), "Event should be deleted")

    def test_delete_allows_non_privileged_if_far_enough(self):
        try:
            reverse(URL_EVENT_DELETE, kwargs={"pk": 1})
        except NoReverseMatch:
            self.skipTest(f"URL name '{URL_EVENT_DELETE}' not found.")
            return

        ev = self.make_event(self.regular, start_delta_hours=48, end_delta_hours=49)
        self.client.login(username="user", password="pass")
        resp = self.client.post(reverse(URL_EVENT_DELETE, kwargs={"pk": ev.pk}))
        self.assertIn(resp.status_code, (301, 302))
        self.assertFalse(Event.objects.filter(pk=ev.pk).exists())

    #testing event details page, with permissions
    def test_event_details_permission(self):
        try:
            reverse(URL_EVENT_DETAILS, kwargs={"pk": 1})
        except NoReverseMatch:
            self.skipTest(f"URL name '{URL_EVENT_DETAILS}' not found.")
            return

        mine = self.make_event(self.regular, 30, 32)
        others = self.make_event(self.staff, 30, 32)

        #non-owner cannot view other's event (should be 404 due to queryset restriction)
        self.client.login(username="user", password="pass")
        r_forbidden = self.client.get(reverse(URL_EVENT_DETAILS, kwargs={"pk": others.pk}))
        self.assertEqual(r_forbidden.status_code, 404)

        #staff can view anyone's event
        self.client.login(username="staff", password="pass")
        r_staff = self.client.get(reverse(URL_EVENT_DETAILS, kwargs={"pk": mine.pk}))
        self.assertEqual(r_staff.status_code, 200)
