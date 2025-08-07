/**
 * Main JavaScript for Pen and I Publishing
 * Handles site-wide functionality
 */

document.addEventListener('DOMContentLoaded', function () {
  // Mobile menu toggle
  setupMobileMenu();
  
  // Handle external links
  setupExternalLinks();
  
  // Initialize any tooltips
  setupTooltips();
  
  // Setup navigation highlighting
  setupNavigationHighlighting();
});

/**
 * Set up the mobile menu toggle functionality
 */
function setupMobileMenu() {
  const mobileMenuButton = document.getElementById('mobile-menu-button');
  const mobileMenu = document.getElementById('mobile-menu');

  if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener('click', function () {
      // Toggle the 'hidden' class on the mobile menu
      mobileMenu.classList.toggle('hidden');

      // Update the aria-expanded attribute
      const expanded = mobileMenuButton.getAttribute('aria-expanded') === 'true' || false;
      mobileMenuButton.setAttribute('aria-expanded', !expanded);

      // Toggle between hamburger and X icons
      const hamburgerIcon = mobileMenuButton.querySelector('svg:first-child');
      const closeIcon = mobileMenuButton.querySelector('svg:last-child');
      
      if (hamburgerIcon && closeIcon) {
        hamburgerIcon.classList.toggle('hidden');
        hamburgerIcon.classList.toggle('block');
        closeIcon.classList.toggle('hidden');
        closeIcon.classList.toggle('block');
      }
    });
  }
}

/**
 * Set up external links to open in new tab
 */
function setupExternalLinks() {
  const links = document.querySelectorAll('a');

  links.forEach(link => {
    // Check if the link is external
    if (link.hostname !== window.location.hostname && link.hostname !== '') {
      // Add target and rel attributes
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');

      // Optionally add an icon to indicate external link
      if (!link.querySelector('.external-icon')) {
        const icon = document.createElement('span');
        icon.className = 'external-icon ml-1 text-xs';
        icon.innerHTML = '↗';
        link.appendChild(icon);
      }
    }
  });
}

/**
 * Set up tooltips for elements with data-tooltip attribute
 */
function setupTooltips() {
  const tooltipElements = document.querySelectorAll('[data-tooltip]');

  tooltipElements.forEach(element => {
    element.addEventListener('mouseenter', function () {
      const tooltipText = this.getAttribute('data-tooltip');

      // Create tooltip element
      const tooltip = document.createElement('div');
      tooltip.className = 'tooltip absolute bg-gray-800 text-white text-xs rounded py-1 px-2 z-50';
      tooltip.textContent = tooltipText;

      // Position tooltip above the element
      const rect = this.getBoundingClientRect();
      tooltip.style.top = (rect.top - 30) + 'px';
      tooltip.style.left = (rect.left + rect.width / 2 - 60) + 'px';

      // Add tooltip to body
      document.body.appendChild(tooltip);

      // Store tooltip reference in element
      this.tooltip = tooltip;
    });

    element.addEventListener('mouseleave', function () {
      // Remove tooltip
      if (this.tooltip) {
        this.tooltip.remove();
        this.tooltip = null;
      }
    });
  });
}

/**
 * Navigation Highlight Fix for Pen and I Publishing
 * This script ensures the blue underline correctly highlights the current page in the navigation.
 */
function setupNavigationHighlighting() {
  // Get the current page URL path
  const currentPath = window.location.pathname;

  // Get all navigation links
  const navLinks = document.querySelectorAll('nav a');

  // Remove active class from all links
  navLinks.forEach(link => {
    link.classList.remove('border-blue-500', 'text-gray-900');
    link.classList.add('border-transparent', 'text-gray-500', 'hover:border-gray-300', 'hover:text-gray-700');
  });

  // Add active class to the link that matches current page
  navLinks.forEach(link => {
    const linkPath = link.getAttribute('href');

    // Check if this link matches the current page
    if (linkPath === currentPath ||
      (currentPath.includes('/blog/') && linkPath.includes('/blog')) ||
      (currentPath.includes('/notebooks/') && linkPath.includes('/notebooks')) ||
      (currentPath.includes('/about/') && linkPath.includes('/about'))) {

      // Add active styles
      link.classList.remove('border-transparent', 'text-gray-500', 'hover:border-gray-300', 'hover:text-gray-700');
      link.classList.add('border-blue-500', 'text-gray-900');
    }
  });

  // Do the same for mobile menu
  const mobileNavLinks = document.querySelectorAll('#mobile-menu a');

  // Remove active class from all mobile links
  mobileNavLinks.forEach(link => {
    link.classList.remove('bg-blue-50', 'border-blue-500', 'text-blue-700');
    link.classList.add('border-transparent', 'text-gray-600', 'hover:bg-gray-50', 'hover:border-gray-300', 'hover:text-gray-800');
  });

  // Add active class to the mobile link that matches current page
  mobileNavLinks.forEach(link => {
    const linkPath = link.getAttribute('href');

    // Check if this link matches the current page
    if (linkPath === currentPath ||
      (currentPath.includes('/blog/') && linkPath.includes('/blog')) ||
      (currentPath.includes('/notebooks/') && linkPath.includes('/notebooks')) ||
      (currentPath.includes('/about/') && linkPath.includes('/about'))) {

      // Add active styles
      link.classList.remove('border-transparent', 'text-gray-600', 'hover:bg-gray-50', 'hover:border-gray-300', 'hover:text-gray-800');
      link.classList.add('bg-blue-50', 'border-blue-500', 'text-blue-700');
    }
  });
}
