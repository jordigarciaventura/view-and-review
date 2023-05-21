$(document).ready(() => {
    var sections = document.querySelectorAll('.step');

    var observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                var sectionId = entry.target.id;
                history.pushState(null, null, '#' + sectionId);
            }
        });
    }, { threshold: 0.01 });

    $('.step').each((index, section) => {
        observer.observe(section);
    })
});