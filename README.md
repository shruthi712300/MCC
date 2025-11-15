Political Party Membership Portal
A comprehensive web-based platform for managing political party membership lifecycle, branch activities, committees, and centralized reporting with full PDPA compliance.

🚀 Features
Core Functionality
Membership Registration - Online application form with proposer/seconder system

Member Workflow Management - Complete approval/rejection process with audit trails

Branch Management - Multi-level organizational structure with delegated administration

Central HQ Oversight - Cross-branch visibility and reporting

Role-Based Access Control - Secure multi-tier user permissions

User Roles
HQ Admin - Full system oversight and cross-branch management

Branch Admin - Branch-level member and activity management

Branch Committee - Read-only access to branch data

Member - Self-service profile management

Public User - Registration and information access

Security & Compliance
PDPA Compliance - Malaysia Personal Data Protection Act 2010 aligned

Data Encryption - Sensitive fields (IC numbers) encrypted at rest

IC Masking - Partial display (last 8 digits only) in user interfaces

Multi-Factor Authentication - Enhanced security for admin accounts

Session Management - Configurable timeout and logout policies

🛠 Technology Stack
Backend
Framework: Python Django with Django REST Framework

Database: PostgreSQL with encryption support

Authentication: Role-based access control with secure password hashing

Frontend
Technology: React with TypeScript

UI Framework: Material UI / Tailwind CSS

Build Tools: Modern frontend toolchain

Infrastructure
File Storage: AWS S3 / Cloud storage for documents and PDFs

Deployment: Dockerized containers with CI/CD pipelines

Web Server: NGINX reverse proxy

Security: HTTP/ITLS enforcement

📋 Key Modules
1. Membership Application
Online registration form with validation

CAPTCHA/bot prevention

Auto PDF generation and archival

Email acknowledgments and notifications

2. Member Workflow
Branch review and approval process

Status tracking (Pending → Approved/Rejected)

Automated email notifications

Complete audit trail

3. Branch Management
Branch directory and admin assignment

Activity posting and management

Local reporting and member statistics

4. HQ Management
Cross-branch oversight

Central activity management

Comprehensive reporting and analytics

5. Reporting & Analytics
Branch-level dashboards

HQ overview with growth trends

Export functionality (CSV, Excel)

Real-time statistics

🔒 Security Features
Encrypted database fields for PII

Masked IC display in all user-facing views

Strong password policies

Session timeout management

Secure file storage and access controls

📁 Project Structure
text
political-party-portal/
├── backend/                 # Django REST API
├── frontend/               # React TypeScript application
├── docker/                 # Docker configuration
├── docs/                   # Project documentation
├── scripts/                # Deployment and utility scripts
└── README.md
🚀 Getting Started
Prerequisites
Python 3.8+

Node.js 16+

PostgreSQL 12+

Docker (optional)

Installation
Backend Setup

bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Frontend Setup

bash
cd frontend
npm install
npm start
Database Configuration

Configure PostgreSQL connection in settings

Run initial migrations

Seed initial data (branches, admin users)

Docker Deployment
bash
docker-compose up -d
📊 API Documentation
Once running, access the API documentation at:

text
http://localhost:8000/api/docs/
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🛡️ Compliance Notes
This system is designed to comply with Malaysia's Personal Data Protection Act (PDPA) 2010:

Data encryption for sensitive information

Consent management during registration

Secure data handling and storage

Audit trails for data access and modifications

📞 Support
For technical support or questions about implementation, please contact the development team or create an issue in this repository.
