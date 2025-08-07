/**
 * Accordion functionality for profile sections
 */
document.addEventListener('DOMContentLoaded', function () {
  // Get all accordion headers
  const accordionHeaders = document.querySelectorAll('.accordion-header');

  // Add click event listener to each header
  accordionHeaders.forEach(header => {
    header.addEventListener('click', function () {
      // Get the target content element
      const targetId = this.getAttribute('data-target');
      const content = document.getElementById(targetId);

      if (!content) return; // Safety check in case element isn't found

      // Toggle the content visibility
      content.classList.toggle('hidden');

      // Toggle the icon rotation for the arrow
      const icon = this.querySelector('.accordion-icon');
      if (icon) {
        icon.classList.toggle('rotate-180');
      }
    });
  });

  // Ensure all accordion panels start closed by default
  const accordionContents = document.querySelectorAll('.accordion-content');
  accordionContents.forEach(content => {
    if (!content.classList.contains('hidden')) {
      content.classList.add('hidden');
    }
  });
});
