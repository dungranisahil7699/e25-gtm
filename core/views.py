import base64
import json
from django.contrib import messages, auth
from django.shortcuts import redirect, render
from core.forms import VerificationCodeForm, FileUpload, MainInput
from .models import *
from django.core.mail import send_mail
from django.conf import settings
import string
import random
import time
import uuid
from django.core.files.storage import FileSystemStorage

static_url = './static/'

# Create your views here.
def send_verification_code(user_object):
    code = ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for x in range(6))
    gmail_user = settings.EMAIL_HOST_USER
    to = [user_object]
    subject = 'Email Verification'
    body = f'Your mail verification Code is: {code}'
    send_mail(subject=subject, from_email = gmail_user , message=body ,recipient_list =to, fail_silently=False)
    return code


def singup(request):
    if request.method == 'POST':
        form1 = VerificationCodeForm(request.POST)
        aj = json.dumps(request.POST)
        aj = json.loads(aj)
        if aj.get('name') == 'Send_code':
            if aj['email']:
                user_email = aj['email']
                code = ""
                if memberdetails.objects.filter(email=user_email).exists():
                    code = send_verification_code(user_email)
                    messages.success(request, "Verification Code Sent Successfully. Verify your Mail.")
                    memberdetails.objects.filter(email=user_email).update(verificationcode=code)
                    return redirect("singup")
                else:
                    code = send_verification_code(user_email)
                    split_time = str(time.time()).split(".")[0]

                    user_account_id = f'60{split_time[2:]}'
                    containerID=f'{split_time[2:8]}22224444'
                    generate_imageids = split_time + "2342342234978" + ''.join(random.choice(string.digits) for x in range(3))
                    imageID = base64.b64encode(bytes(generate_imageids, 'utf-8'))
                    client_data_client_end_point = ''.join(random.choice(string.ascii_lowercase) for x in range(6))
                    server_data_client_end_point = ''.join(random.choice(string.ascii_lowercase) for x in range(6))
                    gtm_end_point = ''.join(random.choice(string.ascii_lowercase) for x in range(6))

                    memberdetails.objects.create(email=user_email, verificationcode=code, accountId = user_account_id, containerId = containerID, imageId = imageID, client_data_client_endpoint = client_data_client_end_point, server_data_client_endpoint = server_data_client_end_point, gtm_endpoint = gtm_end_point)
                    return redirect("singup")

        if 'Login_User' in request.POST:
            if request.POST['mail'] and request.POST['verificationcode']:
                user_email = request.POST['mail']
                user_email_code = request.POST['verificationcode']
                
                if memberdetails.objects.filter(email=user_email).exists():
                    verify_code = memberdetails.objects.get(email=user_email)
                    if user_email_code == verify_code.verificationcode:
                        request.session['email'] = user_email
                        return redirect('mainform')
                    else:
                        messages.error(request, "Invalide Code.")
                        return redirect('singup')
                else:
                    messages.error(request, "Verify your email")
                    return redirect('singup')
    else:
        form1 = VerificationCodeForm()
        email_param = request.session.get('email')
        if email_param is not None:
            if request.session.get('email') == None:
                return render(request, 'singup.html', {'form1':form1})
            else:
                return redirect('home')
        else:
            return render(request, 'singup.html', {'form1':form1})

    return render(request, 'singup.html', {'form1':form1})


def home(request):

    if request.method == "POST":
        if request.session.get('email') and request.session.get('email') != None:
            email = request.session.get('email')
            user = memberdetails.objects.get(email=email)
            if user.is_superuser == True:
                member_id = user.id
                form = FileUpload(request.POST)
                if "Upload_server_file" in request.POST:
                    file = request.FILES['server_file_upload']
                    file_name, file_extension = str(file).split(".")
                    file_name = str(file_name).replace("-","").replace(" ","_")
                    file_extension = "."+file_extension.lower()

                    if file_extension == ".json":

                        file_unique_id = "_" + str(uuid.uuid4().hex[:6])
                        new_file_name = file_name + file_unique_id + file_extension
                        img = request.FILES['server_file_upload']
                        file_URL = static_url + 'server_json_files/'

                        fs = FileSystemStorage(location=file_URL, base_url=None)
                        filename = fs.save(new_file_name, img)
                        uploaded_file_url = fs.url(filename)

                        file_type = 'server'
                        JSON_file = files.objects.create(file_name = new_file_name, file_type = file_type, member_id = member_id)
                        messages.success(request, 'Server File Upload Successfully.')
                        return redirect('home')
                    else:
                        messages.error(request, "Select Only JSON File.")
                        return redirect('home')

                elif "Upload_client_file" in request.POST:
                    file = request.FILES['client_file_upload']
                    file_name, file_extension = str(file).split(".")
                    file_name = str(file_name).replace("-","").replace(" ","_")
                    file_extension = "."+file_extension.lower()

                    if file_extension == ".json":

                        file_unique_id = "_" + str(uuid.uuid4().hex[:6])
                        new_file_name = file_name + file_unique_id + file_extension
                        img = request.FILES['client_file_upload']
                        file_URL = static_url + 'client_json_files/'

                        fs = FileSystemStorage(location=file_URL, base_url=None)
                        filename = fs.save(new_file_name, img)
                        uploaded_file_url = fs.url(filename)

                        file_type = 'client'
                        JSON_file = files.objects.create(file_name = new_file_name, file_type = file_type, member_id = member_id)
                        messages.success(request, 'Client File Upload Successfully.')
                        return redirect('home')
                    else:
                        messages.error(request, "Select Only JSON File.")
                        return redirect('home')
            return render(request, 'home.html', {'form':form})
        else:
            return redirect('singup')
    else:
        if request.session.get('email') and request.session.get('email') != None:
            email = request.session.get('email')
            user = memberdetails.objects.get(email=email)
            if user.is_superuser == True:
                form = FileUpload()
                return render(request, 'home.html', {'form':form})
            else:
                return redirect('mainform')
                # form = MainInput()
                # return render(request, 'main_input_form.html', {'form':form})
        else:
            return redirect('singup')


def mainform(request):
    if request.method == 'POST':
        if request.session.get('email') and request.session.get('email') != None:
            email = request.session.get('email')
            user = memberdetails.objects.get(email=email)
            if user.is_superuser == False:
                member_id = user.id
                accountId = user.accountId
                containerId = user.containerId
                client_data_client_endpoint = user.client_data_client_endpoint
                server_data_client_endpoint = user.server_data_client_endpoint
                gtm_endpoint = user.gtm_endpoint
        
                form = MainInput()

                website_domain = request.POST['website_domain']
                subdomain_of_tracking_server = request.POST['subdomain_of_tracking_server']
                gtm_web_container_id = request.POST['gtm_web_container_id'] 
                ga4_property_id = request.POST['ga4_property_id']
                ua_property_id = request.POST['ua_property_id']
                facebook_pixel_id = request.POST['facebook_pixel_id']
                facebook_auth_token = request.POST['facebook_auth_token']

                connect_multiple_domains_to_the_same_server = request.POST.get('connect_multiple_domains_to_the_same_server')
                hide_setup_from_ad_blockers = request.POST.get('hide_setup_from_ad_blockers')
                view_item_or_view_content = request.POST.get('view_item_or_view_content')
                generate_lead = request.POST.get('generate_lead')
                add_to_cart = request.POST.get('add_to_cart')
                begin_checkout_or_initiate_checkout = request.POST.get('begin_checkout_or_initiate_checkout')
                purchase = request.POST.get('purchase')
                add_payment_info = request.POST.get('add_payment_info')
                add_to_wishlist = request.POST.get('add_to_wishlist')
                sign_up_or_complete_registration = request.POST.get('sign_up_or_complete_registration')
                search = request.POST.get('search')
                contact = request.POST.get('contact')
                customize_product = request.POST.get('customize_product')
                donate = request.POST.get('donate')
                find_location = request.POST.get('find_location')
                schedule = request.POST.get('schedule')
                start_trial = request.POST.get('start_trial')
                submit_application = request.POST.get('submit_application')
                subscribe = request.POST.get('subscribe')
                
                # ServerFile
                with open(str(static_url)+ 'server_json_files/' + 'Template - Base - Server.json', "r") as outfile:
                    json_object = json.load(outfile)

                for k in json_object['containerVersion']:
                    if k == "path":
                        path_list = str(json_object['containerVersion'][k]).split('/')
                        path_list[1] = accountId
                        path_list[3] = containerId
                        join_string ='/'.join(path_list)
                        json_object['containerVersion'][k] = join_string
                    if k == "accountId":
                        json_object['containerVersion'][k] = accountId
                    if k == "containerId":
                        json_object['containerVersion'][k] = containerId
                    if k == "tagManagerUrl":
                        tagManagerUrl_path_list = str(json_object['containerVersion'][k]).split('/')
                        tagManagerUrl_path_list[6] = accountId
                        tagManagerUrl_path_list[8] = containerId
                        tagManagerUrl_path_join_string ='/'.join(tagManagerUrl_path_list)
                        json_object['containerVersion'][k] = tagManagerUrl_path_join_string
                    if k == 'container':
                        for l in json_object['containerVersion'][k]:
                            if l == "path":
                                path_list = str(json_object['containerVersion'][k][l]).split('/')
                                path_list[1] = accountId
                                path_list[3] = containerId
                                join_string ='/'.join(path_list)
                                json_object['containerVersion'][k][l] = join_string
                            if l == "accountId":
                                json_object['containerVersion'][k][l] = accountId
                            if l == "containerId":
                                json_object['containerVersion'][k][l] = containerId
                            if l == "publicId":
                                json_object['containerVersion'][k][l] = 'GTM-'+gtm_web_container_id
                            if l == "tagManagerUrl":
                                tagManagerUrl_list = str(json_object['containerVersion'][k][l]).split('/')
                                tagManagerUrl_list[6] = accountId
                                tagManagerUrl_list[8] = containerId
                                join_string_tagManagerUrl ='/'.join(tagManagerUrl_list)
                                json_object['containerVersion'][k][l] = join_string_tagManagerUrl

                for w in json_object['containerVersion']['client']:
                    for e in w:
                        if e == 'accountId':
                            w[e] = accountId
                        if e == 'containerId':
                            w[e] = containerId 
                        if e == 'type':
                            if w[e] == 'cvt_62188107_5':
                                w[e] = 'cvt_'+containerId+'_5'
                            if w[e] == 'cvt_62188107_29':
                                w[e] = 'cvt_'+containerId+'_29'
                        if e == 'name':
                            if w[e] == 'GTM Loader':
                                for m in w['parameter']:
                                    for l in m:
                                        if l == 'key':
                                            if m[l] == "requestPath":
                                                m['value'] = '/'+gtm_endpoint
                        if e == "name":
                            if w[e] == "Data Client":
                                for a in w['parameter']:
                                    for b in a:
                                        if b == 'key':
                                            if a[b] == "path":
                                                for c in a['list']:
                                                    for d in c:
                                                        if d == "type":
                                                            if c[d] == "MAP":
                                                                for f in c['map']:
                                                                    for g in f:
                                                                        if g == 'key':
                                                                            if f[g] == 'path':
                                                                                f['value'] = "/" + server_data_client_endpoint
                    
                for i in json_object['containerVersion']['tag']:
                    for j in i:
                        if j == 'accountId':
                            i[j] = accountId
                        if j == 'containerId':
                            i[j] = containerId
                        if j == 'type':
                            if i[j] == 'cvt_62188107_3':
                                i[j] = 'cvt_'+containerId+'_3'
                    
                for i in json_object['containerVersion']['trigger']:
                    for j in i:
                        if j == 'accountId':
                            i[j] = accountId
                        if j == 'containerId':
                            i[j] = containerId
                
                for i in json_object['containerVersion']['builtInVariable']:
                    for j in i:
                        if j == 'accountId':
                            i[j] = accountId
                        if j == 'containerId':
                                i[j] = containerId
                
                for i in json_object['containerVersion']['variable']:
                    for j in i:
                        if j == 'accountId':
                            i[j] = accountId
                        if j == 'containerId':
                            i[j] = containerId
                        if j == 'name':
                                                    
                            if i[j] == "GA4 - Measurement ID":
                                for g in i['parameter']:
                                    for h in g:
                                        if h == 'value':
                                            g[h] = 'G-'+ga4_property_id
                            
                            if i[j] == "UA - Tracking ID":
                                for c in i['parameter']:
                                    for d in c:
                                        if d == 'value':
                                            c[d] = 'UA-'+ua_property_id
                            
                            if i[j] == "Facebook - Pixel ID":
                                for m in i['parameter']:
                                    for n in m:
                                        if n == 'value':
                                            m[n] = facebook_pixel_id
                                
                            if i[j] == "Facebook - Conversions API Access Token":
                                for e in i['parameter']:
                                    for f in e:
                                        if f == 'value':
                                            e[f] = facebook_auth_token

                for i in json_object['containerVersion']['customTemplate']:
                    for j in i:
                        if j == 'accountId':
                            i[j] = accountId
                        if j == 'containerId':
                            i[j] = containerId
                        if j == 'name':
                            if i[j] == 'GTM Loader':
                                i[j] = '/'+gtm_endpoint

                file_unique_id = str(uuid.uuid4().hex[:6])
                file_name = 'Server_json_' + file_unique_id + "_updated.json"
                file_name1 = str(static_url)+ 'server_json_files/' + file_name

                with open(file_name1, 'w') as file:
                    json.dump(json_object, file, indent=2)

                updated_file = files.objects.create(file_name = file_name, member_id = member_id, file_type='server')
                server_updated_file_name = updated_file.file_name


                # ClientFile
                with open(str(static_url)+ 'client_json_files/' + 'Template - Base - Client.json', "r+") as outfile:
                    json_object1 = json.load(outfile)

                for k in json_object1['containerVersion']:
                    if k == "path":
                        path_list_1 = str(json_object1['containerVersion'][k]).split('/')
                        path_list_1[1] = accountId
                        path_list_1[3] = containerId
                        join_string ='/'.join(path_list_1)
                        json_object1['containerVersion'][k] = join_string
                    if k == "accountId":
                        json_object1['containerVersion'][k] = accountId
                    if k == "containerId":
                        json_object1['containerVersion'][k] = containerId
                    
                    if k == 'container':
                        for l in json_object1['containerVersion'][k]:
                            if l == "path":
                                path_list_2 = str(json_object1['containerVersion'][k][l]).split('/')
                                path_list_2[1] = accountId
                                path_list_2[3] = containerId
                                join_path_list_2 = '/'.join(path_list_2)
                                json_object1['containerVersion'][k][l] = join_path_list_2

                            if l == "accountId":
                                json_object1['containerVersion'][k][l] = accountId

                            if l == "containerId":
                                json_object1['containerVersion'][k][l] = containerId

                            if l == "publicId":
                                json_object1['containerVersion'][k][l] = 'GTM-'+gtm_web_container_id

                            if l == "tagManagerUrl":
                                tagManagerUpath_list = str(json_object1['containerVersion'][k][l]).split('/')
                                tagManagerUpath_list[6] = accountId
                                tagManagerUpath_list[8] = containerId
                                join_path_list_2 = '/'.join(tagManagerUpath_list)
                                json_object1['containerVersion'][k][l] = join_path_list_2
                    if k == "tagManagerUrl":
                        tagManagerUrl_path_list = str(json_object1['containerVersion'][k]).split('/')
                        tagManagerUrl_path_list[6] = accountId
                        tagManagerUrl_path_list[8] = containerId
                        tagManagerUrl_join_path_list_2 = '/'.join(tagManagerUrl_path_list)
                        json_object1['containerVersion'][k] = tagManagerUrl_join_path_list_2
                
                for i in json_object1['containerVersion']['tag']:
                    for j in i:
                        if j == 'accountId':
                            i[j] = accountId

                        if j == 'containerId':
                            i[j] = containerId

                        if j == 'type':
                            if i[j] == 'cvt_61760393_73':
                                i[j] = 'cvt_'+containerId+'_73'

                for i in json_object1['containerVersion']['trigger']:
                    for j in i:
                        if j == 'accountId':
                            i[j] = accountId

                        if j == 'containerId':
                            i[j] = containerId
                
                for i in json_object1['containerVersion']['builtInVariable']:
                    for j in i:
                        if j == 'accountId':
                            i[j] = accountId

                        if j == 'containerId':
                            i[j] = containerId
                
                for i in json_object1['containerVersion']['customTemplate']:
                    for j in i:
                        if j == 'accountId':
                            i[j] = accountId

                        if j == 'containerId':
                            i[j] = containerId
                
                for i in json_object1['containerVersion']['variable']:
                    for j in i:
                        if j == 'accountId':
                            i[j] = accountId

                        if j == 'containerId':
                            i[j] = containerId

                        if j == 'type':
                            if i[j] == 'cvt_61760393_9':
                                i[j] = 'cvt_'+containerId+'_9'

                        if j == 'name':
                            if i[j] == "Tracking Server - Data Client Endpoint":
                                for a in i['parameter']:
                                    for b in a:
                                        if b == 'key':
                                            if a[b] == "value":
                                                a['value'] = "/" + client_data_client_endpoint
                
                            if i[j] == "Tracking Server - Domain":
                                for a in i['parameter']:
                                    for b in a:
                                        if b == 'value':
                                            a[b] = website_domain

                            if i[j] == "Tracking Server - SUB-Domain":
                                for c in i['parameter']:
                                    for d in c:
                                        if d == 'value':
                                            c[d] = subdomain_of_tracking_server
                            
                            if i[j] == "GA4 - Measurement ID":
                                for e in i['parameter']:
                                    for u in e:
                                        if u == 'key':
                                            if e[u] == 'map':
                                                for g in e['list']:
                                                    for h in g:
                                                        if h == 'type':
                                                            if g[h] == 'MAP':
                                                                for x in g['map']:
                                                                    for m in x:
                                                                        if m == 'key':
                                                                            if x[m] == 'value':
                                                                                x['value'] = 'G-'+ga4_property_id
                                                                                
                        
                            if i[j] == "Facebook - Pixel ID":
                                for ab in i['parameter']:
                                    for bc in ab:
                                        if bc == 'key':
                                            if ab[bc] == 'map':
                                                for cd in ab['list']:
                                                    for de in cd:
                                                        if de == 'type':
                                                            if cd[de] == 'MAP':
                                                                for ef in cd['map']:
                                                                    for fg in ef:
                                                                        if fg == 'key':
                                                                            if ef[fg] == 'value':
                                                                                ef['value'] = facebook_pixel_id
                            
                            if i[j] == "Tracking Server - GTM Endpoint":
                                for e in i['parameter']:
                                    for f in e:
                                        if f == 'value':
                                            e[f] = '/' + gtm_endpoint

                file_unique_id = str(uuid.uuid4().hex[:6])
                file_name = 'Client_json_' + file_unique_id + "_updated.json"
                file_name1 = str(static_url)+ 'client_json_files/' + file_name

                with open(file_name1, 'w') as file:
                    json.dump(json_object1, file, indent=2)

                updated_file = files.objects.create(file_name = file_name, file_type = 'client', member_id = member_id)
                client_updated_file_name = updated_file.file_name

                context = {
                    'server_updated_file_name': server_updated_file_name,
                    'client_updated_file_name': client_updated_file_name,
                    'website_domain': website_domain,
                    'website_subdomain': subdomain_of_tracking_server,
                    'gtm_endpoint': gtm_endpoint
                }
                return render(request, 'download_json_file.html', context)
            else:
                return redirect('home')
        else:
            return redirect('singup')
    else:
        if request.session.get('email') and request.session.get('email') != None:
            email = request.session.get('email')
            user = memberdetails.objects.get(email=email)
            if user.is_superuser == False:
                form = MainInput()
                return render(request, 'main_input_form.html', {'form':form})
            else:
                return redirect('home')
        else:
            return redirect('singup')


def download_file(request,id):
    if request.session.get('email') and request.session.get('email') != None:
        email = request.session.get('email')
        user = memberdetails.objects.get(email=email)
        if user.is_superuser == False:
            file = files.objects.get(id=id)
            name_of_file = file.file_name
            file_type = file.file_type

            if file_type == 'server':
                with open(str(static_url)+ 'server_json_files/' +str(name_of_file), "r") as outfile:
                    json_object = json.load(outfile)
                
                for k in json_object['containerVersion']:
                        if k == 'container':
                            for l in json_object['containerVersion'][k]:
                                if l == "publicId":
                                    web_container_id = json_object['containerVersion'][k][l]
                website_subdomain = ''
                gtm_endpoint = ''

            if file_type == 'client':
                user = memberdetails.objects.get(email=request.session.get('email'))
                gtm_endpoint = user.gtm_endpoint
                with open(str(static_url)+ 'client_json_files/' +str(name_of_file), "r+") as outfile:
                    json_object = json.load(outfile)

                for i in json_object['containerVersion']:
                    if i == 'container':
                        for l in json_object['containerVersion'][i]:
                            if l == "publicId":
                                web_container_id = json_object['containerVersion'][i][l]

                for i in json_object['containerVersion']['variable']:
                    for j in i:
                        if i[j] == "Tracking Server - SUB-Domain":
                            for c in i['parameter']:
                                for d in c:
                                    if d == 'value':
                                        website_subdomain = c[d]

            return render(request, 'download_json_file.html',{"file":file, 'website_subdomain':website_subdomain, 'gtm_endpoint':gtm_endpoint, 'web_container_id':web_container_id})
        else:
            return redirect('home')
    else:
        return redirect('singup')


def logout(request):
    auth.logout(request)
    request.session.flush()
    request.session.clear_expired()
    return redirect('singup')