# Nigeria Transport and Logistics Summit and Awards

A comprehensive Django web application for managing the Nigeria Transport and Logistics Summit and Awards event. This application features a modern, responsive design with full admin panel management for event content, speakers, sponsors, nominations, and more.

## Features

- **Admin-Managed Content**: Full CMS capabilities through Django admin
- **Responsive Design**: Material Design with Nigerian green theme
- **Speakers Management**: Admin-controlled speaker profiles and showcase
- **Sponsorship System**: Tiered sponsor management with logo displays
- **Nominations System**: Award categories and nomination submissions
- **Event Content**: Configurable hero sections, about content, and site settings
- **Exhibition Management**: Package management for exhibitors
- **Media Management**: Image uploads for logos, backgrounds, and speaker photos

## Content Management (for site admins)

Log in at `/admin/`. The dashboard has quick actions, registration stats and a guide.

**Edit the live site:** click **✏️ Edit site live** (or open any page while logged in and press
**Edit page** in the toolbar at the bottom-left). Then:

- Click any highlighted text to type over it. Press Enter (or click away) to save, Esc to cancel.
- Click any picture (logos, speaker photos, about image) to replace it. Heroes have a
  **Replace background** button.
- Bulleted lists (e.g. nomination guidelines) are edited as one item per line.
- Black "Manage…" buttons open the admin for lists (speakers, sponsors, cards, tickets…).

**Gallery:** create one album per event under *Gallery › Gallery Albums*. Upload many photos at
once from the album form, or on the album page in Edit mode (drag & drop, drag to reorder,
click captions to edit). Photos are resized automatically (max 2400px plus an 800px thumbnail).

**Registration:** manage tickets and prices under *Registration › Ticket Types* (set a capacity
to cap numbers). Open or close registration and configure confirmation emails in *Site Settings*.
Registrants receive a reference number (e.g. `TLNG-2026-7KQ2MX`). Export registrations or
nominations to CSV with the admin action "Export selected to CSV".

### For developers

- Editable copy uses the template tags in `summit/templatetags/cms.py`:
  `{% cms_block "page.section.key" "Default text" %}`, `{% cms_field obj "field" %}`,
  `{% cms_list "key" "item 1 | item 2" %}`, `<img {% cms_image obj "field" %}>`.
  New blocks are created automatically the first time a page renders.
- Live-edit endpoints live in `summit/cms.py`. Only models listed in `EDITABLE_MODELS`,
  text/image fields, and users with the model's *change* permission can edit.
- Run tests with `python manage.py test summit`.

## Requirements

- Python 3.11+
- Django 5.2+
- MySQL/MariaDB (for production)
- Pillow (for image handling)

## Local Development Setup

1. **Clone the repository**
   ```bash
   cd tlng_summit
   ```

2. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Website: http://127.0.0.1:8000
   - Admin Panel: http://127.0.0.1:8000/admin

## Production Deployment (cPanel)

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

### Quick Deployment Steps:

1. **Prepare environment**
   ```bash
   cp .env.example .env
   # Edit .env with your production settings
   ```

2. **Run deployment script**
   ```bash
   ./deploy.sh
   ```

3. **Upload to cPanel hosting**

4. **Configure database and domain**

## Project Structure

```
tlng_summit/
├── summit/                     # Main Django app
│   ├── models.py              # Database models
│   ├── admin.py               # Admin interface configuration
│   ├── views.py               # Application views
│   └── urls.py                # URL routing
├── templates/                  # HTML templates
│   └── summit/
│       ├── base.html          # Base template
│       ├── home.html          # Homepage
│       ├── speakers.html      # Speakers page
│       ├── sponsorship.html   # Sponsorship page
│       └── nominations.html   # Nominations page
├── static/                     # Static assets
│   ├── css/                   # Custom CSS
│   ├── js/                    # JavaScript files
│   └── images/                # Static images
├── tlng_summit_project/        # Django project settings
│   ├── settings.py            # Development settings
│   ├── settings_production.py # Production settings
│   └── urls.py                # Main URL configuration
├── passenger_wsgi.py           # WSGI configuration for cPanel
├── requirements.txt            # Python dependencies
├── deploy.sh                  # Deployment script
├── .htaccess                  # Apache configuration
└── DEPLOYMENT_GUIDE.md        # Detailed deployment instructions
```

## Key Models

### Core Models
- **SiteSettings**: Global site configuration (logo, contact info, social media)
- **EventContent**: Homepage content (hero section, about text, features, stats)
- **Speaker**: Speaker profiles with photos and social links
- **Sponsor**: Sponsor information with logos and sponsorship levels
- **SponsorshipLevel**: Tiered sponsorship packages with pricing
- **AwardCategory**: Award categories for nominations
- **Nomination**: Nomination submissions
- **ExhibitionPackage**: Exhibition packages and pricing
- **Exhibitor**: Exhibitor information and package selections

## Admin Interface

The Django admin interface provides comprehensive management for:

- **Site Settings**: Logo, favicon, hero background, contact information
- **Event Content**: Homepage sections, features, statistics
- **Speakers**: Add/edit speaker profiles with photos and social links  
- **Sponsors**: Manage sponsor logos, information, and sponsorship levels
- **Award Categories**: Create and manage award categories
- **Nominations**: View and manage award nominations
- **Exhibition**: Manage exhibition packages and exhibitor information

## Design Features

- **Nigerian Green Theme**: Professional color scheme using #008751
- **Material Design**: Modern UI components and layouts
- **Responsive Layout**: Mobile-first design that works on all devices
- **Tiered Sponsor Display**: Different sizes for Platinum/Gold vs Silver/Bronze sponsors
- **Admin-Configurable Content**: All text, images, and settings manageable through admin
- **Hero Statistics**: Configurable stats display in hero section
- **Feature Showcases**: Highlight key event benefits and topics

## Currency and Localization

- **Nigerian Naira (₦)**: All pricing displayed in local currency
- **Number Formatting**: Comma-separated numbers for better readability
- **Local Context**: Nigerian companies and locations in sample data

## Security Features

- **Production Settings**: Separate configuration for production deployment
- **Security Headers**: XSS protection, content type sniffing prevention
- **HTTPS Enforcement**: SSL redirect and secure cookies in production
- **Environment Variables**: Sensitive data stored in environment variables
- **File Permissions**: Proper file permissions for hosting environments

## Customization

The application is highly customizable through the admin interface:

1. **Site Branding**: Upload custom logos and set site name
2. **Hero Section**: Custom background images and content
3. **Event Information**: Dates, venues, descriptions
4. **Speaker Profiles**: Photos, bios, social media links
5. **Sponsor Management**: Logos, descriptions, website links
6. **Award Categories**: Custom categories and descriptions
7. **Contact Information**: Phone, email, social media links

## Support and Maintenance

- **Error Logging**: Comprehensive logging for troubleshooting
- **Database Backups**: Regular backup procedures recommended
- **Static Files**: Efficient handling and caching
- **Performance**: Optimized queries and caching strategies

## License

This project is proprietary software developed for the Nigeria Transport and Logistics Summit and Awards.

## Contributing

This is a closed-source project. For issues or feature requests, please contact the development team.

---

**For deployment assistance, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**