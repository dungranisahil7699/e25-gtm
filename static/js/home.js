window.addEventListener('load', function() {

    var rnd = Math.random() * (3000 - 2000) + 2000;
    setTimeout(function() {
        document.getElementById('loader').remove();
    }, rnd);
});
    