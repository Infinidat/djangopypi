from django.http import HttpResponse, QueryDict
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.datastructures import MultiValueDict
from django.contrib.auth import authenticate


class HttpResponseNotImplemented(HttpResponse):
    status_code = 501


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

    def __init__(self, realm):
        HttpResponse.__init__(self)
        self['WWW-Authenticate'] = 'Basic realm="%s"' % realm


def parse_distutils_request(request):
    """ This is being used because the built in request parser that Django uses,
    django.http.multipartparser.MultiPartParser is interperting the POST data
    incorrectly and/or the post data coming from distutils is invalid.

    One portion of this is the end marker: \r\n\r\n (what Django expects)
    versus \n\n (what distutils is sending).
    """

    try:
        sep = request.body.lstrip().splitlines()[0]
    except:
        raise ValueError('Invalid post data')


    request.POST = QueryDict('',mutable=True)
    try:
        request._files = MultiValueDict()
    except Exception, e:
        pass

    for part in filter(lambda e: e.strip(), request.body.split(sep)):
        try:
            header, content = part.lstrip().split('\r\n\r\n', 1)
        except Exception:
            continue

        content = content.strip()
        header_parts = get_content_disposition(header)

        if "name" not in header_parts:
            continue

        if "filename" in header_parts:
            dist = TemporaryUploadedFile(name=header_parts["filename"],
                                         size=len(content),
                                         content_type="application/gzip",
                                         charset='utf-8')
            dist.write(content)
            dist.seek(0)
            request.FILES.appendlist(header_parts['name'], dist)
        else:
            request.POST.appendlist(header_parts["name"],content)
    return


def get_content_disposition(header):
    for header in header.split('\r\n'):
        header_type, header_content = header.split(';', 1)
        if not header_type.startswith('Content-Disposition'):
            continue

        header_parts = {}
        for item in header_content.split(';'):
            item = item.strip()
            try:
                key, value = item.split("=", 1)
            except ValueError:
                continue
            header_parts[key.strip()] = value.strip('"')
        return header_parts


def login_basic_auth(request):
    authentication = request.META.get("HTTP_AUTHORIZATION")
    if not authentication:
        return
    (authmeth, auth) = authentication.split(' ', 1)
    if authmeth.lower() != "basic":
        return
    auth = auth.strip().decode("base64")
    username, password = auth.split(":", 1)
    return authenticate(username=username, password=password)
