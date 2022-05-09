document.getElementById("clean_main_form").addEventListener("click", product_list_func);
function product_list_func() {
    if(document.getElementById("id_website_domain")){
        document.getElementById("id_website_domain").value = '';
    }
    if(document.getElementById("id_subdomain_of_tracking_server")){
        document.getElementById("id_subdomain_of_tracking_server").value = '';
    }
    if(document.getElementById("id_gtm_web_container_id")){
        document.getElementById("id_gtm_web_container_id").value = '';
    }
    if(document.getElementById("id_ga4_property_id")){
        document.getElementById("id_ga4_property_id").value = '';
    }
    if(document.getElementById("id_ua_property_id")){
        document.getElementById("id_ua_property_id").value = '';
    }
    if(document.getElementById("id_facebook_pixel_id")){
        document.getElementById("id_facebook_pixel_id").value = '';
    }
    if(document.getElementById("id_facebook_auth_token")){
        document.getElementById("id_facebook_auth_token").value = '';
    }
    document.getElementById("id_connect_multiple_domains_to_the_same_server").checked = false;
    document.getElementById("id_hide_setup_from_ad_blockers").checked = false;
    document.getElementById("id_view_item_or_view_content").checked = false;
    document.getElementById("id_generate_lead").checked = false;
    document.getElementById("id_add_to_cart").checked = false;
    document.getElementById("id_begin_checkout_or_initiate_checkout").checked = false;
    document.getElementById("id_purchase").checked = false;
    document.getElementById("id_add_payment_info").checked = false;
    document.getElementById("id_add_to_wishlist").checked = false;
    document.getElementById("id_sign_up_or_complete_registration").checked = false;
    document.getElementById("id_search").checked = false;
    document.getElementById("id_contact").checked = false;
    document.getElementById("id_customize_product").checked = false;
    document.getElementById("id_donate").checked = false;
    document.getElementById("id_find_location").checked = false;
    document.getElementById("id_schedule").checked = false;
    document.getElementById("id_start_trial").checked = false;
    document.getElementById("id_submit_application").checked = false;
    document.getElementById("id_subscribe").checked = false;
    window.reload = "/mainform/";
}

document.getElementById("sign_out_main_form").addEventListener("click", logout_func);
function logout_func() {
    window.location = "/logout/";
}


window.addEventListener('load', function() {

    var rnd = Math.random() * (3000 - 2000) + 2000;
    setTimeout(function() {
        document.getElementById('loader').remove();
    }, rnd);
});
    