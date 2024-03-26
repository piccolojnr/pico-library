$(document).ready(function() {
    // API endpoint for popular books
    var apiUrl = "api/v1/";

    // Function to fetch popular books from API
    function fetchPopularBooks() {
        $.ajax({
            url: apiUrl+"books/popular?per_page=3",
            method: "GET",
            success: function(response) {
                // Process the response and display popular books
                displayPopularBooks(response);
            },
            error: function(xhr, status, error) {
                console.error("Error fetching popular books:", error);
            }
        });
    }
    function fetchPopularAuthors() {
        $.ajax({
            url: apiUrl+"agents/popular?per_page=3",
            method: "GET",
            success: function(response) {
                // Process the response and display popular books
                displayPopularAuthors(response);
            },
            error: function(xhr, status, error) {
                console.error("Error fetching popular authors:", error);
            }
        });
    }

    function generate_book_card(id, image, title, description) {
        return `
        <div class="book-card col-md-4" >
            <div class="card mb-4">
                <img src="${image}" class="card-img-top" alt="${title}">
                <div class="card-body">
                    <h5 class="card-title">${title}</h5>
                    <p class="card-text">${description}</p>
                    <a href="/books/${id}" data-id="${id}"  data-title="${title}" class="btn btn-primary">
                    Read More
                    </a>
                </div>
            </div>
        </div>
        `
    }



    function generate_author_card(alias,birth_date,death_date,id,name) 
    {
        return `
        <div class="book-card col-md-4" >
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">${name}</h5>
                    <p class="card-text">${birth_date} - ${death_date}</p>
                    <p class="card-text">${alias}</p>
                    <a href="/agents/${id}" data-id="${id}"  data-title="${name}" class="btn btn-primary">
                    Read More
                    </a>
                </div>
            </div>
        </div>
        `
    }

    function displayPopularAuthors(authors) {
        // Clear previous content
        $("#popular-authors > .container > .row").empty();

        // Iterate over each book and create HTML elements
        $.each(authors["items"], function(index, author) {
            var cardHtml = generate_author_card(author.alias, author.birth_date, author.death_date, author.id, author.name);

            // Append cardHtml to the container
            $("#popular-authors  > .container > .row").append(cardHtml);
        });
    }

    // Function to display popular books
    function displayPopularBooks(books) {
        // Clear previous content
        $("#popular-books > .container > .row").empty();

        // Iterate over each book and create HTML elements
        $.each(books["items"], function(index, book) {
            var cardHtml = generate_book_card(book.id, book.image, book.title, book.description);

            // Append cardHtml to the container
            $("#popular-books  > .container > .row").append(cardHtml);
        });
    }

    // Fetch popular books when the page loads
    fetchPopularBooks();
    fetchPopularAuthors();
});

