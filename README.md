# Pen and I Publishing

![Pen and I Publishing Logo](https://github.com/djangify/pen/blob/3cbcb0a0c28988d2c75fab1ad61e9f66c5e9619c/penandipublishing.png)

## Overview

Pen and I Publishing (www.penandipublishing.co.uk) is a UK-based platform designed to help individuals capture their life stories and memories through guided writing. The site focuses on making memoir writing accessible to everyone—not for publication, but for personal reflection, growth, and sharing with family.

The project is being developed in phases, with the first phase MVP now complete. This document outlines the current structure and planned development roadmap.

## Project Structure

```
pen_and_i/
├── blog/                          # Blog app
│   ├── admin.py                   # Admin configuration for blog posts
│   ├── models.py                  # Post and Category models
│   ├── serializers.py             # API serializers
│   ├── templates/                 # Blog templates
│   │   ├── category.html          # Category listing page
│   │   ├── detail.html            # Post detail page
│   │   └── list.html              # Blog listing page
│   ├── urls.py                    # Blog URL patterns
│   └── views.py                   # Blog views
├── core/                          # Core app
│   ├── templates/                 # Core templates
│   │   ├── about.html             # About page
│   │   ├── core/                  # Core template partials
│   │   │   └── _messages.html     # System messages component
│   │   ├── privacy_policy.html    # Privacy policy page
│   │   └── terms.html             # Terms and conditions page
│   ├── urls.py                    # Core URL patterns
│   └── views.py                   # Core views
├── pen/                           # Main project directory
│   ├── asgi.py                    # ASGI configuration
│   ├── settings.py                # Project settings
│   ├── urls.py                    # Main URL patterns
│   └── wsgi.py                    # WSGI configuration
├── prompt/                        # Prompt generator app
│   ├── admin.py                   # Admin configuration
│   ├── models.py                  # Tag, PromptCategory, WritingPrompt models
│   ├── serializers.py             # API serializers
│   ├── urls.py                    # Prompt URL patterns
│   └── views.py                   # Prompt views
├── static/                        # Static files
│   ├── css/                       # CSS files
│   ├── img/                       # Image files
│   │   └── penandi.png            # Site logo
│   └── js/                        # JavaScript files
│       ├── category-filter.js     # Filter functionality
│       ├── main.js                # Main site functionality
│       └── prompt-generator.js    # Prompt generator functionality
├── templates/                     # Global templates
│   ├── base.html                  # Base template
│   ├── components/                # Reusable components
│   │   ├── footer.html            # Site footer
│   │   └── nav.html               # Site navigation
│   └── index.html                 # Homepage
├── manage.py                      # Django management script
└── requirements.txt               # Project dependencies
```

## Current Features (Phase 1, Part 1 - Complete)

### 1. Writing Prompt Generator
- Random prompt generation based on filters
- Category, difficulty, and prompt type filtering
- Immediate display of prompts without page reload
- Mobile-responsive design

### 2. Blog Section
- Article categorization
- Publishing workflow with draft/published states
- Related posts and navigation between posts
- YouTube video embedding support
- SEO metadata fields for each post

### 3. Core Functionality
- Responsive navigation
- About page explaining the site's purpose
- Amazon integration for notebook purchases
- Basic analytics tracking

## Upcoming Development (Phase 1, Part 2 - In Progress)

### User Authentication and Personalization
- User registration and login functionality
- Secure authentication system
- User profile pages
- Ability to save and favorite prompts
- Personal prompt collection management

### Implementation Details
- Extend User model with profile information
- Create Favorites model to link users with prompts
- Implement session management
- Design profile dashboard interface
- Add appropriate permission checks to views

## Future Development Roadmap

### Phase 2 (Planned for April 2025)
**AI-Powered Question Expander**
- Allow users to enter basic memory prompts
- Generate thoughtful follow-up questions using AI
- Help users explore memories more deeply
- Implementation using Django and OpenAI API

### Phase 3 (Planned for May/June 2025)
**Memoir Writing Progress Tracker**
- Set personal writing goals
- Track progress towards writing milestones
- Gamification elements (badges, achievements)
- Writing streak tracking
- Optional sharing of milestones

## Technical Stack

- **Backend**: Django 5.1
- **Database**: MySQL
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Deployment**: Gunicorn, Whitenoise
- **API**: Django REST Framework
- **Editor**: Django Prose Editor for rich text

## Installation and Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with the following variables:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_NAME=your-db-name
   DATABASE_USER=your-db-user
   DATABASE_PASSWORD=your-db-password
   DATABASE_HOST=localhost
   DATABASE_PORT=3306
   ```
6. Run migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Load sample data: `python manage.py loaddata writing_prompts.json`
9. Run the development server: `python manage.py runserver`

## Contributing

Pen and I Publishing is currently under active development. If you'd like to contribute, please contact the project maintainer.

## License

All rights reserved. This codebase is proprietary and confidential.

## Contact

For any questions or feedback, please contact me - Diane Corriette - at https://www.djangify.com 
