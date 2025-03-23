from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SparkFundApplication, Innovator


def home(request):
    return render(request, 'index.html')

def funds(request):
    return render(request, 'funds.html')

def incub(request):
    return render(request, 'incubation.html')

def form_view(request):
    return render(request, 'sparkform.html')

def newspc(request):
    return render(request, 'newsclipings.html')

def mentor(request):
    return render(request, 'mentorship.html')

def products(request):
    return render(request, 'product.html')

def recents(request):
    return render(request, 'recent.html')

#Database Submission View (Handles Form Submission)
def spark_fund_form(request):
    if request.method == "POST":
        try:
            # Get form data
            project_title = request.POST.get("project_title", "").strip()

            # Lead Innovator
            lead_innovator = Innovator(
                name=request.POST.get("name", "").strip(),
                department=request.POST.get("department", "").strip(),
                section=request.POST.get("section", "").strip(),
                roll_no=request.POST.get("roll_no", "").strip(),
                email=request.POST.get("email", "").strip(),
                contact=request.POST.get("mobile", "").strip()
            )

            # Collect other innovators (if any)
            other_innovators = []
            for i in range(1, 6):  # Allow up to 5 other innovators
                name = request.POST.get(f"other_name_{i}", "").strip()
                if name:
                    other_innovators.append(Innovator(
                        name=name,
                        department=request.POST.get(f"other_department_{i}", "").strip(),
                        section=request.POST.get(f"other_section_{i}", "").strip(),
                        roll_no=request.POST.get(f"other_roll_{i}", "").strip(),
                        email=request.POST.get(f"other_email_{i}", "").strip(),
                        contact=request.POST.get(f"other_contact_{i}", "").strip()
                    ))

            # Convert checkboxes (checkboxes return "on" when checked)
            proof_of_concept = request.POST.get("poc") == "on"
            id_card = request.POST.get("id_card") == "on"
            marksheet = request.POST.get("marksheet") == "on"
            community_certificate = request.POST.get("community") == "on"
            aadhaar_card = request.POST.get("aadhaar") == "on"
            bank_passbook = request.POST.get("bank") == "on"

            # Financial fields (ensure float values)
            own_share = float(request.POST.get("own_share", "0") or "0")
            support_sought = float(request.POST.get("support_sought", "0") or "0")

            # Mentor details
            mentor_name = request.POST.get("mentor_name", "").strip()
            mentor_department = request.POST.get("mentor_department", "").strip()
            mentor_email = request.POST.get("mentor_email", "").strip()
            mentor_mobile = request.POST.get("mentor_mobile", "").strip()

            # Declaration checkbox
            declaration = request.POST.get("declaration") == "on"

            # Create Spark Fund Application
            application = SparkFundApplication(
                project_title=project_title,
                lead_innovator=lead_innovator,
                other_innovators=other_innovators,
                proof_of_concept=proof_of_concept,
                id_card=id_card,
                marksheet=marksheet,
                community_certificate=community_certificate,
                aadhaar_card=aadhaar_card,
                bank_passbook=bank_passbook,
                project_sector=request.POST.get("sector", "").strip(),
                trl_level=request.POST.get("trl", "").strip(),
                own_share=own_share,
                support_sought=support_sought,
                mentor_name=mentor_name,
                mentor_department=mentor_department,
                mentor_email=mentor_email,
                mentor_mobile=mentor_mobile,
                declaration=declaration
            )

            # Save to MongoDB
            application.save()

            #Show success message
            messages.success(request, "Your application has been submitted successfully!")

            #Redirect back to the form page
            return redirect("spark_fund_form")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect("spark_fund_form")

    return render(request, "sparkform.html")

#API: Get All Applications
def get_applications(request):
    applications = SparkFundApplication.objects()
    data = [{
        "project_title": app.project_title,
        "lead_innovator": app.lead_innovator.name,
        "mentor_name": app.mentor_name,
        "submitted_at": app.submitted_at.strftime("%Y-%m-%d %H:%M:%S")  # Format date properly
    } for app in applications]

    return JsonResponse({"applications": data}, safe=False)
