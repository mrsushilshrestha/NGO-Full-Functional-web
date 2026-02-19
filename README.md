# NHAF Nepal - National Health Association Force Nepal

A modern, scalable NGO website with full CMS (admin-controlled system) built with Django.

## Features

- **Home**: Hero banners, announcements, gallery, latest programs
- **About**: Mission, vision, objectives, founders, chapters, achievements
- **Programs/Events**: Upcoming & past programs with filtering and sorting
- **Team Directory**: Searchable member directory with QR codes, filters
- **Join Us**: Volunteer form, Membership/Collaboration form (eSewa, Khalti, Bank)
- **Impact**: Animated statistics
- **Contact**: Contact form, map (New Baneshwor, Kathmandu)
- **Donate**: Donation tiers, eSewa, Khalti, Bank transfer

## Setup

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # Windows
# or: source venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

If you get "disk I/O error" with SQLite (e.g. on OneDrive), move the project to a local folder or use PostgreSQL.

Visit http://127.0.0.1:8000/ for the website.

## Custom CMS (Easy-to-Use Admin)

**Login at: http://127.0.0.1:8000/admin-login/**

A custom CMS with a clean UI separate from Django admin. Use the same superuser credentials (must have staff access). Manage:
- **Home**: Banners, content blocks, announcements, gallery
- **About**: Organization info, founders, chapters, achievements
- **Impact**: Statistics with icons
- **Contact**: Contact info
- **Donation**: Tiers and bank details

Django admin at /admin/ is still available for Programs, Team, Membership applications, etc.

## Django Admin (Fallback)

- **Home content**: Admin → Core (HeroBanner, HomeContent, AnnouncementPopup, GalleryImage)
- **About**: Admin → About (OrganizationInfo, Founder, ChapterLocation, Achievement)
- **Programs**: Admin → Programs (Program, Category)
- **Team**: Admin → Team (Member, Chapter)
- **Membership fees**: Admin → Membership (MembershipFee)
- **Impact stats**: Admin → Impact (ImpactStat)
- **Contact info**: Admin → Contact (ContactInfo)

## Optional Enhancements (installed)

- **django-ckeditor**: Rich text editing in admin for Mission, Vision, Programs, etc.
- **django-crispy-forms**: Bootstrap-styled forms for Contact, Volunteer, Membership.
- **Payment gateways**: eSewa and Khalti integration for Donations and Membership.

## Payment Gateway Setup

**eSewa** (uses test credentials by default):
- Set `ESEWA_MERCHANT_ID` and `ESEWA_SECRET_KEY` for production
- Success/failure callbacks: `/donate/esewa/success/<tid>/`, `/donate/esewa/failure/<tid>/`

**Khalti** (requires secret key):
- Get key from [test-admin.khalti.com](https://test-admin.khalti.com) (sandbox) or [admin.khalti.com](https://admin.khalti.com) (production)
- Set `KHALTI_SECRET_KEY` in environment
- Donation/Membership will redirect to Khalti checkout

**Bank Transfer**: Add bank details in Admin → Donation → Bank Details

## Project Structure

```
ngo/
├── manage.py
├── requirements.txt
├── nhaf_nepal/          # Project settings
├── apps/
│   ├── core/            # Home
│   ├── about/
│   ├── programs/
│   ├── team/
│   ├── membership/
│   ├── impact/
│   ├── contact/
│   └── donation/
├── templates/
├── static/
└── media/
```
