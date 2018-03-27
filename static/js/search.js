/********** AUTOCOMPLETE ***********/
let searchForm = $('.search-form');
let searchInput = searchForm.find('[name=q]');
const typingInterval = 1500;
searchInput.keyup(function (e) {
    clearTimeout(typingInterval);
    typingTimer = setTimeout(performSearch, typingInterval);
});

searchInput.keydown(function () {
    clearTimeout(typingInterval);
});

function progressBarInit(){
    let progress = $('#progressBar');
    let progressLine = progress.find('.indeterminate');
    progressLine.addClass('purple');
    progress.addClass('white');
    progress.css("margin", "0");
    progress.css("height", "2px");
    progress.css("display", "block");
}

function performSearch(){
    progressBarInit();
    var q = searchInput.val();
    setTimeout(function(){
        window.location.href = `/search/?q=${q}`;
    },300);   
}