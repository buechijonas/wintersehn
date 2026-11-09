from decimal import Decimal
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PillowImage
from rest_framework.test import APITestCase

from commons.testing import create_admin, create_user

from .models import (
    Exam,
    Flashcard,
    Institution,
    LearningSet,
    Subject,
    grade_tone,
    round_half,
)


def png():
    output = BytesIO()
    PillowImage.new("RGB", (4, 4), "red").save(output, format="PNG")
    return SimpleUploadedFile("bild.png", output.getvalue(), content_type="image/png")


class AtlasTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(create_admin())
        self.institution = Institution.objects.create(name="gibb BMS")
        self.subject = Subject.objects.create(
            institution=self.institution, name="Mathematik"
        )

    def test_requires_admin(self):
        self.client.force_authenticate(create_user("user"))
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


class GradeTests(APITestCase):
    def setUp(self):
        self.client.force_authenticate(create_admin())
        self.institution = Institution.objects.create(name="gibb BMS")
        self.math = Subject.objects.create(
            institution=self.institution, name="Mathematik"
        )
        self.german = Subject.objects.create(
            institution=self.institution, name="Deutsch"
        )

    def exam(self, subject, data):
        return self.client.post(
            f"/api/atlas/subjects/{subject.uuid}/exams/", data, format="json"
        )

    def test_rounds_to_half_grades(self):
        self.assertEqual(round_half(Decimal("4.25")), Decimal("4.5"))
        self.assertEqual(round_half(Decimal("4.24")), Decimal("4"))
        self.assertEqual(round_half(Decimal("5.75")), Decimal("6"))

    def test_tone_follows_thresholds(self):
        self.assertEqual(grade_tone(Decimal("3.5")), "error")
        self.assertEqual(grade_tone(Decimal("4")), "warning")
        self.assertEqual(grade_tone(Decimal("4.5")), "warning")
        self.assertEqual(grade_tone(Decimal("5")), "success")

    def test_requires_grade_or_parts(self):
        response = self.exam(self.math, {"name": "Leer"})
        self.assertEqual(response.status_code, 400)

    def test_exam_result_from_weighted_parts(self):
        parts = [
            {"name": "Theorie", "weight": "2", "grade": "5.5"},
            {"name": "Praxis", "weight": "1", "grade": "4"},
        ]
        exam = self.exam(self.math, {"name": "Algebra", "parts": parts}).json()
        self.assertEqual(exam["result"], "5.00")
        self.assertEqual(exam["tone"], "success")
        self.assertEqual(
            [part["name"] for part in exam["parts"]], ["Theorie", "Praxis"]
        )

    def test_subject_and_institution_averages(self):
        self.exam(self.math, {"name": "A", "weight": "2", "grade": "4.5"})
        self.exam(self.math, {"name": "B", "weight": "1", "grade": "5.25"})
        self.exam(self.german, {"name": "C", "grade": "3.6"})
        math = self.client.get(f"/api/atlas/subjects/{self.math.uuid}/").json()
        self.assertEqual(
            (math["average"], math["rounded"], math["tone"]), ("4.75", "5.0", "success")
        )
        institution = self.client.get(
            f"/api/atlas/institutions/{self.institution.uuid}/"
        ).json()
        subjects = {subject["name"]: subject for subject in institution["subjects"]}
        self.assertEqual(
            (subjects["Deutsch"]["rounded"], subjects["Deutsch"]["tone"]),
            ("3.5", "error"),
        )
        self.assertEqual(institution["average"], "4.25")
        self.assertEqual(
            (institution["rounded"], institution["tone"]), ("4.5", "warning")
        )

    def test_update_replaces_parts(self):
        exam = self.exam(
            self.math, {"name": "A", "parts": [{"name": "x", "grade": "6"}]}
        ).json()
        response = self.client.patch(
            f"/api/atlas/exams/{exam['uuid']}/",
            {"parts": [{"name": "y", "grade": "3"}, {"name": "z", "grade": "4"}]},
            format="json",
        ).json()
        self.assertEqual(response["result"], "3.50")
        self.assertEqual(Exam.objects.get().parts.count(), 2)
