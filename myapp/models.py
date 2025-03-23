from mongoengine import Document, StringField, EmailField, BooleanField, ListField, DateTimeField, FloatField, EmbeddedDocument, EmbeddedDocumentField
import datetime

# Sub-document for multiple innovators
class Innovator(EmbeddedDocument):
    name = StringField(max_length=255)
    department = StringField(max_length=100)
    section = StringField(max_length=20)
    roll_no = StringField(max_length=20)
    email = EmailField()
    contact = StringField(max_length=15)

# Main application form
class SparkFundApplication(Document):
    # Project Details
    project_title = StringField(required=True, max_length=500)

    # Lead Innovator Details
    lead_innovator = EmbeddedDocumentField(Innovator, required=True)

    # Other Innovators
    other_innovators = ListField(EmbeddedDocumentField(Innovator))

    # Required Documents Checklist
    proof_of_concept = BooleanField(default=False)
    id_card = BooleanField(default=False)
    marksheet = BooleanField(default=False)
    community_certificate = BooleanField(default=False)
    aadhaar_card = BooleanField(default=False)
    bank_passbook = BooleanField(default=False)

    # File Uploads (Store filenames)
    annexure1 = StringField()
    annexure2 = StringField()
    annexure3 = StringField()
    annexure4 = StringField()
    annexure5 = StringField()
    annexure6 = StringField()

    # Project Classification
    project_sector = StringField(choices=[
        "agriculture", "biotech", "building", "renewable", "healthcare",
        "ict", "sensor", "manufacturing", "electronics", "materials",
        "waste", "housing", "transport", "telecom", "cyber", "drone", "textiles", "other"
    ])
    
    trl_level = StringField(choices=[f"TRL {i}" for i in range(10)])

    # Financial Support Information
    own_share = FloatField(default=0.0)
    support_sought = FloatField(default=0.0)

    # Mentor Information
    mentor_name = StringField(required=True, max_length=255)
    mentor_department = StringField(max_length=100)
    mentor_email = EmailField()
    mentor_mobile = StringField(max_length=15)

    # Declaration
    declaration = BooleanField(default=False)

    # Timestamp
    submitted_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {"collection": "spark_fund_applications"}
