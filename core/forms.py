from django import forms

class VerificationCodeForm(forms.Form):
    verificationcode = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'placeholder': '6 Digit OTP', 'class':'form-control','style':'width:323px; display:inline-block; margin:5px 0px 0px -19px;'}), label='Enter OTP')


class FileUpload(forms.Form):
    server_file_upload = forms.FileField(label='Server File', widget=forms.FileInput(attrs={'style':'width: 210px;'}))
    client_file_upload = forms.FileField(label='Client File', widget=forms.FileInput(attrs={'style':'width: 210px;'}))


class MainInput(forms.Form):
    website_domain = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'website.com', 'class':'form-control'}), label='Website Domain *', required=False)
    subdomain_of_tracking_server = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Subdomain', 'class':'form-control'}), label='Subdomain of Tracking Server *', required=False)
    gtm_web_container_id = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'GTM Web Container ID', 'class':'form-control'}), label='GTM Web Container ID *', required=False)
    ga4_property_id = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'GA4 Property ID', 'class':'form-control'}), label='GA4 Property ID *', required=False)
    ua_property_id = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'UA Property ID', 'class':'form-control'}), label='UA Property ID (Optional)', required=False)
    facebook_pixel_id = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Facebook Pixel ID', 'class':'form-control'}), label='Facebook Pixel ID *', required=False)
    facebook_auth_token = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Facebook Auth Token', 'class':'form-control'}), label='Facebook Auth Token *', required=False)
    connect_multiple_domains_to_the_same_server = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    hide_setup_from_ad_blockers = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    view_item_or_view_content = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    generate_lead = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    add_to_cart = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    begin_checkout_or_initiate_checkout = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    purchase = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    add_payment_info = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    add_to_wishlist = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    sign_up_or_complete_registration = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    search = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    contact = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    customize_product = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    donate = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    find_location = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    schedule = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    start_trial = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    submit_application = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)
    subscribe = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), required=False)