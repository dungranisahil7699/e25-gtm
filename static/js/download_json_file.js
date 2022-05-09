window.addEventListener('load', function() {

    var rnd = Math.random() * (3000 - 2000) + 2000;
    setTimeout(function() {
        document.getElementById('loader').remove();
    }, rnd);
});


document.getElementById("sign_out_id").addEventListener("click", logout_func);
function logout_func() {
    window.location = "/logout/";
}
