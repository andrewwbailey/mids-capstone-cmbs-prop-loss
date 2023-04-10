// Get the search input and icons
const searchInput = document.querySelector('.search-input');
const searchIcon = document.querySelector('.search-icon');
const clearIcon = document.querySelector('.clear-icon');
const searchCombox = document.querySelector('.search-combobox');

// Show/hide clear icon based on input value
searchInput.addEventListener('input', () => {
    if (searchInput.value) {
        clearIcon.style.display = 'block';
    } else {
        clearIcon.style.display = 'none';
    }
});
// Handle search functionality
function handleSearch() {
    const query = searchInput.value.trim();
    if (query) {
        console.log(`Search for: ${query}`);
        // Perform search here
        doQuery(searchInput.value, searchCombox.value);
    }
}

// Handle clear functionality
function handleClear() {
    searchInput.value = '';
    clearIcon.style.display = 'none';
    console.log('Search cleared');
    doClearall();
}

// Attach event listeners
searchIcon.addEventListener('click', handleSearch);
searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        handleSearch();
    }
});
clearIcon.addEventListener('click', handleClear);