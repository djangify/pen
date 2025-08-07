/**
 * Category Filter JavaScript
 * Handles category filtering functionality for the prompt generator
 */

document.addEventListener('DOMContentLoaded', function () {
  // Elements
  const categorySelect = document.getElementById('category');
  const difficultySelect = document.getElementById('difficulty');
  const promptTypeSelect = document.getElementById('promptType');

  // Set up event listeners for filter changes
  setupFilterListeners();

  /**
   * Set up listeners for filter changes
   */
  function setupFilterListeners() {
    // Listen for changes on all filter inputs
    if (categorySelect) {
      categorySelect.addEventListener('change', handleFilterChange);
    }

    if (difficultySelect) {
      difficultySelect.addEventListener('change', handleFilterChange);
    }

    if (promptTypeSelect) {
      promptTypeSelect.addEventListener('change', handleFilterChange);
    }
  }

  /**
   * Handle filter change events
   */
  function handleFilterChange() {
    // Update UI to reflect current filter state
    updateFilterUI();

    // Save filter preferences to localStorage
    saveFilterPreferences();

    // Skip availability check for now to avoid errors
    // updatePromptAvailability();
  }

  /**
   * Update the UI based on selected filters
   */
  function updateFilterUI() {
    // Add visual indicators for active filters
    if (categorySelect) {
      if (categorySelect.value) {
        categorySelect.classList.add('border-blue-500');
      } else {
        categorySelect.classList.remove('border-blue-500');
      }
    }

    if (difficultySelect) {
      if (difficultySelect.value) {
        difficultySelect.classList.add('border-blue-500');
      } else {
        difficultySelect.classList.remove('border-blue-500');
      }
    }

    if (promptTypeSelect) {
      if (promptTypeSelect.value) {
        promptTypeSelect.classList.add('border-blue-500');
      } else {
        promptTypeSelect.classList.remove('border-blue-500');
      }
    }
  }

  /**
   * Save filter preferences to localStorage
   */
  function saveFilterPreferences() {
    const preferences = {
      category: categorySelect ? categorySelect.value : '',
      difficulty: difficultySelect ? difficultySelect.value : '',
      promptType: promptTypeSelect ? promptTypeSelect.value : ''
    };

    localStorage.setItem('promptFilterPreferences', JSON.stringify(preferences));
  }

  /**
   * Restore filter preferences from localStorage
   */
  function restoreFilterPreferences() {
    const savedPreferences = localStorage.getItem('promptFilterPreferences');

    if (savedPreferences) {
      try {
        const preferences = JSON.parse(savedPreferences);

        // Apply saved preferences to the UI
        if (categorySelect && preferences.category) {
          categorySelect.value = preferences.category;
        }

        if (difficultySelect && preferences.difficulty) {
          difficultySelect.value = preferences.difficulty;
        }

        if (promptTypeSelect && preferences.promptType) {
          promptTypeSelect.value = preferences.promptType;
        }

        // Update UI to reflect restored preferences
        updateFilterUI();
      } catch (error) {
        console.error('Error restoring filter preferences:', error);
      }
    }
  }

  // Restore saved preferences when page loads
  restoreFilterPreferences();
});
