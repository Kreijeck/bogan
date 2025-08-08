// mobile menu
const burgerIcon = document.querySelector('#burger');
const navbarMenu = document.querySelector('#nav-links');

burgerIcon.addEventListener('click', () => {
    navbarMenu.classList.toggle('is-active');
})

// Modern collapsible sections functionality - global version
function initializeCollapsibleSections() {
    const collapsibleHeaders = document.querySelectorAll('.collapsible-header');
    
    collapsibleHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);
            const chevron = this.querySelector('.collapse-icon i');
            
            if (targetSection) {
                // Toggle visibility
                if (targetSection.style.display === 'none') {
                    targetSection.style.display = 'block';
                    if (chevron) {
                        chevron.classList.remove('fa-chevron-down');
                        chevron.classList.add('fa-chevron-up');
                    }
                } else {
                    targetSection.style.display = 'none';
                    if (chevron) {
                        chevron.classList.remove('fa-chevron-up');
                        chevron.classList.add('fa-chevron-down');
                    }
                }
            }
        });
        
        // Add hover effect
        header.style.cursor = 'pointer';
        header.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(72, 95, 199, 0.1)';
        });
        header.addEventListener('mouseleave', function() {
            this.style.backgroundColor = 'transparent';
        });
    });
}

// Simple toggle function for detail buttons and other elements
function toggleElement(id) {
    const element = document.getElementById(id);
    if (element) {
        if (element.style.display === 'none') {
            element.style.display = 'block';
        } else {
            element.style.display = 'none';
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeCollapsibleSections();
});

// show markdown
async function loadMarkdown(file, targetId) {
const contentDiv = document.getElementById(targetId);

// Toggle Sichtbarkeit
if (contentDiv.style.display === 'none' || contentDiv.style.display === '') {
  try {
    // Lade die Markdown-Datei
    const response = await fetch(file);
    if (!response.ok) {
      throw new Error(`Datei "${file}" konnte nicht geladen werden.`);
    }
    const markdown = await response.text();

    // Konvertiere Markdown in HTML und zeige es an
    contentDiv.innerHTML = marked.parse(markdown);
    contentDiv.style.display = 'block';
  } catch (error) {
    contentDiv.innerHTML = `<p class="has-text-danger">Fehler: ${error.message}</p>`;
    contentDiv.style.display = 'block';
  }
} else {
  // Verberge den Inhalt bei erneutem Klick
  contentDiv.style.display = 'none';
}
}

/**
* Initialisiert eine Live-Suche für Listenelemente.
*
* @param {string} searchInputId - Die ID des Suchfeldes.
* @param {string} listContainerId - Die ID des Containers, in dem sich die Listenelemente befinden.
* @param {string} itemSelector - Ein CSS-Selektor, mit dem die einzelnen Listenelemente ausgewählt werden (z. B. ".list-item").
*/
function initLiveSearch(searchInputId, listContainerId, itemSelector) {
  const searchInput = document.getElementById(searchInputId);
  const listContainer = document.getElementById(listContainerId);

  if (!searchInput || !listContainer) {
    console.error('LiveSearch: Überprüfe bitte, ob die übergebenen Element-IDs korrekt sind.');
    return;
  }

  searchInput.addEventListener('input', () => {
    const filter = searchInput.value.toLowerCase();
    const items = listContainer.querySelectorAll(itemSelector);

    items.forEach(item => {
      const text = item.textContent.toLowerCase();
      item.style.display = text.includes(filter) ? '' : 'none';
    });
  });
}
