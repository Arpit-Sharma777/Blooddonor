from django.shortcuts import render, get_object_or_404, redirect
from .models import BloodBank, Donor, Donation ,BloodGroup # Ensure Donation is imported
from .forms import BloodBankForm, BloodGroupFormSet, DonorForm
from django.db.models import Q


def home(request):
    eligibility_criteria = [
        "You must be at least 18 years old.",
        "You must weigh at least 50 kg.",
        "You must not have any diseases that are transmissible via blood donation."
    ]
    importance_of_donating_blood = [
        "Blood donation saves lives by replenishing the blood supply for those in need.",
        "It helps patients undergoing surgeries, medical treatments, and emergencies.",
        "Regular blood donation also has health benefits for the donor, such as reducing the risk of certain diseases."
    ]
    dos_and_donts = {
        'before_donation': [
            "Do eat a healthy meal and drink plenty of water before donating.",
            "Don't consume fatty foods or alcohol before donation.",
            "Do get a good night's sleep before donation."
        ],
        'after_donation': [
            "Do eat iron-rich foods and stay hydrated after donation.",
            "Don't engage in strenuous physical activity immediately after donation.",
            "Do rest and avoid smoking or drinking alcohol for a few hours after donation."
        ]
    }
    context = {
        'eligibility_criteria': eligibility_criteria,
        'importance_of_donating_blood': importance_of_donating_blood,
        'dos_and_donts': dos_and_donts
    }
    return render(request, 'donors/home.html', context)

def register_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            form.save()
            return redirect('donor_list')
    else:
        form = DonorForm()
    return render(request, 'donors/register_donor.html', {'form': form})

def donor_list(request):
    blood_group = request.GET.get('blood_group', '')
    location = request.GET.get('location', '')
    donors = Donor.objects.filter(
        Q(blood_group__iexact=blood_group) & 
        Q(location__icontains=location) & 
        Q(disease='') &
        Q(weight__gte=50)
    )
    return render(request, 'donors/donor_list.html', {'donors': donors})

def blood_bank_list(request):
    blood_banks = BloodBank.objects.all()
    return render(request, 'donors/blood_bank_list.html', {'blood_banks': blood_banks})

def blood_bank_dashboard(request):
    blood_banks = BloodBank.objects.all()
    blood_groups = BloodGroup.objects.all()
    donor_count = Donor.objects.count()
    blood_bank_count = BloodBank.objects.count()
    recent_donations = Donation.objects.order_by('-date')[:5]  # Assuming you have a Donation model

    context = {
        'blood_banks': blood_banks,
        'blood_groups': blood_groups,
        'donor_count': donor_count,
        'blood_bank_count': blood_bank_count,
        'recent_donations': recent_donations,
    }
    return render(request, 'donors/blood_bank_dashboard.html', context)
def add_blood_bank(request):
    if request.method == 'POST':
        form = BloodBankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blood_bank_dashboard')  # Redirect to the dashboard after saving
    else:
        form = BloodBankForm()
    return render(request, 'donors/add_blood_bank.html', {'form': form})

def blood_bank_update(request, pk):
    blood_bank = get_object_or_404(BloodBank, pk=pk)
    if request.method == 'POST':
        form = BloodBankForm(request.POST, instance=blood_bank)
        formset = BloodGroupFormSet(request.POST, instance=blood_bank)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('blood_bank_dashboard')  # Redirect to the dashboard after saving
    else:
        form = BloodBankForm(instance=blood_bank)
        formset = BloodGroupFormSet(instance=blood_bank)
    return render(request, 'donors/blood_bank_update.html', {'form': form, 'formset': formset})

def blood_bank_delete(request, pk):
    blood_bank = get_object_or_404(BloodBank, pk=pk)
    if request.method == 'POST':
        blood_bank.delete()
        return redirect('blood_bank_list')
    return render(request, 'donors/blood_bank_confirm_delete.html', {'blood_bank': blood_bank})

