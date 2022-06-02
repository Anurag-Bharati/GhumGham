from django.shortcuts import render, redirect
from packages.models import Packages
from packages.forms import PackagesForm


# Create your views here.
def admin(request):
    return render(request, 'admins_home.html', {})


def showpackages(request):
    packagess = Packages.objects.all().filter(is_featured=True)
    # it means (select * from Admins )
    return render(request, "packages.html", {'packagess': packagess})


def addpackages(request):
    if request.method == 'POST':
        package_name = request.POST["package_name"]
        price = request.POST['price']
        coverpick = request.POST["coverpick"]
        rating = request.POST["rating"]
        event = request.POST["event"]
        destination_list = request.POST["destination_list"]
        description = request.POST["description"]
        image = request.FILES["image"]
        packages = Packages(packagess_name=package_name, price=price, cover_pick=coverpick, rating=rating, event=event,
                            destination_List=destination_list, description=description, image=image, is_featured=True)
        packages.save()
        return redirect('/admin/packages')

    else:
        return render(request, "add_packages.html", {})


def packages_delete(request, p_id):
    product = Packages.objects.get(p_id=p_id)
    product.delete()
    return redirect('/admin/packages')


def update_packages(request, update_id):
    packages = Packages.objects.get(p_id=update_id)

    if (request.method == "POST"):
        form = PackagesForm(request.POST, request.FILES, instance=packages)

        if form.is_valid():
            form.save()
            return redirect('/admin/packages/')

        else:
            return render(request, "update_packages.html", {'packages': packages})
    return render(request, "update_packages.html", {'packages': packages})
