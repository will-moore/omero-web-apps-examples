#
# Copyright (c) 2017 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import JsonResponse
import omero

from omeroweb.decorators import login_required

# login_required: if not logged-in, will redirect to webclient
# login page. Then back to here, passing in the 'conn' connection
# and other arguments **kwargs.
@login_required()
def index(request, conn=None, **kwargs):

    # We can load data from OMERO via Blitz Gateway connection.
    # See https://docs.openmicroscopy.org/latest/omero/developers/Python.html
    experimenter = conn.getUser()

    # A dictionary of data to pass to the html template
    context = {'firstName': experimenter.firstName,
               'lastName': experimenter.lastName,
               'experimenterId': experimenter.id}
    # print can be useful for debugging, but remove in production
    # print 'context', context

    # Render the html template and return the http response
    return render(request, 'minimal_webapp/index.html', context)

@login_required()
def best(request, conn=None, **kwargs):

    qs = conn.getQueryService()
    params = omero.sys.ParametersI()
    params.addLong('rating', 5)

    query = """select image from Image as image
        left outer join fetch image.annotationLinks as annLink
        left outer join fetch annLink.child as ann
        where ann.longValue=:rating"""

    result = qs.findAllByQuery(query, params)

    data = []
    for l in result:
        # print l
        data.append({'id': l.id.val, 'name': l.name.val})

    return JsonResponse({"count": len(result), "data": data})
