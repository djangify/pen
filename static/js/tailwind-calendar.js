/**
 * Writing Calendar using Tailwind CSS
 * Renders a calendar showing writing activity using only Tailwind classes
 */

// Calendar rendering function (using only Tailwind classes)
function renderCalendar(year, month) {
  console.log("Rendering calendar for", year, month);

  // Get DOM element
  const calendarContainer = document.getElementById('writing-calendar');
  if (!calendarContainer) {
    console.error("Calendar container not found!");
    return;

    // Clear calendar container
    calendarContainer.innerHTML = '';

    // Create date objects for the month
    const firstDayOfMonth = new Date(year, month, 1);
    const lastDayOfMonth = new Date(year, month + 1, 0);

    // Get day of week for first day (0 = Sunday, 6 = Saturday)
    const firstDayWeekday = firstDayOfMonth.getDay();

    // Create weekday headers
    const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    weekdays.forEach(day => {
      const dayElem = document.createElement('div');
      dayElem.className = 'text-center font-medium text-gray-600 py-2';
      dayElem.textContent = day;
      calendarContainer.appendChild(dayElem);
    });

    // Add empty cells for days before first day of month
    for (let i = 0; i < firstDayWeekday; i++) {
      const emptyCell = document.createElement('div');
      emptyCell.className = 'h-10 border border-gray-100 rounded bg-gray-50';
      calendarContainer.appendChild(emptyCell);
    }

    // Get today's date for highlighting
    const today = new Date();
    const isCurrentMonth = (today.getMonth() === month && today.getFullYear() === year);

    // Add cells for each day of the month
    for (let day = 1; day <= lastDayOfMonth.getDate(); day++) {
      const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const dayCell = document.createElement('div');

      // Default styling
      let cellClasses = [
        'h-10',
        'flex',
        'justify-center',
        'items-center',
        'border',
        'rounded',
        'relative',
        'transition-colors'
      ];

      // Check if day has writing data
      if (calendarData && calendarData[dateStr]) {
        const sessionData = calendarData[dateStr];

        // Color based on minutes
        if (sessionData.minutes > 40) {
          cellClasses.push('bg-blue-600', 'text-white', 'font-medium');
        } else if (sessionData.minutes > 20) {
          cellClasses.push('bg-blue-400', 'text-white');
        } else {
          cellClasses.push('bg-blue-200', 'text-gray-800');
        }

        // Add tooltip
        dayCell.setAttribute('title', `${sessionData.minutes} minutes | ${sessionData.words} words | ${sessionData.count} session(s)`);

        // Add session count badge if multiple sessions
        if (sessionData.count > 1) {
          const badge = document.createElement('span');
          badge.className = 'absolute top-0 right-0 -mt-1 -mr-1 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center text-xs';
          badge.textContent = sessionData.count;
          dayCell.appendChild(badge);
        }
      } else {
        cellClasses.push('bg-white', 'text-gray-700', 'hover:bg-gray-50');
      }

      // Highlight today
      if (isCurrentMonth && day === today.getDate()) {
        cellClasses.push('ring-2', 'ring-blue-500', 'font-bold');
      }

      dayCell.className = cellClasses.join(' ');
      dayCell.textContent = day;
      calendarContainer.appendChild(dayCell);
    }

    // Update month/year display
    const monthYearDisplay = document.getElementById('current-month-display');
    if (monthYearDisplay) {
      const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ];
      monthYearDisplay.textContent = `${monthNames[month]} ${year}`;
    }

    console.log("Calendar rendered");
  }

  // Create calendar grid
  const grid = document.createElement('div');
  grid.className = 'grid grid-cols-7 gap-1';

  // Add empty cells for days before first day of month
  for (let i = 0; i < firstDayWeekday; i++) {
    const emptyCell = document.createElement('div');
    emptyCell.className = 'aspect-square flex justify-center items-center';
    grid.appendChild(emptyCell);
  }

  // Get today's date for highlighting
  const today = new Date();
  const isCurrentMonth = (today.getMonth() === month && today.getFullYear() === year);

  // Add cells for each day of the month
  for (let day = 1; day <= lastDayOfMonth.getDate(); day++) {
    const dayCell = document.createElement('div');

    // Base classes for all day cells
    let dayCellClasses = [
      'aspect-square',
      'flex',
      'justify-center',
      'items-center',
      'rounded',
      'border',
      'border-gray-200',
      'text-sm',
      'relative',
      'hover:bg-gray-50',
      'transition-colors',
      'duration-150'
    ];

    // Create date string in YYYY-MM-DD format for data lookup
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

    // Default color is white background with gray text
    let colorClasses = ['bg-white', 'text-gray-600'];

    // Check if there's writing data for this day
    if (calendarData && calendarData[dateStr]) {
      const sessionData = calendarData[dateStr];

      // Determine color based on minutes spent
      if (sessionData.minutes > 40) {
        colorClasses = ['bg-blue-600', 'text-white'];
      } else if (sessionData.minutes > 20) {
        colorClasses = ['bg-blue-400', 'text-white'];
      } else {
        colorClasses = ['bg-blue-200', 'text-gray-800'];
      }

      // Add tooltip with session details
      dayCell.setAttribute('title', `${sessionData.minutes} minutes | ${sessionData.words} words | ${sessionData.count} session(s)`);

      // Add session count indicator if more than one session
      if (sessionData.count > 1) {
        const countBadge = document.createElement('span');
        countBadge.className = 'absolute top-0.5 right-0.5 bg-red-500 text-white text-xs w-4 h-4 rounded-full flex justify-center items-center';
        countBadge.textContent = sessionData.count;
        dayCell.appendChild(countBadge);
      }
    }

    // Highlight today with a blue border
    if (isCurrentMonth && day === today.getDate()) {
      dayCellClasses.push('font-bold', 'border-2', 'border-blue-500');
    }

    // Combine all classes 
    dayCell.className = [...dayCellClasses, ...colorClasses].join(' ');

    // Add day number
    const dayNumber = document.createElement('span');
    dayNumber.textContent = day;
    dayCell.appendChild(dayNumber);

    grid.appendChild(dayCell);
  }

  calendarContainer.appendChild(grid);

  // Update month/year display if needed
  const monthYearDisplay = document.getElementById('current-month-display');
  if (monthYearDisplay) {
    const monthNames = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    monthYearDisplay.textContent = `${monthNames[month]} ${year}`;
  }
}

// Initialize calendar navigation
function initCalendarControls() {
  // Get DOM elements
  const prevMonthBtn = document.getElementById('prev-month');
  const nextMonthBtn = document.getElementById('next-month');
  const calendarContainer = document.getElementById('writing-calendar');

  if (!calendarContainer || !prevMonthBtn || !nextMonthBtn) return;

  // Current date for initial display
  let currentDate = new Date();

  // Render the initial calendar
  renderCalendar(currentDate.getFullYear(), currentDate.getMonth());

  // Previous month button
  prevMonthBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar(currentDate.getFullYear(), currentDate.getMonth());
  });

  // Next month button
  nextMonthBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar(currentDate.getFullYear(), currentDate.getMonth());
  });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
  initCalendarControls();
});
