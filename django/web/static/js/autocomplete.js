$(document).ready(() => {
    $("#search").autocomplete({
    source: "/search/json",
    minLength: 2,
    messages: {
        noResults: '',
        results: function() {}
    },
    select: (event, ui) => {
        event.preventDefault();
        window.location.href = "/movie/" + ui.item.id + "/";
    },
    open: function() {
        $("ul.ui-menu").width( $(this).innerWidth() );
    }
    })
    .data("ui-autocomplete")._renderItem = (ul, item) => {
        var inner_html = `
        <a href="/film/${item.id}" class="search-result">
            <image src="${item.poster_path}" />
            <div class="search-result-desc">
                <div class="search-result-desc-upper">
                    <div class="search-result-title cut-text">${item.title}</div>
                    <p class="search-result-date">${item.release_date}</p>
                </div>
                <div>${item.genres}</div>
            </div>
        </a>`;
        return $("<li>")
            .append(inner_html)
            .appendTo(ul);
    };
});