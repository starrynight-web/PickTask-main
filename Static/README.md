# PickTask Landing Page

A modern, responsive landing page for PickTask - a task management platform with AI-powered voice memo features.

## Features

### Design Elements
- **Custom Color Scheme**: Uses the specified colors (#071727, #31c9c1, #68e4b8)
- **Modern UI**: Clean, professional design with gradients and shadows
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Dynamic Animations**: Smooth transitions, hover effects, and scroll animations

### Interactive Features
- **Smooth Scrolling**: Navigation links smoothly scroll to sections
- **Auto-rotating Features**: Features automatically cycle every 4 seconds
- **Auto-rotating Testimonials**: Testimonials automatically cycle every 5 seconds
- **Interactive Navigation**: Click dots to manually navigate features/testimonials
- **Ripple Effects**: Button click animations
- **Parallax Effects**: Floating shapes move with scroll
- **Counter Animations**: Statistics animate when scrolled into view

### Sections

1. **Navigation Bar**
   - Logo with brand name "PickTask"
   - Menu options: Features, Pricing, Testimonials, Contact
   - "Get Started" button
   - Responsive hamburger menu for mobile

2. **Hero Section**
   - Main title: "Task Management Made Simple"
   - Subtitle with value proposition
   - Two CTA buttons: "Get Started — It's Free" and "Watch Demo"
   - Animated demo visuals in background
   - Floating geometric shapes

3. **Features Section**
   - **Voice Memos**: AI-powered task creation from audio
   - **Kanban Boards**: Visual workflow management
   - **Team Collaboration**: Real-time team features
   - **Progress Tracking**: Analytics and reporting
   - **Calendar Integration**: Task scheduling
   - **Time Tracking**: Built-in timers

4. **Testimonials Section**
   - Dynamic testimonial carousel
   - User photos and company information
   - Auto-rotation with manual navigation

5. **Call-to-Action Section**
   - Gradient background with floating shapes
   - Statistics counter animation
   - Prominent CTA buttons

6. **Footer**
   - Company information and SEO-friendly text
   - Organized link sections: Product, Resources, Company
   - Social media links
   - Copyright and legal links

## Technical Implementation

### Technologies Used
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with Flexbox and Grid
- **Vanilla JavaScript**: No frameworks, pure JS for interactivity
- **Font Awesome**: Icons
- **Google Fonts**: Inter font family

### Key CSS Features
- CSS Custom Properties (variables) for consistent theming
- CSS Grid and Flexbox for responsive layouts
- CSS Animations and Transitions
- Backdrop filters for glassmorphism effects
- CSS Gradients for visual appeal
- Media queries for responsive design

### JavaScript Features
- Intersection Observer API for scroll animations
- Event delegation for efficient event handling
- Smooth scrolling implementation
- Auto-rotation with pause on hover
- Counter animations with intersection observer
- Keyboard navigation support
- Accessibility features (focus management)

## File Structure

```
pickup/
├── index.html          # Main HTML structure
├── styles.css          # CSS styles and animations
├── script.js           # JavaScript functionality
└── README.md           # Project documentation
```

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Responsive design works on all screen sizes

## Performance Features

- Optimized animations using CSS transforms
- Efficient event handling with delegation
- Lazy loading of animations with Intersection Observer
- Minimal JavaScript footprint
- Optimized CSS with efficient selectors

## Accessibility Features

- Semantic HTML structure
- Keyboard navigation support
- Focus management
- ARIA labels where appropriate
- High contrast color scheme
- Responsive text sizing

## Getting Started

1. Open `index.html` in a web browser
2. The page will load with all animations and interactions
3. Navigate using the menu or scroll naturally
4. Click buttons to see ripple effects
5. Hover over elements to see hover animations

## Customization

### Colors
Update the CSS custom properties in `:root` to change the color scheme:
```css
:root {
    --primary-dark: #071727;
    --primary-teal: #31c9c1;
    --primary-green: #68e4b8;
}
```

### Content
- Update text content in `index.html`
- Modify feature descriptions and testimonials
- Change company information in the footer

### Animations
- Adjust animation durations in CSS
- Modify auto-rotation intervals in JavaScript
- Add or remove animation effects

## Future Enhancements

- Add actual sign-up/sign-in functionality
- Implement video modal for demo
- Add more interactive elements
- Include form validation
- Add loading states
- Implement dark mode toggle
- Add more accessibility features

## License

This project is created for demonstration purposes. Feel free to use and modify as needed.
