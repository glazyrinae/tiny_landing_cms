# Tiny Landing CMS

A lightweight, easy-to-use Content Management System specifically designed for landing pages. This CMS provides a simple way to manage and update landing page content without the complexity of full-featured CMS platforms.

## Features

- 🚀 Fast and lightweight
- 📝 Simple content editing
- 🎨 Theme customization
- 📱 Mobile-responsive
- 🔒 Secure authentication
- 🔄 Real-time preview
- 📦 Easy deployment

## Tech Stack

- Backend: Node.js with Express
- Frontend: React
- Database: SQLite
- Authentication: JWT
- Styling: Tailwind CSS

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Git

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/tiny_landing_cms.git
    cd tiny_landing_cms
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Set up environment variables:

    ```bash
    cp .env.example .env
    ```

4. Initialize the database:

    ```bash
    npm run db:init
    ```

5. Start the development server:

    ```bash
    npm run dev
    ```

    The application will be available at `http://localhost:3000`

## Project Structure

```
tiny_landing_cms/
├── client/                 # Frontend React application
├── server/                 # Backend Node.js/Express application
├── database/              # Database migrations and seeds
├── public/               # Static files
└── docs/                 # Documentation
```

## Configuration

The CMS can be configured through the `.env` file. Available options include:

- `PORT`: Server port (default: 3000)
- `DATABASE_URL`: Database connection string
- `JWT_SECRET`: Secret key for JWT tokens
- `ADMIN_EMAIL`: Default admin email
- `ADMIN_PASSWORD`: Default admin password

## Usage

### Content Management

1. Login to the admin panel at `/admin`
2. Navigate to the content section
3. Edit your landing page content using the visual editor
4. Preview changes in real-time
5. Publish when ready

### Theme Customization

1. Access the theme editor in the admin panel
2. Modify colors, typography, and layout
3. Save changes to update the landing page appearance

## API Documentation

The CMS provides a RESTful API for content management:

- `GET /api/content`: Retrieve page content
- `POST /api/content`: Update page content
- `GET /api/themes`: List available themes
- `PUT /api/themes`: Update theme settings

## Development

### Running Tests

```bash
npm test
```

### Building for Production

```bash
npm run build
```

### Deployment

1. Build the project
2. Set production environment variables
3. Run database migrations
4. Start the server:

    ```bash
    npm start
    ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Security

- All admin routes are protected with JWT authentication
- Password hashing using bcrypt
- CSRF protection enabled
- XSS prevention measures
- Regular security updates

## Troubleshooting

Common issues and solutions:

1. **Database connection fails**
   - Check database credentials
   - Verify database server is running

2. **Cannot login to admin panel**
   - Ensure correct credentials in .env
   - Check server logs for errors

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
- Check the documentation
- Create an issue on GitHub
- Join our community Discord

## Acknowledgments

- Thanks to all contributors
- Built with open source software
- Inspired by the need for a simple landing page CMS

---

For detailed documentation, visit our [Wiki](https://github.com/yourusername/tiny_landing_cms/wiki)
