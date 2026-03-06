# KMeans Engine

A web-based SaaS platform for customer segmentation using K-Means clustering. Upload customer data (Excel/CSV up to 5,000 rows), and the system automatically clusters them using K-Means++ with clear visualizations and export capabilities.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

## Features

- **Automated K-Means Clustering** with K-Means++ algorithm for optimal initial cluster centers
- **Data Upload Support** for Excel (.xlsx) and CSV (UTF-8) file formats
- **Automated Data Validation and Cleaning** with null and duplicate detection
- **Interactive Cluster Visualization** with professional charts and metrics
- **Results Export** in Excel (.xlsx) and CSV formats
- **Clean, Professional UI** with responsive design and smooth animations

## Tech Stack

### Frontend
- **Next.js 14** - React framework for production
- **React** - UI component library
- **Tailwind CSS** - Utility-first CSS framework
- **Shadcn UI** - Pre-built UI components
- **Acernity UI** - Modern UI components
- **Radix UI** - Headless UI primitives
- **Motion Dev & Magic UI** - Animation libraries

### Backend
- **Python FastAPI** - Modern, fast web framework for building APIs
- **Pandas** - Data manipulation and analysis
- **Scikit-Learn** - Machine learning library for K-Means clustering

### Database
- **MySQL 8.0** - Relational database for data storage

### Infrastructure
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container orchestration

## Quick Start

### Prerequisites

- Docker Desktop 4.20+ (recommended)
- Git 2.30+
- Windows, Linux, or macOS

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kmeans-engine.git
   cd kmeans-engine
   ```

2. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env.local

   # Edit .env.local with your configuration (see docs/SETUP.md for details)
   ```

3. **Start the application**
   ```bash
   # Windows
   start.bat

   # Linux/Mac
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Documentation

- **Setup Guide:** [docs/SETUP.md](docs/SETUP.md) - Detailed setup and configuration instructions
- **Project Planning:** `.planning/` - Project requirements, roadmap, and phase planning
- **Architecture:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) (coming soon) - System architecture and design decisions

## Development

### Local Development Commands

```bash
# Start all services
start.bat          # Windows
docker-compose up  # Linux/Mac

# Stop all services
stop.bat           # Windows
docker-compose down # Linux/Mac

# Restart services
restart.bat        # Windows
docker-compose restart # Linux/Mac

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Development Workflow

1. Create a new branch for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test locally

3. Commit your changes with conventional commit messages
   ```bash
   git commit -m "feat: add new feature"
   ```

4. Push and create a pull request
   ```bash
   git push origin feature/your-feature-name
   ```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## Project Structure

```
kmeans-engine/
├── backend/              # FastAPI application
│   ├── app/             # Application modules
│   ├── tests/           # Backend tests
│   └── requirements.txt # Python dependencies
├── frontend/            # Next.js application
│   ├── app/            # Next.js app directory
│   ├── components/     # React components
│   └── package.json     # Node.js dependencies
├── docs/                # Documentation
│   ├── SETUP.md        # Setup instructions
│   └── ARCHITECTURE.md # System architecture
├── scripts/             # Utility scripts
├── .planning/          # Project planning documents
├── docker-compose.yml  # Docker Compose configuration
├── start.bat          # Windows startup script
├── stop.bat           # Windows stop script
├── README.md          # This file
└── CONTRIBUTING.md    # Contribution guidelines
```

## Constraints

- **Row Limit:** Maximum 5,000 rows per upload
- **File Formats:** Excel (.xlsx) and CSV (UTF-8) only
- **User Accounts:** One account per user (no team collaboration in v1)
- **Data Retention:** Data stored for account lifetime with manual delete option

## Roadmap

The project is divided into 7 phases:

1. **Infrastructure Foundation** - Docker setup, database, Hello World endpoints
2. **Authentication System** - User registration, login, sessions
3. **Dashboard & Navigation** - Main dashboard, sidebar, project list
4. **Data Upload & Understanding** - File upload, validation, data preview
5. **Data Preparation & Cleaning** - Null/duplicate detection, auto/manual cleaning
6. **K-Means Modeling** - K selection, K-Means++ execution, progress tracking
7. **Visualization & Export** - Cluster charts, metrics, Excel/CSV download

See [`.planning/ROADMAP.md`](.planning/ROADMAP.md) for detailed phase information.

## Troubleshooting

For common issues and solutions, see the [Setup Guide](docs/SETUP.md) troubleshooting section.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Support

If you encounter any issues or have questions, please:
1. Check the [documentation](docs/)
2. Search existing [issues](https://github.com/yourusername/kmeans-engine/issues)
3. Create a new issue if needed

---

Built with Next.js, FastAPI, and MySQL. Powered by Docker.
