// ========================================
// BOGAN JavaScript Library
// Globale JavaScript-Funktionen für alle Seiten
// ========================================

// Mobile Menu
const burgerIcon = document.querySelector('#burger');
const navbarMenu = document.querySelector('#nav-links');

if (burgerIcon && navbarMenu) {
    burgerIcon.addEventListener('click', () => {
        navbarMenu.classList.toggle('is-active');
    });
}

// Mobile Dropdown Toggle - Nur auf Mobile, Desktop bleibt unverändert
document.addEventListener('DOMContentLoaded', function() {
    function handleMobileDropdowns() {
        const dropdownLinks = document.querySelectorAll('.navbar-item.has-dropdown .navbar-link');
        
        dropdownLinks.forEach(link => {
            // Remove any existing mobile click listeners
            const newLink = link.cloneNode(true);
            link.parentNode.replaceChild(newLink, link);
            
            // Nur auf Mobile (≤768px) Click-Handler hinzufügen
            if (window.innerWidth <= 768) {
                newLink.addEventListener('click', function(e) {
                    e.preventDefault();
                    const parentDropdown = this.closest('.has-dropdown');
                    
                    // Toggle current dropdown
                    parentDropdown.classList.toggle('is-active');
                    
                    // Close other dropdowns
                    document.querySelectorAll('.navbar-item.has-dropdown').forEach(otherDropdown => {
                        if (otherDropdown !== parentDropdown) {
                            otherDropdown.classList.remove('is-active');
                        }
                    });
                });
            }
            // Auf Desktop: Keine Click-Handler, normale Hover-Funktionalität bleibt
        });
    }
    
    // Initialize on load
    handleMobileDropdowns();
    
    // Reinitialize on window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(handleMobileDropdowns, 250);
    });
});

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

// Show markdown content
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
 * Tab-Funktionalität für Bulma CSS Tabs
 * Aktiviert automatisch alle Tabs mit .tabs Navigation
 */
function initializeTabs() {
    // Handle desktop tabs (Bulma)
    const desktopTabs = document.querySelectorAll('.tabs li[data-tab]');
    const tabPanes = document.querySelectorAll('.tab-pane');

    desktopTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all desktop tabs
            desktopTabs.forEach(t => t.classList.remove('is-active'));
            // Add active class to clicked desktop tab
            this.classList.add('is-active');
            
            // Update mobile tabs to match
            const mobileTabs = document.querySelectorAll('.mobile-tab-button');
            mobileTabs.forEach(mTab => {
                mTab.classList.remove('active');
                if (mTab.getAttribute('data-tab') === targetTab) {
                    mTab.classList.add('active');
                }
            });
            
            // Show/hide content
            showTabContent(targetTab, tabPanes);
        });
    });
    
    // Handle mobile tabs (Custom buttons)
    const mobileTabs = document.querySelectorAll('.mobile-tab-button');
    mobileTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all mobile tabs
            mobileTabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked mobile tab
            this.classList.add('active');
            
            // Update desktop tabs to match
            desktopTabs.forEach(dTab => {
                dTab.classList.remove('is-active');
                if (dTab.getAttribute('data-tab') === targetTab) {
                    dTab.classList.add('is-active');
                }
            });
            
            // Show/hide content
            showTabContent(targetTab, tabPanes);
        });
    });
}

function showTabContent(targetTab, tabPanes) {
    // Hide all tab-panes
    tabPanes.forEach(pane => pane.classList.remove('is-active'));
    
    // Show the selected tab-pane
    const targetPane = document.getElementById('tab-' + targetTab);
    if (targetPane) {
        targetPane.classList.add('is-active');
    }
}

/**
 * Erweiterte Live-Suche für Player Overview
 * @param {Object} config - Konfiguration für die Suche
 * @param {string} config.searchInputId - ID des Suchfeldes
 * @param {string} config.containerSelector - Selektor für den Container
 * @param {string} config.itemSelector - Selektor für die Items
 * @param {string} config.noResultsSelector - Selektor für "keine Ergebnisse" Element
 * @param {string} config.totalCountSelector - Selektor für Anzahl-Counter
 * @param {string} config.searchAttribute - Attribut für suchbaren Text (default: 'data-searchable')
 */
function initializePlayerSearch(config) {
    const searchInput = document.getElementById(config.searchInputId);
    const container = document.querySelector(config.containerSelector);
    const noResults = document.querySelector(config.noResultsSelector);
    const totalCountSpan = document.querySelector(config.totalCountSelector);
    
    if (!searchInput || !container) return;
    
    const items = container.querySelectorAll(config.itemSelector);
    const totalItems = items.length;
    const searchAttribute = config.searchAttribute || 'data-searchable';

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        let visibleCount = 0;
        
        items.forEach(function(item) {
            const searchableText = item.getAttribute(searchAttribute);
            
            if (searchableText && searchableText.includes(searchTerm)) {
                item.style.display = '';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });
        
        // Update counter
        if (totalCountSpan) {
            totalCountSpan.textContent = visibleCount;
        }
        
        // Show/hide "no results" message
        if (noResults) {
            if (visibleCount === 0 && searchTerm !== '') {
                const noResultsText = noResults.querySelector('#noResultsText');
                if (noResultsText) {
                    noResultsText.textContent = `Es wurden keine Spieler für "${searchTerm}" gefunden.`;
                }
                noResults.style.display = '';
                container.style.display = 'none';
            } else {
                noResults.style.display = 'none';
                container.style.display = '';
            }
        }
        
        // Reset counter when search is cleared
        if (searchTerm === '' && totalCountSpan) {
            totalCountSpan.textContent = totalItems;
        }
    });
}

/**
 * Live-Suche für Games Overview (Tabellen-basiert)
 * @param {Object} config - Konfiguration für die Suche
 */
function initializeGamesTableSearch(config) {
    const searchInput = document.getElementById(config.searchInputId);
    const tableBody = document.querySelector(config.tableBodySelector);
    const totalCountSpan = document.querySelector(config.totalCountSelector);
    
    if (!searchInput || !tableBody) return;
    
    const gameRows = tableBody.querySelectorAll(config.rowSelector);
    const totalGames = gameRows.length;

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        let visibleCount = 0;
        
        gameRows.forEach(function(row) {
            const searchableText = row.getAttribute('data-searchable');
            
            if (searchableText && searchableText.includes(searchTerm)) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });
        
        // Update counter
        if (totalCountSpan) {
            totalCountSpan.textContent = visibleCount;
        }
        
        // Show/hide "no results" message
        let noResultsRow = document.getElementById('noResultsRow');
        if (visibleCount === 0 && searchTerm !== '') {
            if (!noResultsRow) {
                noResultsRow = document.createElement('tr');
                noResultsRow.id = 'noResultsRow';
                noResultsRow.innerHTML = `<td colspan="6" class="has-text-centered has-text-grey"><em>Keine Partien gefunden für "${searchTerm}"</em></td>`;
                tableBody.appendChild(noResultsRow);
            }
            noResultsRow.style.display = '';
        } else if (noResultsRow) {
            noResultsRow.style.display = 'none';
        }
        
        // Reset counter when search is cleared
        if (searchTerm === '' && totalCountSpan) {
            totalCountSpan.textContent = totalGames;
        }
    });
}

/**
 * Live-Suche für Player Detail mit Monats-Gruppierung
 * @param {Object} config - Konfiguration für die Suche
 */
function initializePlayerDetailSearch(config) {
    const searchInput = document.getElementById(config.searchInputId);
    
    if (!searchInput) return;
    
    const gameHistoryItems = document.querySelectorAll('.game-history-item');
    const monthSections = document.querySelectorAll('.month-section');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        let totalVisibleCount = 0;
        
        // Durch alle Monate gehen
        monthSections.forEach(function(monthSection) {
            const monthItems = monthSection.querySelectorAll('.game-history-item');
            let monthVisibleCount = 0;
            
            monthItems.forEach(function(item) {
                const searchableText = item.getAttribute('data-searchable');
                
                if (searchableText && searchableText.includes(searchTerm)) {
                    item.style.display = '';
                    monthVisibleCount++;
                    totalVisibleCount++;
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Verstecke den ganzen Monat wenn keine Spiele sichtbar sind
            if (monthVisibleCount === 0 && searchTerm !== '') {
                monthSection.style.display = 'none';
            } else {
                monthSection.style.display = '';
            }
        });
        
        // Auch fallback items durchsuchen
        const fallbackItems = document.querySelectorAll('#fallbackGamesGrid .game-history-item');
        fallbackItems.forEach(function(item) {
            const searchableText = item.getAttribute('data-searchable');
            
            if (searchableText && searchableText.includes(searchTerm)) {
                item.style.display = '';
                totalVisibleCount++;
            } else {
                item.style.display = 'none';
            }
        });
        
        // Show/hide "no results" message for game history
        let noResultsHistory = document.getElementById('noResultsHistory');
        if (totalVisibleCount === 0 && searchTerm !== '') {
            if (!noResultsHistory) {
                noResultsHistory = document.createElement('div');
                noResultsHistory.id = 'noResultsHistory';
                noResultsHistory.className = 'notification is-warning has-text-centered';
                noResultsHistory.innerHTML = '<strong>Keine Partien gefunden</strong><br><span id="noResultsHistoryText">Es wurden keine Partien für den Suchbegriff gefunden.</span>';
                const gameHistorySection = document.getElementById('game-history-section');
                if (gameHistorySection) {
                    gameHistorySection.appendChild(noResultsHistory);
                }
            }
            const noResultsText = noResultsHistory.querySelector('#noResultsHistoryText');
            if (noResultsText) {
                noResultsText.textContent = `Es wurden keine Partien für "${searchTerm}" gefunden.`;
            }
            noResultsHistory.style.display = '';
        } else {
            if (noResultsHistory) noResultsHistory.style.display = 'none';
        }
        
        // Reset visibility when search is cleared
        if (searchTerm === '') {
            monthSections.forEach(function(monthSection) {
                monthSection.style.display = '';
            });
        }
    });
}

/**
 * Simple Live-Suche für Boardgames Grid
 * @param {Object} config - Konfiguration für die Suche
 */
function initializeBoardgamesSearch(config) {
    const searchInput = document.getElementById(config.searchInputId);
    const gameGrid = document.querySelector(config.gridSelector);
    
    if (!searchInput || !gameGrid) return;
    
    const gameItems = gameGrid.querySelectorAll(config.itemSelector);

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        gameItems.forEach(function(item) {
            const gameTitle = item.querySelector('.game-title');
            if (gameTitle) {
                const titleText = gameTitle.textContent.toLowerCase();
                if (titleText.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            }
        });
    });
}

// ========================================
// Dynamic Style Applier
// Konvertiert data-Attribute zu CSS-Styles für Jinja2-Templates
// ========================================
function applyDynamicStyles() {
    // Performance Bars
    document.querySelectorAll('[data-width]').forEach(element => {
        const width = element.getAttribute('data-width');
        if (width !== null) {
            element.style.width = width + '%';
        }
    });
    
    // Position Elements (left positioning)
    document.querySelectorAll('[data-left]').forEach(element => {
        const left = element.getAttribute('data-left');
        if (left !== null) {
            element.style.left = left + '%';
        }
    });
    
    // Win Bar Fill Elements (special case for win bars)
    document.querySelectorAll('.win-bar-compact-fill[data-width]').forEach(element => {
        const width = element.getAttribute('data-width');
        if (width !== null) {
            element.style.width = width + '%';
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeCollapsibleSections();
    initializeTabs();
    applyDynamicStyles();  // Apply dynamic styles from data attributes
});
