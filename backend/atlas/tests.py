from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PillowImage
from rest_framework.test import APITestCase

from wintersehn.accounts.models import UserProfile

from .models import Flashcard, Institution, LearningSet, Subject


def create_user(username, admin=True):
    user = get_user_model().objects.create_user(username)
    UserProfile.objects.create(user=user, verified=True)
    if admin:
        user.user_permissions.add(
            Permission.objects.get(
                codename="view_admin", content_type__app_label="content"
            )
        )
    return user


def png():
    output = BytesIO()
    PillowImage.new("RGB", (4, 4), "red").save(output, format="PNG")
    return SimpleUploadedFile("bild.png", output.getvalue(), content_type="image/png")


class AtlasTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(create_user("admin"))
        self.institution = Institution.objects.create(name="gibb BMS")
        self.subject = Subject.objects.create(
            institution=self.institution, name="Mathematik"
        )

    def test_requires_admin(self):
        self.client.force_authenticate(create_user("user", admin=False))
        self.assertEqual(self.client.get("/api/atlas/institutions/").status_code, 403)
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get("/api/atlas/institutions/").status_code, 403)

    def test_builds_hierarchy(self):
        response = self.client.post(
            f"/api/atlas/institutions/{self.institution.uuid}/subjects/",
            {"name": "Deutsch"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        institutions = self.client.get("/api/atlas/institutions/").json()
        self.assertEqual(institutions[0]["subject_count"], 2)
        subjects = self.client.get(
            f"/api/atlas/institutions/{self.institution.uuid}/"
        ).json()
        self.assertEqual(
            [s["name"] for s in subjects["subjects"]], ["Deutsch", "Mathematik"]
        )

    def test_documentation_renders_safe_markdown(self):
        uuid = self.client.post(
            f"/api/atlas/subjects/{self.subject.uuid}/documentations/",
            {"title": "Ableitungen"},
            format="json",
        ).json()["uuid"]
        body = "# Titel\n\n<script>alert(1)</script>\n\n```\ncode\n```"
        response = self.client.patch(
            f"/api/atlas/documentations/{uuid}/", {"body": body}, format="json"
        )
        html = response.json()["html"]
        self.assertIn("<h1>Titel</h1>", html)
        self.assertIn("<code>code", html)
        self.assertNotIn("<script>", html)
        self.assertEqual(response.json()["subject"]["institution"]["name"], "gibb BMS")

    def test_overview_groups_by_institution_and_subject(self):
        LearningSet.objects.create(subject=self.subject, title="Formeln")
        Subject.objects.create(institution=self.institution, name="Leer")
        groups = self.client.get("/api/atlas/learning-sets/").json()
        self.assertEqual(len(groups), 1)
        self.assertEqual([s["name"] for s in groups[0]["subjects"]], ["Mathematik"])
        self.assertEqual(groups[0]["subjects"][0]["items"][0]["title"], "Formeln")
        self.assertEqual(self.client.get("/api/atlas/documentations/").json(), [])

    def create_cards(self, *pairs):
        learning_set = LearningSet.objects.create(subject=self.subject, title="Formeln")
        for position, (front, back) in enumerate(pairs):
            Flashcard.objects.create(
                learning_set=learning_set, front=front, back=back, position=position
            )
        return learning_set

    def answer(self, card, mode, answer):
        return self.client.post(
            f"/api/atlas/cards/{card.uuid}/answer/",
            {"mode": mode, "answer": answer},
            format="json",
        ).json()

    def test_rejects_card_without_front(self):
        learning_set = self.create_cards()
        response = self.client.post(
            f"/api/atlas/learning-sets/{learning_set.uuid}/cards/",
            {"front": " ", "back": "x"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_quiz_offers_up_to_four_distinct_options(self):
        pairs = [("a", "1"), ("b", "2"), ("c", "3"), ("d", "4"), ("e", "5"), ("f", "1")]
        learning_set = self.create_cards(*pairs)
        quiz = self.client.get(
            f"/api/atlas/learning-sets/{learning_set.uuid}/quiz/"
        ).json()
        self.assertEqual(len(quiz), 6)
        for card in quiz:
            backs = [option["back"] for option in card["options"]]
            self.assertEqual(len(backs), 4)
            self.assertEqual(len(set(backs)), 4)
            self.assertIn(card["uuid"], [option["uuid"] for option in card["options"]])

    def test_choice_then_write_marks_card_known(self):
        learning_set = self.create_cards(("Ableitung von x²", "2x"), ("sin", "cos"))
        card = learning_set.cards.get(front="sin")
        self.assertTrue(self.answer(card, "choice", str(card.uuid))["correct"])
        card.refresh_from_db()
        self.assertIsNone(card.last_known)
        result = self.answer(card, "write", "  COS ")
        self.assertEqual((result["correct"], result["back"]), (True, "cos"))
        card.refresh_from_db()
        self.assertTrue(card.last_known)

    def test_wrong_answer_marks_card_unknown(self):
        learning_set = self.create_cards(("a", "1"), ("b", "2"))
        card = learning_set.cards.get(front="a")
        other = learning_set.cards.get(front="b")
        self.assertFalse(self.answer(card, "choice", str(other.uuid))["correct"])
        detail = self.client.get(
            f"/api/atlas/learning-sets/{learning_set.uuid}/"
        ).json()
        self.assertEqual(detail["known_count"], 0)
        self.assertFalse(Flashcard.objects.get(pk=card.pk).last_known)

    def test_image_upload_and_card_image(self):
        image = self.client.post(
            "/api/atlas/images/", {"file": png()}, format="multipart"
        ).json()
        self.assertEqual(self.client.get(image["url"])["Content-Type"], "image/webp")
        learning_set = LearningSet.objects.create(subject=self.subject, title="Bilder")
        card = self.client.post(
            f"/api/atlas/learning-sets/{learning_set.uuid}/cards/",
            {"front": "", "front_image": image["uuid"]},
            format="json",
        ).json()
        self.assertEqual(card["front_image_url"], image["url"])
