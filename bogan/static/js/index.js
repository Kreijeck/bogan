// mobile menu
const burgerIcon = document.querySelector('#burger');
const navbarMenu = document.querySelector('#nav-links');

burgerIcon.addEventListener('click', () => {
    navbarMenu.classList.toggle('is-active');
})

// toggle visibility of tables
function toggleVisibility(id) {
    const table = document.getElementById(id);
    if (table.style.display === "none") {
        table.style.display = "block";
    } else {
        table.style.display = "none";
    }
}

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
